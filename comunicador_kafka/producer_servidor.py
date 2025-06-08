import confluent_kafka as ck
import json
import Ice
import RemoteCalculator as rc

# Funcion que genera el productor que envia los mensajes al cliente
def generar_producer():
    config = {"bootstrap.servers": "localhost:9092"}
    return ck.Producer(config)

# Funcion que crea el mensaje json a enviar
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

# Metodo que procesa los mensaje json con formato correcto
def procesar_acierto(proxy,data):
    print("Procesando: ")
    producer = generar_producer()
    # Desglosamos el json
    id = data["id"]
    operacion = data["operation"]
    op1 = data["args"]["op1"]
    op2 = data["args"]["op2"]
    
    try:
        # Iniciamos el comunicador de ice
        communicator = Ice.initialize()
        str_proxy = proxy
        proxy = communicator.stringToProxy(str_proxy)
        calculator = rc.CalculatorPrx.checkedCast(proxy)

        # Intentamos realizar la operacion
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
            try :
                resultado = calculator.div(op1, op2)
            except rc.ZeroDivisionError:
                # Si se intenta dividir entre 0, se recibe una excepcion
                mensaje = crear_mensaje(id, False, "No es posible dividir entre 0")
                mensaje_str = json.dumps(mensaje)
                producer.produce("resultados", value=mensaje_str.encode("utf-8"))
                producer.flush()
                print("Mensaje enviado")
                return
        else:
            # Si la operacion no es correcta, se envia un mensaje de error
            mensaje = crear_mensaje(id, False, "Operacion no encontrada")
            mensaje_str = json.dumps(mensaje)
            producer.produce("resultados", value=mensaje_str.encode("utf-8"))
            producer.flush()
            print("Mensaje enviado")
            return

        # Si la operacion se realiza correctamente, se envia el resultado
        mensaje = crear_mensaje(id, True, resultado=resultado)
        print("Resultado: ", resultado)
        mensaje_str = json.dumps(mensaje)
        producer.produce("resultados", value=mensaje_str.encode("utf-8"))
        producer.flush()
        print("Mensaje enviado")

    except Exception as e:
        # Si ocurre un error en la conexion, se envia mensaje de error y se termina la ejecucion
        mensaje = crear_mensaje(id, False, f"Error interno: {str(e)}\nCerrando consumer...")
        mensaje_str = json.dumps(mensaje)
        producer.produce("resultados", value=mensaje_str.encode("utf-8"))
        producer.flush()
        print(f"Error: {str(e)}")
        exit(1)

# Metodo para procesar los mensajes con formato incorrecto (si existe un id)
def procesar_fallo(data):
    print("Procesando fallo: ")
    producer = generar_producer()

    if "id" not in data:
        return
    
    id = data["id"]
    mensaje = crear_mensaje(id, False, "Formato de mensaje incorrecto")
    mensaje_str = json.dumps(mensaje)
    producer.produce("resultados", mensaje_str.encode("utf-8"))
    producer.flush()