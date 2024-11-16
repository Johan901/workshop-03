import datetime
from confluent_kafka import Consumer
import joblib
import json
from sqlalchemy.orm import sessionmaker
import pandas as pd
import sys
import os
import sklearn

# Añadir ruta personalizada para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), "../Connection"))
from database_conn import obtener_conexion  # Importar función para conexión a la base de datos

# Cargar el modelo con manejo de errores
try:
    model = joblib.load(os.path.join(os.path.dirname(__file__), "../Model/model.pkl"))
    print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    sys.exit(1)

# Conectar a la base de datos
connection = obtener_conexion()

# Configurar el consumidor de Confluent Kafka
conf_cons = {
    'bootstrap.servers': 'localhost:9092',
    'security.protocol': 'PLAINTEXT',
    'group.id': 'prediction-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf_cons)
consumer.subscribe(['prediction'])

# Definir las columnas esperadas por el modelo, excluyendo 'Happiness Score'
expected_columns = [
    'Economy (GDP per Capita)',
    'Family',
    'Health (Life Expectancy)',
    'Freedom',
    'Trust (Government Corruption)',
    'Generosity',
    'Dystopia Residual',
    'Year'
]

try:
    while True:
        print("Esperando mensajes...")
        message = consumer.poll(1.0)
        if message is None:
            print("No se recibió ningún mensaje.")
            continue
        if message.error():
            print(f"Error del consumidor: {message.error()}")
            continue

        print("Mensaje recibido")
        kafka = json.loads(message.value().decode('utf-8'))
        df1 = pd.DataFrame([kafka])

        # Asegurarse de que todos los valores están completos antes de la predicción
        df1.fillna('NULL', inplace=True)  # Rellena con un valor predeterminado, como 'NULL'

        # Excluir 'Happiness Score' del DataFrame para la predicción
        df = df1[expected_columns]

        # Realizar la predicción
        try:
            predicted = model.predict(df)[0]
            kafka['prediction'] = predicted
            print(f"Predicción realizada: {predicted}")
        except Exception as e:
            print(f"Error en la predicción: {e}")
            continue

        # Agregar la predicción a `df1`
        df1 = pd.concat([df1, pd.DataFrame([kafka])], ignore_index=True)

        # Cargar el DataFrame a Postgres, asegurándose de que no haya valores `NaN`
        try:
            Session = sessionmaker(bind=connection)
            session = Session()
            df1.to_sql("prediction", con=connection, if_exists="append", index=False)
            print(f"[{datetime.datetime.now()}] - Datos cargados a la tabla 'prediction'")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

except KeyboardInterrupt:
    print("Proceso interrumpido por el usuario.")
finally:
    consumer.close()
    print("Consumidor cerrado.")
