@echo off
echo == BAT DAU CAI DAT VA CHAY LABELIMG ==

:: Kiểm tra xem conda có sẵn không
where conda >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong tim thay Miniconda. Vui long cai dat Miniconda truoc.
    echo Tai Miniconda tai: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

:: Kiểm tra môi trường labelimg
echo Kiem tra moi truong Conda 'labelimg'...
conda env list | findstr /C:"labelimg " >nul
if %ERRORLEVEL% neq 0 (
    echo Moi truong 'labelimg' chua ton tai. Dang tao moi truong...
    call conda create -n labelimg python=3.8 -y
    :: Kiểm tra lại môi trường sau khi tạo
    conda env list | findstr /C:"labelimg " >nul
    echo Moi truong labelimg da duoc tao.
) else (
    echo Moi truong labelimg da ton tai.
)

:: Kích hoạt môi trường và cài đặt thư viện
echo Kich hoat moi truong labelimg va cai dat thu vien...
call conda activate labelimg
if %ERRORLEVEL% neq 0 (
    echo [LOI] Kich hoat moi truong labelimg that bai.
    pause
    exit /b 1
)

:: Cài đặt labelImg và các thư viện phụ thuộc
echo Cai dat labelImg va thu vien...
pip install labelImg pyqt5 lxml
if %ERRORLEVEL% neq 0 (
    echo [LOI] Cai dat labelImg hoac thu vien that bai.
    pause
    exit /b 1
)
echo Cai dat labelImg va thu vien thanh cong.

:: Chạy labelImg
echo Chay labelImg voi classes.txt...
conda run -n labelimg python labelImg.py class_file classes.txt
if %ERRORLEVEL% neq 0 (
    echo [LOI] Chay labelImg that bai. Kiem tra lai cai dat hoac tep classes.txt.
    pause
    exit /b 1
)

echo == HOAN TAT ==
pause