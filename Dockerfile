# استخدم صورة Python الرسمية
FROM python:3.11-slim

# تثبيت المتطلبات النظامية لـ moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && apt-get clean

# إعداد مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY . /app

# تثبيت المتطلبات
RUN pip install --upgrade pip && pip install -r requirements.txt

# فتح المنفذ
EXPOSE 10000

# أمر التشغيل
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
