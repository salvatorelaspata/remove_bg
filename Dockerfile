FROM python:3.9-slim

# Installa dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file delle dipendenze e installa i pacchetti Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY app.py .

# Espone la porta su cui gira il servizio
EXPOSE 8002

# Avvia l'applicazione con Uvicorn usando il modulo Python
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]