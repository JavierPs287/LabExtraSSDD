import confluent_kafka as ck
import json
import Ice
import RemoteCalculator as rc

def generar_producer():
    config = {"bootstrap.servers": "localhost:9092"}
    return ck.Producer(config)



def procesar_acierto(data):
    print("Procesando: ")
    producer=generar_producer()
    id=data["id"]
    operacion=data["operation"]
    op1=data["args"]["op1"]
    op2=data["args"]["op2"]
    communicator=Ice.initialize()
    str_proxy="calculator -t -e 1.1:tcp -h 192.168.1.37 -p 10000 -t 60000:tcp -h 172.18.0.1 -p 10000 -t 60000:tcp -h 172.17.0.1 -p 10000 -t 60000" #De momento es fijo, pero habra que cambiarlo"
    proxy=communicator.stringToProxy(str_proxy)
    calculator=rc.CalculatorPrx.checkedCast(proxy)
    if operacion=="sum":
        resultado=calculator.sum(op1,op2)
        print("Suma")
    elif operacion=="sub":
        resultado=calculator.sub(op1,op2)
        print("Resta")
    elif operacion=="mult":
        resultado=calculator.mult(op1,op2)
        print("Multiplicacion")
    elif operacion=="div":
        if op2!=0:
            resultado=calculator.div(op1,op2)
            print("Division")
        else:
            mensaje = {
                "id": str(id),
                "status": False,
                "error": "No es posible dividir entre 0"
            }
            print("Division entre 0")
                
            mensaje_json = json.dumps(mensaje)
            producer.produce(id, value=mensaje_json.encode("utf-8"))
            producer.flush()
            print("Mensaje enviado")
            return

    #No existe la operacion    
    else:
        mensaje = {
            "id": str(id),
            "status": False,
            "error": "operation not found"
        }
        print("Operacion no encontrada")
            
        mensaje_json = json.dumps(mensaje)
        producer.produce(id, value=mensaje_json.encode("utf-8"))
        producer.flush()
        print("Mensaje enviado")
        return
    
    #La operacion existe y se obtiene resultado
    mensaje = {
        "id": str(id),
        "status": True,
        "result": resultado
    }
    print("Resultado: ", resultado)
        
    mensaje_json = json.dumps(mensaje)
    producer.produce(id, value=mensaje_json.encode("utf-8"))
    producer.flush()
    print("Mensaje enviado")



def procesar_fallo(data):
    print("Procesando: ")
    producer=generar_producer()

    if "id" not in data:
        return
    
    id=data["id"]

    mensaje = {
        "id": str(id),
        "status": False,
        "error": "wrong format"
    }

    mensaje_json = json.dumps(mensaje)
    producer.produce(id, mensaje_json.encode("utf-8"))
    producer.flush()