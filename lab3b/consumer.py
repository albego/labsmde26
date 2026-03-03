from confluent_kafka import Consumer, KafkaError
import json

# Configuración Sustituir @ por el valor de tu configuración
topic_name = '@'
bootstrap_servers = '@.servicebus.windows.net:9093'  # Endpoint de Event Hubs
sasl_password = 'Endpoint=sb://@.servicebus.windows.net/;SharedAccessKeyName=@;SharedAccessKey=@'  # Cadena de conexión SASL

# Configuración del consumidor de Kafka para Azure Event Hubs
config = {
    'bootstrap.servers': bootstrap_servers,  # Usar variable bootstrap_servers
    'security.protocol': 'SASL_SSL',  # Protocolo de seguridad
    'sasl.mechanism': 'PLAIN',  # Mecanismo de autenticación
    'sasl.username': '$ConnectionString',  # Nombre de usuario (siempre es $ConnectionString)
    'sasl.password': sasl_password,  # Usar variable sasl_password
    'group.id': 'lab3',
    'auto.offset.reset': 'earliest'  # Comienza a leer desde el inicio del stream si es la primera vez
}

# Crear un consumidor al topico
consumer = Consumer(**config)
consumer.subscribe([topic_name])

# Inicializar el contador
message_counter = 0

# Procesar mensajes
try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fin de la partición
                continue
            else:
                print(msg.error())
                break

        # Incrementar el contador de mensajes
        message_counter += 1

        # Mensaje recibido
        print('Received message: {}'.format(json.loads(msg.value().decode('utf-8'))))
        print('Total messages received: {}'.format(message_counter))
        print('\n')

except KeyboardInterrupt:
    pass
finally:
    # Cerrar el consumidor
    consumer.close()
