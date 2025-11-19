FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Port mapping to localhost is configured at runtime. Example:
# docker run -p 127.0.0.1:8000:8000 <image-name>

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
