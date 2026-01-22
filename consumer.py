import json
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine

# --- CONFIGURATION KAFKA ---
TOPIC = "nfe101-topic"
BOOTSTRAP_SERVERS = "localhost:9092"  # ou localhost selon Docker

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# --- CONFIGURATION POSTGRESQL ---
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nfe101"

# Crée l'engine SQLAlchemy
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

print("Démarrer, en attente de messages...")

# --- TRAITEMENT DES MESSAGES ---
for message in consumer:
    data = message.value
    # Convertir en DataFrame pandas (1 ligne)
    df = pd.DataFrame([data])
    # Insérer dans PostgreSQL
    df.to_sql(schema='projet2',name='loyers',con=engine, if_exists='append', index=False)
    print(f"Ligne insérée dans PostgreSQL: {data}")