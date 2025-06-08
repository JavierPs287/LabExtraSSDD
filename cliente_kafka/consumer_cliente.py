import json
import confluent_kafka as ck

def generar_consumer():
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "calculadora-respuestas",
        "auto.offset.reset": "earliest"
    }
    return ck.Consumer(config)

def esperar_mensaje(id):
    consumer = generar_consumer()
    consumer.subscribe(["resultados"])
    print("Esperando mensaje...")

    while True:
        mensajes = consumer.consume(num_messages=1, timeout=1.0)

        if not mensajes:
            continue

        mensaje = mensajes[0]

        if mensaje.error():
            print("Error en el mensaje:", mensaje.error())
            continue

        try:
            data = json.loads(mensaje.value().decode("utf-8"))
            if data["id"] == id:
                return data
            else:
                print("ID no coincide. Esperando el mensaje correcto...")
        except json.JSONDecodeError:
            print("Error decoding JSON")