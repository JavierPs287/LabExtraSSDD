import confluent_kafka as ck
import json
import producer_servidor as ps

config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "calculadora",
}

consumer = ck.Consumer(config)

while True:
    print("Esperando mensaje...")
    consumer.subscribe(["calculadora"])
    mensaje = consumer.poll(1.0)

    if mensaje is None:
        continue

    try:
        data=json.loads(mensaje.value().decode("utf-8"))
        formato=False
        formato= (
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