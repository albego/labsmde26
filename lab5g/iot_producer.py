import time
import random
import json
from datetime import datetime
from confluent_kafka import Producer

# ==========================================
# CONFIGURACIÓN KAFKA / AZURE EVENT HUBS
# ==========================================
# Sustituir @ por el valor de tu configuración
topic_name = '@'
bootstrap_servers = '@.servicebus.windows.net:9093'  # Endpoint de Event Hubs
sasl_password = 'Endpoint=sb://@.servicebus.windows.net/;SharedAccessKeyName=Send;SharedAccessKey=@'  # Cadena de conexión SASL

conf = {
    'bootstrap.servers': bootstrap_servers,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '$ConnectionString',
    'sasl.password': sasl_password,
    'client.id': 'python-sensor-producer'
}

producer = Producer(**conf)

def delivery_report(err, msg):
    """Callback de confirmación de entrega. Registra errores si los hay."""
    if err is not None:
        print(f'Error al enviar el mensaje: {err}')

# ==========================================
# DATOS DE SENSORES Y LÓGICA DE PAYLOAD
# ==========================================
SENSORES_ACTUALES = [
    {"ID_Sensor": "S_001", "Latitud": 40.3977, "Longitud": -3.6565},
    {"ID_Sensor": "S_002", "Latitud": 40.4283, "Longitud": -3.7141},
    {"ID_Sensor": "S_003", "Latitud": 40.4384, "Longitud": -3.7711},
    {"ID_Sensor": "S_004", "Latitud": 40.4216, "Longitud": -3.7534},
    {"ID_Sensor": "S_005", "Latitud": 40.4077, "Longitud": -3.6233},
    {"ID_Sensor": "S_006", "Latitud": 40.4194, "Longitud": -3.7519},
    {"ID_Sensor": "S_007", "Latitud": 40.3584, "Longitud": -3.6812},
    {"ID_Sensor": "S_008", "Latitud": 40.3876, "Longitud": -3.623},
    {"ID_Sensor": "S_009", "Latitud": 40.4636, "Longitud": -3.7092},
    {"ID_Sensor": "S_010", "Latitud": 40.3703, "Longitud": -3.779},
    {"ID_Sensor": "S_011", "Latitud": 40.4154, "Longitud": -3.6817},
    {"ID_Sensor": "S_012", "Latitud": 40.3953, "Longitud": -3.7008},
    {"ID_Sensor": "S_013", "Latitud": 40.4674, "Longitud": -3.7165},
    {"ID_Sensor": "S_014", "Latitud": 40.352, "Longitud": -3.7513},
    {"ID_Sensor": "S_015", "Latitud": 40.3429, "Longitud": -3.6482},
    {"ID_Sensor": "S_016", "Latitud": 40.4648, "Longitud": -3.7637},
    {"ID_Sensor": "S_017", "Latitud": 40.4278, "Longitud": -3.72},
    {"ID_Sensor": "S_018", "Latitud": 40.4665, "Longitud": -3.6761},
    {"ID_Sensor": "S_019", "Latitud": 40.4447, "Longitud": -3.621},
    {"ID_Sensor": "S_020", "Latitud": 40.435, "Longitud": -3.716},
    {"ID_Sensor": "S_021", "Latitud": 40.4292, "Longitud": -3.7299},
    {"ID_Sensor": "S_022", "Latitud": 40.3645, "Longitud": -3.6448},
    {"ID_Sensor": "S_023", "Latitud": 40.4062, "Longitud": -3.6819},
    {"ID_Sensor": "S_024", "Latitud": 40.3742, "Longitud": -3.644},
    {"ID_Sensor": "S_025", "Latitud": 40.4359, "Longitud": -3.6689},
    {"ID_Sensor": "S_026", "Latitud": 40.4843, "Longitud": -3.7532},
    {"ID_Sensor": "S_027", "Latitud": 40.4189, "Longitud": -3.7263},
    {"ID_Sensor": "S_028", "Latitud": 40.3833, "Longitud": -3.6452},
    {"ID_Sensor": "S_029", "Latitud": 40.4842, "Longitud": -3.7639},
    {"ID_Sensor": "S_030", "Latitud": 40.4323, "Longitud": -3.6695}
]

CONTAMINANTES = ["O3", "NO2", "PM2.5", "CO2"]

def generar_evento(sensor):
    """Genera una lectura simulada para un sensor concreto."""
    if random.random() < 0.10:
        valor_ppm = "0.00"  # 10% de las veces el sensor falla y reporta 0
    else:
        valor_ppm = str(round(random.uniform(120.0, 450.0), 2))

    bateria = f"{random.randint(10, 90)}"

    evento = {
        "ID_Sensor": sensor["ID_Sensor"],
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Tipo_Contaminante": random.choice(CONTAMINANTES),
        "Valor_PPM": valor_ppm,
        "Latitud": str(sensor["Latitud"]),
        "Longitud": str(sensor["Longitud"]),
        "Estado_Bateria": bateria
    }
    
    return evento

# ==========================================
# EJECUCIÓN DEL ENVÍO INFINITO
# ==========================================
if __name__ == "__main__":
    print(f"Iniciando envío de eventos al Event Hub '{topic_name}'... Pulsa Ctrl+C para detener.")
    
    try:
        mensajes_enviados = 0
        while True:
            # Elegimos un sensor al azar de la lista
            sensor_elegido = random.choice(SENSORES_ACTUALES)
            
            # Generamos su lectura
            nuevo_evento = generar_evento(sensor_elegido)
            
            # Imprimimos por pantalla para ver qué estamos enviando
            print(f"Enviando evento: {json.dumps(nuevo_evento)}")
            
            # Enviar a Kafka / Event Hubs
            producer.produce(
                topic=topic_name,
                value=json.dumps(nuevo_evento).encode('utf-8'),  # Codificamos a bytes
                callback=delivery_report
            )
            
            producer.poll(0)
            
            mensajes_enviados += 1
            
            # Esperamos entre 0.5 y 1.5 segundos para no saturar y darle ritmo "realista"
            time.sleep(random.uniform(0.5, 1.5))
            
    except KeyboardInterrupt:
        print("\nSimulación detenida por el usuario.")
    except Exception as e:
        print(f"\nError fatal: {e}")
    finally:
        # Asegurarse de que todos los mensajes pendientes se envíen antes de cerrar
        print(f"Vaciando buffer de mensajes (enviados hasta ahora: {mensajes_enviados})...")
        producer.flush()
        print("Productor cerrado correctamente.")
