import json
import random
import uuid
from datetime import datetime, timedelta
import pytz
from confluent_kafka import Producer

# Configuración
topic_name = 'eh-transactions'
bootstrap_servers = SUSTITUIR.servicebus.windows.net:9093'  # Endpoint de Event Hubs
sasl_password = SUSTITUIR'  # Cadena de conexión SASL

# Configuración del productor de Kafka para Azure Event Hubs
conf = {
    'bootstrap.servers': bootstrap_servers,  # Usar variable bootstrap_servers
    'security.protocol': 'SASL_SSL',  # Protocolo de seguridad
    'sasl.mechanism': 'PLAIN',  # Mecanismo de autenticación
    'sasl.username': '$ConnectionString',  # Nombre de usuario (siempre es $ConnectionString)
    'sasl.password': sasl_password,  # Usar variable sasl_password
    'client.id': 'python'  # Identificador del cliente
}

# Crear el productor de Kafka
producer = Producer(**conf)

# Función de callback para confirmar la entrega del mensaje
def delivery_report(err, msg):
    """
    Callback que se ejecuta cuando un mensaje falla.
    """
    if err is not None:
        print(f'Error al enviar el mensaje: {err}')

# Datos simulados de algunas ciuidades con su localización
cities = [
    {"id": 1, "city": "Madrid", "country": "Spain", "latitude": 40.4168, "longitude": -3.7038},
    {"id": 2, "city": "Alcalá de Henares", "country": "Spain", "latitude": 40.4810, "longitude": -3.3650},
    {"id": 3, "city": "Getafe", "country": "Spain", "latitude": 40.3084, "longitude": -3.7321},
    {"id": 4, "city": "Alcorcón", "country": "Spain", "latitude": 40.3451, "longitude": -3.8286},
    {"id": 5, "city": "Fuenlabrada", "country": "Spain", "latitude": 40.2893, "longitude": -3.8012},
    {"id": 6, "city": "Leganés", "country": "Spain", "latitude": 40.3081, "longitude": -3.7680},
    {"id": 7, "city": "Móstoles", "country": "Spain", "latitude": 40.3165, "longitude": -3.8667},
    {"id": 8, "city": "Pozuelo de Alarcón", "country": "Spain", "latitude": 40.4503, "longitude": -3.8067},
    {"id": 9, "city": "San Sebastián de los Reyes", "country": "Spain", "latitude": 40.5486, "longitude": -3.6344},
    {"id": 10, "city": "Tres Cantos", "country": "Spain", "latitude": 40.6204, "longitude": -3.7439},
    {"id": 11, "city": "Rivas-Vaciamadrid", "country": "Spain", "latitude": 40.3404, "longitude": -3.5539},
    {"id": 12, "city": "Barcelona", "country": "Spain", "latitude": 41.3851, "longitude": 2.1734},
    {"id": 13, "city": "Valencia", "country": "Spain", "latitude": 39.4699, "longitude": -0.3763},
    {"id": 14, "city": "Sevilla", "country": "Spain", "latitude": 37.3891, "longitude": -5.9845},
    {"id": 15, "city": "Bilbao", "country": "Spain", "latitude": 43.2630, "longitude": -2.9340},
    {"id": 16, "city": "Zaragoza", "country": "Spain", "latitude": 41.6488, "longitude": -0.8891},
    {"id": 17, "city": "Malaga", "country": "Spain", "latitude": 36.7213, "longitude": -4.4217},
    {"id": 18, "city": "Granada", "country": "Spain", "latitude": 37.1773, "longitude": -3.5986},
    {"id": 19, "city": "Alicante", "country": "Spain", "latitude": 38.3452, "longitude": -0.4810},
    {"id": 20, "city": "Murcia", "country": "Spain", "latitude": 37.9835, "longitude": -1.1296},
    {"id": 21, "city": "Palma", "country": "Spain", "latitude": 39.5696, "longitude": 2.6502},
    {"id": 22, "city": "Córdoba", "country": "Spain", "latitude": 37.8882, "longitude": -4.7794},
    {"id": 23, "city": "Toledo", "country": "Spain", "latitude": 39.8628, "longitude": -4.0273},
    {"id": 24, "city": "Vigo", "country": "Spain", "latitude": 42.2406, "longitude": -8.7207},
    {"id": 25, "city": "Salamanca", "country": "Spain", "latitude": 40.9704, "longitude": -5.6635},
    {"id": 26, "city": "Oviedo", "country": "Spain", "latitude": 43.3613, "longitude": -5.8494},
    {"id": 27, "city": "Gijón", "country": "Spain", "latitude": 43.5322, "longitude": -5.6613},
    {"id": 28, "city": "San Sebastián", "country": "Spain", "latitude": 43.3183, "longitude": -1.9812},
    {"id": 29, "city": "Logroño", "country": "Spain", "latitude": 42.4668, "longitude": -2.4500},
    {"id": 30, "city": "Lleida", "country": "Spain", "latitude": 41.6162, "longitude": 0.6226},
    {"id": 31, "city": "Castellón de la Plana", "country": "Spain", "latitude": 39.9860, "longitude": -0.0513},
    {"id": 32, "city": "Badajoz", "country": "Spain", "latitude": 38.8793, "longitude": -6.9707},
    {"id": 33, "city": "Santiago de Compostela", "country": "Spain", "latitude": 42.8782, "longitude": -8.5448},
    {"id": 34, "city": "Tarragona", "country": "Spain", "latitude": 41.1189, "longitude": 1.2445},
    {"id": 35, "city": "Cádiz", "country": "Spain", "latitude": 36.5312, "longitude": -6.2919},
    {"id": 36, "city": "Valladolid", "country": "Spain", "latitude": 41.6523, "longitude": -4.7247},
    {"id": 37, "city": "Huelva", "country": "Spain", "latitude": 37.2610, "longitude": -6.9447},
    {"id": 38, "city": "León", "country": "Spain", "latitude": 42.5987, "longitude": -5.5671}
]

merchants = [
    {"name": "Tienda de Electrónica", "category": "Electrónica"},
    {"name": "Tienda de Informática", "category": "Electrónica"},
    {"name": "Tienda de Smartphones", "category": "Electrónica"},
    {"name": "Tienda de Videojuegos", "category": "Electrónica"},
    {"name": "Tienda de Electrodomésticos", "category": "Electrónica"},
    {"name": "Tienda de Muebles", "category": "Hogar y Decoración"},
    {"name": "Tienda de Decoración", "category": "Hogar y Decoración"},
    {"name": "Tienda de Iluminación", "category": "Hogar y Decoración"},
    {"name": "Tienda de Jardinería", "category": "Hogar y Decoración"},
    {"name": "Farmacia", "category": "Salud y Belleza"},
    {"name": "Perfumería", "category": "Salud y Belleza"},
    {"name": "Tienda de Cosmética", "category": "Salud y Belleza"},
    {"name": "Tienda de Juguetes", "category": "Juguetes y Ocio"},
    {"name": "Tienda de Manualidades", "category": "Juguetes y Ocio"},
    {"name": "Tienda de Disfraces", "category": "Juguetes y Ocio"},
    {"name": "Librería", "category": "Libros y Papelería"},
    {"name": "Tienda de Material de Oficina", "category": "Libros y Papelería"},
    {"name": "Tienda de Revistas", "category": "Libros y Papelería"},
    {"name": "Tienda de Arte y Dibujo", "category": "Libros y Papelería"},
    {"name": "Tienda de Mochilas y Maletas", "category": "Libros y Papelería"},
    {"name": "Restaurante", "category": "Comida"},
    {"name": "Cafetería", "category": "Comida"},
    {"name": "Pizzería", "category": "Comida"},
    {"name": "Hamburguesería", "category": "Comida"},
    {"name": "Tienda de Ropa", "category": "Moda"},
    {"name": "Zapatería", "category": "Moda"},
    {"name": "Tienda de Deportes", "category": "Moda"}
]

# Función para generar una transacción simulada
def generate_transaction():
    """
    Genera una transacción simulada con datos aleatorios y aplanada.
    """
    user_id = f"user_{random.randint(100000, 999999)}"
    transaction_id = f"txn_{uuid.uuid4()}"
    timestamp = (datetime.now(pytz.timezone('Europe/Madrid')).replace(second=random.randint(0, 59)).strftime('%Y-%m-%dT%H:%M:%SZ'))
    amount = round(random.uniform(10.0, 500.0), 2)
    merchant = random.choice(merchants)
    city = random.choice(cities)

    # Aplanar el JSON
    transaction = {
        "transactionId": transaction_id,
        "userId": user_id,
        "timestamp": timestamp,
        "amount": amount,
        "currency": "EUR",
        "transactionType": "purchase",
        "merchantName": merchant["name"],  
        "merchantCategory": merchant["category"], 
        "paymentMethod": random.choice(["credit_card", "debit_card", "paypal"]),
        "status": random.choice(["completed", "pending", "failed"]),
        "deviceType": random.choice(["mobile", "desktop"]),  
        "deviceOs": random.choice(["iOS", "Android", "Windows"]), 
        "deviceIpAddress": f"192.168.1.{random.randint(1, 255)}",  
        "idCity": city["id"], 
        "userLocationCity": city["city"], 
        "userLocationCountry": city["country"],  
        "userLocationLatitude": city["latitude"],  
        "userLocationLongitude": city["longitude"]  
    }

    print(f"Generated transaction: {json.dumps(transaction, indent=4)}")

    return transaction

# Contadores para los estados de las transacciones
status_counters = {
    "completed": 0,
    "pending": 0,
    "failed": 0
}

# Enviar transacciones a Event Hubs
try:
    for _ in range(random.randint(50, 2000)):  # Envía 50-200 transacciones
        transaction = generate_transaction()
        producer.produce(
            topic=topic_name,  # Nombre del Event Hub
            value=json.dumps(transaction),  # Convertir la transacción a JSON
            callback=delivery_report  # Callback para confirmar la entrega
        )

        # Actualizar el contador de estados
        status = transaction["status"]
        status_counters[status] += 1

    # Asegurarse de que todos los mensajes se envíen
    producer.flush()

    # Imprimir el resumen de estados
    print("\nResumen de estados de las transacciones:")
    print(f"Completadas: {status_counters['completed']}")
    print(f"Pendientes: {status_counters['pending']}")
    print(f"Fallidas: {status_counters['failed']}")
    total_transacciones = status_counters['completed'] + status_counters['pending'] + status_counters['failed']
    print(f"Total de transacciones: {total_transacciones}")

except Exception as e:
    print(f"Error: {e}")
