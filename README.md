# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG PHẦN MỀM LABELIMG

## 1. Giới thiệu
**labelImg** là một công cụ mã nguồn mở dùng để gắn nhãn (annotation) cho hình ảnh, hỗ trợ các định dạng như YOLO, Pascal VOC, và CreateML. Phần mềm này được sử dụng rộng rãi để chuẩn bị dữ liệu huấn luyện cho các mô hình học máy, đặc biệt trong nhiệm vụ phát hiện đối tượng.

Hướng dẫn này cung cấp các bước chi tiết để:
- Cài đặt labelImg thông qua Miniconda.
- Tạo môi trường ảo và cài đặt công cụ.
- Clone mã nguồn từ GitHub (nếu cần).
- Chuẩn bị tệp `classes.txt` và thực hiện gán nhãn theo định dạng YOLO.

---

## 2. Cài đặt labelImg

### 2.1. Cài đặt Miniconda
Miniconda là trình quản lý môi trường Python nhẹ, giúp tạo môi trường ảo để tránh xung đột thư viện.

**Bước 1: Tải Miniconda**
- Truy cập trang web: https://docs.conda.io/en/latest/miniconda.html
- Chọn phiên bản phù hợp:
  - Hệ điều hành: Windows, macOS, hoặc Linux.
  - Python: 3.8 hoặc 3.9 (khuyến nghị).
- Tải tệp cài đặt (ví dụ: `Miniconda3-latest-Windows-x86_64.exe` cho Windows).

**Bước 2: Cài đặt Miniconda**
- Chạy tệp cài đặt.
- Chọn **Install for all users** (khuyến nghị) hoặc chỉ cho người dùng hiện tại.
- Giữ đường dẫn mặc định (ví dụ: `C:\Users\<Username>\Miniconda3` trên Windows).
- Tích tùy chọn **Add Miniconda to PATH** để dễ dàng sử dụng lệnh `conda`.
- Hoàn tất cài đặt.

**Bước 3: Kiểm tra cài đặt**
- Mở Command Prompt (Windows) hoặc Terminal (macOS/Linux).
- Gõ lệnh:
  ```
  conda --version
  ```
- Nếu hiển thị phiên bản (ví dụ: `conda 23.7.4`), cài đặt thành công.

### 2.2. Tạo môi trường ảo
**Bước 1: Tạo môi trường**
- Mở terminal và gõ:
  ```
  conda create -n labelimg python=3.8
  ```
  - `labelimg`: Tên môi trường ảo (có thể đổi).
  - `python=3.8`: Sử dụng Python 3.8.

**Bước 2: Kích hoạt môi trường**
- Gõ:
  ```
  conda activate labelimg
  ```
- Bạn sẽ thấy `(labelimg)` trước dấu nhắc lệnh, cho biết môi trường đã kích hoạt.

### 2.3. Cài đặt labelImg
Có hai phương pháp: cài qua pip hoặc clone từ GitHub.

**Phương pháp 1: Cài qua pip**
- Trong môi trường ảo, gõ:
  ```
  pip install labelImg
  pip install pyqt5 lxml
  ```
- Kiểm tra:
  ```
  labelImg
  ```
- Nếu giao diện labelImg mở ra, bỏ qua bước clone.

**Phương pháp 2: Clone từ GitHub**
- **Cài Git** (nếu chưa có):
  - Windows: Tải từ https://git-scm.com/download/win.
  - Ubuntu/Debian: `sudo apt-get install git`.
  - macOS: `brew install git` (yêu cầu Homebrew).
- Clone mã nguồn:
  ```
  git clone https://github.com/tzutalin/labelImg.git
  cd labelImg
  ```
- Cài thư viện:
  ```
  pip install pyqt5 lxml
  ```
- (Tùy chọn) Nếu sử dụng mã tùy chỉnh:
  - Sao chép `labelImg.py` vào thư mục `labelImg`.
  - Sao chép `import_labels.py` vào thư mục `labelImg/libs`.
- Chạy:
  ```
  python labelImg.py
  ```

### 2.4. Xử lý lỗi cài đặt
- **Lỗi thiếu PyQt5**:
  ```
  pip install pyqt5
  ```
- **Lỗi `resources.py`**:
  - Trong thư mục `labelImg`, chạy:
    ```
    pyrcc5 -o libs/resources.py resources.qrc
    ```
- **Lỗi Python version**:
  - Kiểm tra:
    ```
    python --version
    ```
  - Đảm bảo dùng Python 3.6–3.9.

---

## 3. Gắn nhãn với labelImg

### 3.1. Chuẩn bị tệp `classes.txt`
Tệp `classes.txt` định nghĩa các lớp (labels) dùng để gán nhãn.

**Bước 1: Tạo tệp**
- Mở Notepad hoặc trình soạn thảo văn bản.
- Viết mỗi lớp trên một dòng, ví dụ:
  ```
  person
  car
  dog
  ```
- Lưu với tên `classes.txt` (không dùng `.text`).

**Bước 2: Đặt tệp**
- Sao chép `classes.txt` vào thư mục lưu nhãn (ví dụ: `/path/to/annotations`).
- Hoặc đặt trong `labelImg/data/predefined_classes.txt`.

### 3.2. Mở thư mục ảnh
**Bước 1: Mở labelImg**
- Kích hoạt môi trường:
  ```
  conda activate labelimg
  cd path/to/labelImg
  python labelImg.py
  ```

**Bước 2: Mở thư mục**
- Nhấn **Ctrl+U** hoặc vào **File > Open Dir**.
- Chọn thư mục chứa ảnh (ví dụ: `/path/to/images`).
- Danh sách ảnh xuất hiện trong **File List** (bên phải).

**Bước 3: (Tùy chọn) Chỉ định thư mục lưu nhãn**
- Nhấn **Ctrl+R** hoặc vào **File > Change Save Dir**.
- Chọn thư mục lưu nhãn (ví dụ: `/path/to/annotations`, nơi có `classes.txt`).

### 3.3. Thực hiện gán nhãn
**Bước 1: Mở ảnh**
- Nhấp đúp vào ảnh trong **File List**.

**Bước 2: Vẽ hộp giới hạn**
- Nhấn **W** hoặc nút **Create RectBox**.
- Nhấp và kéo chuột để vẽ hình chữ nhật quanh đối tượng.
- Cửa sổ nhập nhãn hiện ra:
  - Nhập **class ID** (dựa trên `classes.txt`):
    - `0` cho `person`.
    - `1` cho `car`.
    - `2` cho `dog`.
  - Hoặc chọn từ danh sách nếu `classes.txt` được tải.
  - Nhấn **OK**.

**Bước 3: Chỉnh sửa nhãn**
- **Sửa nhãn**: Nhấp đúp vào nhãn trong **Box Labels**, nhập ID mới.
- **Xóa**: Chọn hộp, nhấn **Delete**.
- **Di chuyển/Thay đổi kích thước**: Kéo hộp hoặc các góc trên canvas.

**Bước 4: Lưu nhãn**
- Nhấn **Ctrl+S** hoặc vào **File > Save**.
- Tệp `.txt` (YOLO format) lưu trong thư mục đã chọn, ví dụ:
  ```
  0 0.5 0.5 0.2 0.3
  1 0.6 0.4 0.1 0.2
  ```
- Dữ liệu cũng lưu vào `image_labels.db`.

**Bước 5: Chuyển ảnh**
- Nhấn **D** (ảnh tiếp theo) hoặc **A** (ảnh trước).
- Bật **Auto Save** (menu **View > Auto Save Mode**) để tự động lưu.

### 3.4. (Tùy chọn) Nhập và tìm kiếm nhãn
**Nhập dữ liệu YOLO**:
- Vào **File > Import Data** hoặc nhấn **Ctrl+I**.
- Chọn thư mục chứa tệp `.txt`.
- Dữ liệu nhập vào `image_labels.db`.

**Tìm kiếm ảnh theo nhãn**:
- Nhập `class_id` (ví dụ: `0`) vào ô **Tìm kiếm theo nhãn** trong **File List**.
- Nhấn **Enter** để lọc ảnh.
- Nhấp đúp để xem ảnh.

---

## 4. Phím tắt hữu ích
- **Ctrl+O**: Mở ảnh.
- **Ctrl+U**: Mở thư mục ảnh.
- **Ctrl+S**: Lưu nhãn.
- **Ctrl+I**: Nhập dữ liệu YOLO.
- **W**: Tạo hộp giới hạn.
- **D**: Ảnh tiếp theo.
- **A**: Ảnh trước.
- **Delete**: Xóa hộp.
- **Ctrl++**: Phóng to.
- **Ctrl+-**: Thu nhỏ.

---

## 5. Xử lý lỗi
- **Tệp `classes.txt` không tải**:
  - Kiểm tra tệp trong thư mục lưu nhãn hoặc `labelImg/data`.
  - Đảm bảo mỗi lớp trên một dòng.
- **Lỗi lưu nhãn**:
  - Kiểm tra quyền ghi thư mục.
  - Đảm bảo ảnh đã mở.
- **Lỗi tìm kiếm nhãn**:
  - Nhập dữ liệu YOLO trước (**File > Import Data**).
  - Kiểm tra `class_id` đúng.
- **Lỗi cơ sở dữ liệu**:
  - Xóa `image_labels.db` và nhập lại dữ liệu.

---

## 6. Kết luận
Hướng dẫn này giúp bạn cài đặt labelImg qua Miniconda, tạo môi trường ảo, và gán nhãn ảnh theo định dạng YOLO. Hãy chuẩn bị `classes.txt` và thư mục lưu nhãn đúng cách. Tham khảo thêm tại: https://github.com/tzutalin/labelImg.