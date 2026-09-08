FROM python:3.10-slim

WORKDIR /app

# Dependencies pehle copy/install karo (Docker caching optimize karta hai)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora code copy karo
COPY . .

# Port expose karo
EXPOSE 8000

# Container start hone pe yeh command chalegi
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]