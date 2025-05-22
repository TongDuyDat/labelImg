import sqlite3
import os
import glob

class YoloLabelManager:
    def __init__(self, db_path="image_labels.db"):
        """Khởi tạo kết nối cơ sở dữ liệu SQLite."""
        self.db_path = db_path
        self.selected_dir = ""  # Lưu thư mục người dùng chọn
        self.conn, self.cursor = self._init_db()

    def _init_db(self):
        """Tạo cơ sở dữ liệu và các bảng nếu chưa tồn tại."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tạo bảng labels
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS labels (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT
            )
        ''')
        
        # Tạo bảng images (lưu file_name thay vì file_path)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tạo bảng image_labels
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_labels (
                image_id TEXT,
                label_id TEXT,
                PRIMARY KEY (image_id, label_id),
                FOREIGN KEY (image_id) REFERENCES images(image_id),
                FOREIGN KEY (label_id) REFERENCES labels(id)
            )
        ''')
        
        # Tạo bảng bounding_boxes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bounding_boxes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id TEXT,
                label_id TEXT,
                x_center REAL,
                y_center REAL,
                width REAL,
                height REAL,
                FOREIGN KEY (image_id) REFERENCES images(image_id),
                FOREIGN KEY (label_id) REFERENCES labels(id)
            )
        ''')
        
        # Tạo chỉ mục để tối ưu truy vấn
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_labels ON image_labels(label_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_bounding_boxes ON bounding_boxes(image_id, label_id)')
        
        conn.commit()
        return conn, cursor

    def _collect_labels(self, labels_dir):
        """Quét thư mục để thu thập class_id duy nhất."""
        if not os.path.exists(labels_dir):
            raise FileNotFoundError(f"Thư mục {labels_dir} không tồn tại")
        
        class_ids = set()
        txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
        
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    class_id = parts[0]
                    class_ids.add(class_id)
        
        # Thêm class_id vào bảng labels với tên mặc định
        for class_id in class_ids:
            self.cursor.execute('''
                INSERT OR REPLACE INTO labels (id, name, description)
                VALUES (?, ?, ?)
            ''', (class_id, f"label_{class_id}", ''))
        
        self.conn.commit()

    def import_yolo_data(self, labels_dir):
        """Nhập dữ liệu từ file YOLO (.txt) trong thư mục người dùng chọn."""
        if not os.path.exists(labels_dir):
            raise FileNotFoundError(f"Thư mục {labels_dir} không tồn tại")
        
        # Lưu thư mục người dùng chọn
        self.selected_dir = labels_dir
        
        # Thu thập và nhập nhãn từ file .txt
        self._collect_labels(labels_dir)
        
        # Quét file .txt
        txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
        
        for txt_file in txt_files:
            try:
                image_id = os.path.splitext(os.path.basename(txt_file))[0]
                
                # Giả định tên file ảnh (thêm đuôi .jpg, có thể tùy chỉnh)
                file_name = f"{image_id}.jpg"  # Có thể hỗ trợ .jpeg, .png nếu cần
                
                # Thêm ảnh vào bảng images
                self.cursor.execute('''
                    INSERT OR REPLACE INTO images (image_id, file_name)
                    VALUES (?, ?)
                ''', (image_id, file_name))
                
                # Đọc file .txt và lấy nhãn
                with open(txt_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) < 5:
                            continue
                        class_id = parts[0]
                        x_center, y_center, width, height = map(float, parts[1:5])
                        
                        # Thêm vào bảng image_labels
                        self.cursor.execute('''
                            INSERT OR REPLACE INTO image_labels (image_id, label_id)
                            VALUES (?, ?)
                        ''', (image_id, class_id))
                        
                        # Thêm vào bảng bounding_boxes
                        self.cursor.execute('''
                            INSERT INTO bounding_boxes (image_id, label_id, x_center, y_center, width, height)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (image_id, class_id, x_center, y_center, width, height))
            except sqlite3.Error as e:
                print(f"SQLite error: {e} while processing file {txt_file}")
            except FileNotFoundError as e:
                print(f"File not found: {e} while processing file {txt_file}")
            except PermissionError as e:
                print(f"Permission error: {e} while processing file {txt_file}")
            except Exception as e:
                print(f"Error processing file {txt_file}: {e}")
        
        self.conn.commit()

    def filter_images_by_label(self, label_id):
        """Lọc ảnh dựa trên nhãn, trả về đường dẫn đầy đủ."""
        self.cursor.execute('''
            SELECT i.image_id, i.file_name, i.created_at
            FROM images i
            JOIN bounding_boxes bb ON i.image_id = bb.image_id
            WHERE bb.label_id = ?
        ''', (label_id,))
        
        results = self.cursor.fetchall()
        # Kết hợp selected_dir với file_name để tạo full_path
        return [{
            "image_id": row[0],
            "file_path": os.path.join(self.selected_dir, row[1]) if self.selected_dir else row[1],
            "created_at": row[2]
        } for row in results]

    def assign_label_to_image(self, image_id, label_id):
        """Thêm nhãn cho ảnh."""
        self.cursor.execute('''
            INSERT OR REPLACE INTO image_labels (image_id, label_id)
            VALUES (?, ?)
        ''', (image_id, label_id))
        self.conn.commit()

    def remove_label_from_image(self, image_id, label_id):
        """Xóa nhãn khỏi ảnh."""
        self.cursor.execute('''
            DELETE FROM image_labels
            WHERE image_id = ? AND label_id = ?
        ''', (image_id, label_id))
        self.cursor.execute('''
            DELETE FROM bounding_boxes
            WHERE image_id = ? AND label_id = ?
        ''', (image_id, label_id))
        self.conn.commit()

    def get_bounding_boxes(self, image_id):
        """Lấy thông tin hộp giới hạn của ảnh."""
        self.cursor.execute('''
            SELECT label_id, x_center, y_center, width, height
            FROM bounding_boxes
            WHERE image_id = ?
        ''', (image_id,))
        results = self.cursor.fetchall()
        return [{"label_id": row[0], "x_center": row[1], "y_center": row[2], "width": row[3], "height": row[4]} for row in results]

    def clear_data(self):
        """Xóa toàn bộ dữ liệu trong cơ sở dữ liệu."""
        self.cursor.execute("DELETE FROM bounding_boxes")
        self.cursor.execute("DELETE FROM image_labels")
        self.cursor.execute("DELETE FROM images")
        self.cursor.execute("DELETE FROM labels")
        self.selected_dir = ""  # Xóa thư mục đã chọn
        self.conn.commit()

    def close(self):
        """Đóng kết nối cơ sở dữ liệu."""
        self.conn.close()
    
    def save_data(self, temp_data):
        """Lưu dữ liệu từ temp_data vào cơ sở dữ liệu SQLite."""
        try:
            # 1. Lưu nhãn vào bảng labels
            for label in temp_data.get("labels", []):
                self.cursor.execute('''
                    INSERT OR REPLACE INTO labels (id, name, description)
                    VALUES (?, ?, ?)
                ''', (label["id"], label["name"], label["description"]))

            # 2. Lưu ảnh vào bảng images
            for image in temp_data.get("images", []):
                self.cursor.execute('''
                    INSERT OR REPLACE INTO images (image_id, file_name)
                    VALUES (?, ?)
                ''', (image["image_id"], image["file_name"]))

                # 3. Lưu quan hệ ảnh-nhãn vào bảng image_labels
                for label_id in image.get("label_ids", []):
                    self.cursor.execute('''
                        INSERT OR REPLACE INTO image_labels (image_id, label_id)
                        VALUES (?, ?)
                    ''', (image["image_id"], label_id))

                # 4. Lưu hộp giới hạn vào bảng bounding_boxes
                # Xóa các hộp giới hạn cũ của ảnh để tránh trùng lặp
                self.cursor.execute('''
                    DELETE FROM bounding_boxes WHERE image_id = ?
                ''', (image["image_id"],))
                
                for bbox in image.get("bounding_boxes", []):
                    self.cursor.execute('''
                        INSERT INTO bounding_boxes (image_id, label_id, x_center, y_center, width, height)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        image["image_id"],
                        bbox["label_id"],
                        bbox["x_center"],
                        bbox["y_center"],
                        bbox["width"],
                        bbox["height"]
                    ))

            # Cam kết thay đổi
            self.conn.commit()
            print("Đã lưu dữ liệu vào cơ sở dữ liệu SQLite thành công.")
        except sqlite3.Error as e:
            print(f"Lỗi SQLite khi lưu dữ liệu: {str(e)}")
            raise
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {str(e)}")
            raise