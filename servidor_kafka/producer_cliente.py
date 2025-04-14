import confluent_kafka as ck
import json
import uuid
import consumer_cliente as cc
import time

def generar_producer():
    config = {"bootstrap.servers": "localhost:9092"}
    return ck.Producer(config)

def mostrar_menu():
    print("\nCalculadora remota - Elige una operación:")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Salir")
    
    while True:
        try:
            opcion = int(input("Selecciona una opción (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print("Por favor, introduce un número entre 1 y 5")
        except ValueError:
            print("Entrada inválida. Introduce un número.")

def obtener_operandos():
    while True:
        try:
            op1 = float(input("Introduce el primer operando: "))
            op2 = float(input("Introduce el segundo operando: "))
            return op1, op2
        except ValueError:
            print("Por favor, introduce números válidos.")

def main():
    producer = generar_producer()
    topic = "calculadora"  # Topic donde se enviarán las solicitudes
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == 5:
            print("Saliendo...")
            break
        
        operaciones = {1: "sum", 2: "sub", 3: "mult", 4: "div"}
        operacion = operaciones[opcion]
        
        print(f"\nOperación seleccionada: {operacion}")
        op1, op2 = obtener_operandos()
        
        # Generar un ID único para esta operación
        operacion_id = str(uuid.uuid4())
        
        # Construir el mensaje
        mensaje = {
            "id": operacion_id,
            "operation": operacion,
            "args": {
                "op1": op1,
                "op2": op2
            }
        }
        
        # Enviar el mensaje
        producer.produce(topic, value=json.dumps(mensaje).encode('utf-8'))
        producer.flush()
        
        print(f"\nSolicitud enviada con ID: {operacion_id}")
        print(f"Esperando resultado para la operación: {op1} {operacion} {op2}...\n")
        time.sleep(15)
        data=cc.esperar_mensaje(operacion_id)
        print("Resultado recibido.\n")
        print(f"Resultado de la operacion con ID {data['id']} es: {data['result']}")


if __name__ == "__main__":
    main()