# استخدم صورة Python خفيفة
FROM python:3.11-slim

# تثبيت المتطلبات اللازمة لتشغيل moviepy
RUN apt-get update && apt-get install -y ffmpeg imagemagick && apt-get clean

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المشروع إلى الصورة
COPY . /app

# تثبيت حزم Python المطلوبة
RUN pip install --upgrade pip && pip install -r requirements.txt

# تحديد المنفذ
EXPOSE 10000

# أمر التشغيل
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
