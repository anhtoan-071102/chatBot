# Sử dụng образ Python 3.10 như cơ sở
FROM python:3.10-slim

# Đặt biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tạo thư mục ứng dụng và đặt làm thư mục làm việc
RUN mkdir /qna_project
WORKDIR /qna_project

# Cài đặt các phụ thuộc hệ thống
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    default-libmysqlclient-dev \
    build-essential \
    && apt-get clean

# Sao chép tệp requirements.txt và cài đặt các thư viện
COPY requirements.txt /qna_project/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /qna_project/

# Chạy các lệnh migrate để tạo cơ sở dữ liệu
RUN python manage.py migrate

# Chạy server phát triển
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]