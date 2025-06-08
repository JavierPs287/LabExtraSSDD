import json
import confluent_kafka as ck

# Creamos el consumer que recibe la respuesta
def generar_consumer():
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "calculadora-respuestas",
        "auto.offset.reset": "earliest"
    }
    return ck.Consumer(config)

# Metodo que espera un mensaje del topic "resultados" y devuelve el resultado
def esperar_mensaje(id):
    consumer = generar_consumer()
    consumer.subscribe(["resultados"])
    print("Esperando mensaje...")

    while True:
        # Bucle que espera un mensaje
        mensajes = consumer.consume(num_messages=1, timeout=1.0)

        if not mensajes:
            continue

        mensaje = mensajes[0]

        if mensaje.error():
            print("Error en el mensaje:", mensaje.error())
            continue

        try:
            # Decodifica el mensaje y verifica el ID
            data = json.loads(mensaje.value().decode("utf-8"))
            if data["id"] == id:
                # Si el ID coincide, devolvemos el resultado
                return data
            else:
                # Si el ID no coincide, seguimos esperando
                print("ID no coincide. Esperando el mensaje correcto...")
        except json.JSONDecodeError:
            print("Error decoding JSON")