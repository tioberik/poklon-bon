# Koristimo zvaničnu Python 3.12 sliku kao osnovu
FROM python:3.12-slim

# Postavljanje radnog direktorija u kontejneru
WORKDIR /app

# Kopiranje potrebnih fajlova u kontejner
COPY requirements.txt .

# Instalacija zavisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiranje ostatka aplikacije u kontejner
COPY . .

# Postavljanje env varijabli za pokretanje aplikacije
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=password
ENV MYSQL_HOST=mysql
ENV MYSQL_DB=poklon_bon_db

EXPOSE 8000
EXPOSE 3306
EXPOSE 6379

# Pokretanje aplikacije
CMD ["uvicorn", "poklon_bon.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
