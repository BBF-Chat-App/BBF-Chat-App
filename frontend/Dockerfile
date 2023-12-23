FROM python:3.8-slim

# Çalışma dizini oluştur
WORKDIR /app
COPY templates /app/templates

# Gerekli Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Consumer scriptini kopyala
COPY main.py .

# Consumer scriptini çalıştır
CMD ["python", "main.py"]