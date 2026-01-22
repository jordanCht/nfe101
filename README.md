# NFE101 - mini projet 2

Projet traitant les trois premiers points du TP n°2. 

- Nettoyage des données, 
- Diffusion dans un topic Kafka
- Consommation du topic et enregistrement en base de données
- Exposition des données par API.

## Donnée source

Cartographie nationale des loyers au mètre carré.

Documentation de la source : https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2025
Lien stable : https://www.data.gouv.fr/api/1/datasets/r/8623fa1b-6575-4122-ab7a-bc241d610851

## Architecture

Le système se compose de trois principaux composants :

1.  **Producteur (`producer.py`)**: Lit les enregistrements du fichier CSV des données nettoyées (`data/TP2_NFE101.csv`) et les publie en tant que messages dans un topic Kafka (`nfe101-topic`).
2.  **Consommateur (`consumer.py`)**: S'abonne au topic Kafka, consomme les messages et les enregistre dans une table `loyers` d'une base de données PostgreSQL.
3.  **API (`exposition.py`)**: Une API qui expose les données stockées en base.

### Apache kafka

Le serveur kafka est executé sur dans un container docker. L'image officiel est utilisée (apache/kafka-4.1.1)

Documentation officiel : https://kafka.apache.org/quickstart/

Création du topic

```
$ opt/kafka/bin/kafka-topics.sh --create --topic nfe101-topic --bootstrap-server localhost:9092
```

### Points de terminaison de l'API

Fastapi permet de mettre en place rapidement la couche d'exposition des données.

Les points de terminaison suivants sont disponibles :

- `GET /docs`: Accès à la documentation interactive de l'API (Swagger UI).
- `GET /loyers`: Récupère tous les enregistrements de données sur les loyers.
- `GET /loyers/{code_insee}`: Récupère les données de loyer pour une municipalité spécifique par son code INSEE.
