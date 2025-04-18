import confluent_kafka as ck
import json
import Ice
import RemoteCalculator as rc

def generar_producer():
    config = {"bootstrap.servers": "localhost:9092"}
    return ck.Producer(config)

# Cambiamos el nombre de la función para evitar conflicto
def crear_mensaje(id, status, msg=None, resultado=None):
    mensaje = {
        "id": str(id),
        "status": status
    }
    if status:
        mensaje["result"] = resultado
    else:
        mensaje["error"] = msg
    return mensaje

def procesar_acierto(data):
    print("Procesando: ")
    producer = generar_producer()
    id = data["id"]
    operacion = data["operation"]
    op1 = data["args"]["op1"]
    op2 = data["args"]["op2"]
    
    try:
        communicator = Ice.initialize()
        str_proxy = "calculator -t -e 1.1:tcp -h 192.168.1.37 -p 10000 -t 60000:tcp -h 172.18.0.1 -p 10000 -t 60000:tcp -h 172.17.0.1 -p 10000 -t 60000"
        proxy = communicator.stringToProxy(str_proxy)
        calculator = rc.CalculatorPrx.checkedCast(proxy)

        if operacion == "sum":
            resultado = calculator.sum(op1, op2)
            print("Suma")
        elif operacion == "sub":
            resultado = calculator.sub(op1, op2)
            print("Resta")
        elif operacion == "mult":
            resultado = calculator.mult(op1, op2)
            print("Multiplicacion")
        elif operacion == "div":
            if op2 != 0:
                resultado = calculator.div(op1, op2)
                print("Division")
            else:
                mensaje = crear_mensaje(id, False, "No es posible dividir entre 0")
                mensaje_str = json.dumps(mensaje)
                producer.produce(id, value=mensaje_str.encode("utf-8"))
                producer.flush()
                print("Mensaje enviado")
                return
        else:
            mensaje = crear_mensaje(id, False, "Operacion no encontrada")
            mensaje_str = json.dumps(mensaje)
            producer.produce(id, value=mensaje_str.encode("utf-8"))
            producer.flush()
            print("Mensaje enviado")
            return

        # Operación exitosa
        mensaje = crear_mensaje(id, True, resultado=resultado)
        print("Resultado: ", resultado)
        mensaje_str = json.dumps(mensaje)
        producer.produce(id, value=mensaje_str.encode("utf-8"))
        producer.flush()
        print("Mensaje enviado")

    except Exception as e:
        mensaje = crear_mensaje(id, False, f"Error interno: {str(e)}")
        mensaje_str = json.dumps(mensaje)
        producer.produce(id, value=mensaje_str.encode("utf-8"))
        producer.flush()
        print(f"Error: {str(e)}")

def procesar_fallo(data):
    print("Procesando fallo: ")
    producer = generar_producer()

    if "id" not in data:
        return
    
    id = data["id"]
    mensaje = crear_mensaje(id, False, "Formato de mensaje incorrecto")
    mensaje_str = json.dumps(mensaje)
    producer.produce(id, mensaje_str.encode("utf-8"))
    producer.flush()