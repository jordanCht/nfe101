from kafka import KafkaProducer
import pandas as pd
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "nfe101-topic"

# producer.send("nfe101-topic", {"message": "Hello Kafka with uv"})
# producer.send("nfe101-topic", {"message": "Hello Kafka with uv 1"})
# producer.send("nfe101-topic", {"message": "Hello Kafka with uv 2"})
# producer.flush()

df = pd.read_csv("data/TP2_NFE101.csv", sep=";")

for _, row in df.iterrows():
    message = row.to_dict()  # convertit la ligne en dict
    producer.send(topic, message)

# S'assurer que tous les messages sont envoyés
producer.flush()
producer.close()

print("Message envoyé")