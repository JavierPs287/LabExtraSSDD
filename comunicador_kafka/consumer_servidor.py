import confluent_kafka as ck
import json
import producer_servidor as ps

# Configuramos el consumidor de apache kafka en localhost, en el grupo calculadora
config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "calculadora",
    "auto.offset.reset": "earliest"
}

# Creamos el consumidor y lo inicializamos en el canal "calculadora"
consumer = ck.Consumer(config)
consumer.subscribe(["calculadora"])
proxy = str(input("Introduce el str del proxy: "))
print("Esperando mensaje...")

while True:
    # Lo ponemos a escuchar, con un timeout de 1 segundo
    mensajes = consumer.consume(num_messages=1, timeout=1.0)

    # Si no se recibe nada seguimos
    if not mensajes:
        continue
    
    # Si se recibe un mensaje, lo procesamos
    mensaje = mensajes[0]

    # Si el mensaje tiene error, lo mostramos y seguimos
    if mensaje.error():
        print("Error en el mensaje:", mensaje.error())
        continue
    
    # Si el mensaje es correcto, lo procesamos
    try:
        # Decodificamos el mensaje  
        data = json.loads(mensaje.value().decode("utf-8"))
        formato = (
            "id" in data and
            "operation" in data and
            "args" in data and
            "op1" in data["args"] and
            "op2" in data["args"]
        )
        # Si cumple con el formato de la orden, lo procesamos como correcto
        if formato:
            ps.procesar_acierto(proxy,data)
        # Si no cumple con el formato, lo procesamos como fallo
        else:
            ps.procesar_fallo(data)

    except json.JSONDecodeError:
        # Si al decodificar el mensaje no es formato json, salta error
        print("Error decoding JSON")
