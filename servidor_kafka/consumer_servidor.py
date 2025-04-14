import confluent_kafka as ck
import json
import producer_servidor as ps

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "calculadora",
    "auto.offset.reset": "earliest"
}

consumer = ck.Consumer(config)
consumer.subscribe(["calculadora"])

while True:
    print("Esperando mensaje...")
    mensajes = consumer.consume(num_messages=1, timeout=1.0)

    if not mensajes:
        continue

    mensaje = mensajes[0]

    if mensaje.error():
        print("Error en el mensaje:", mensaje.error())
        continue

    try:
        data = json.loads(mensaje.value().decode("utf-8"))
        formato = (
            "id" in data and
            "operation" in data and
            "args" in data and
            "op1" in data["args"] and
            "op2" in data["args"]
        )
        if formato:
            ps.procesar_acierto(data)
        else:
            ps.procesar_fallo(data)

    except json.JSONDecodeError:
        print("Error decoding JSON")
