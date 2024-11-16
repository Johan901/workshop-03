from confluent_kafka import Producer
import pandas as pd
import json
import time

# Cargar el conjunto de datos limpio
dataset = pd.read_csv("../data/cleaned.csv")

# Rellenar NaN con un valor predeterminado para evitar valores NULL en los datos enviados
dataset = dataset.fillna('NULL')  # Usa un valor que prefieras en lugar de 'NULL'

# Configuración del productor de Kafka
kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'security.protocol': 'PLAINTEXT'
}
kafka_producer = Producer(kafka_config)

def confirmar_entrega(error, mensaje):
    if error is not None:
        print(f"Error al enviar el mensaje: {error}")
    else:
        print(f"Mensaje enviado al tópico {mensaje.topic()} en la partición {mensaje.partition()}")

print("Iniciando el envío de mensajes...")

# Iterar sobre cada fila del conjunto de datos y enviar al tópico de Kafka
for _, fila in dataset.iterrows():
    contenido_mensaje = fila[[
        'Happiness Score',
        'Economy (GDP per Capita)',
        'Family',
        'Health (Life Expectancy)',
        'Freedom',
        'Trust (Government Corruption)',
        'Generosity',
        'Dystopia Residual',
        'Year'
    ]].to_dict()

    kafka_producer.produce(
        topic="prediction",
        value=json.dumps(contenido_mensaje),
        callback=confirmar_entrega
    )
    kafka_producer.poll(0)  # Asegura el manejo de mensajes en cola
    print(f"Mensaje enviado al tópico 'prediction': {contenido_mensaje}")
    time.sleep(1)

# Asegurar que todos los mensajes pendientes se envíen antes de finalizar
kafka_producer.flush()
print("Todos los mensajes han sido enviados exitosamente al tópico.")
