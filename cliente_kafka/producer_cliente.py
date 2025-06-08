import confluent_kafka as ck
import json
import uuid
import consumer_cliente as cc
import time

# Metodo que se encarga de generar el productor de Kafka
def generar_producer():
    config = {"bootstrap.servers": "localhost:9092"}
    return ck.Producer(config)

# Metodo que muestra el menú de operaciones disponibles
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

# Metodo que recoge los operandos de la operación
def obtener_operandos():
    while True:
        try:
            op1 = float(input("Introduce el primer operando: "))
            op2 = float(input("Introduce el segundo operando: "))
            return op1, op2
        except ValueError:
            print("Por favor, introduce números válidos.")

# Metodo principal que ejecuta la aplicación
def main():
    producer = generar_producer()
    topic = "calculadora"  # Topic donde se enviarán las solicitudes
    n = 0
    
    while True:
        # Se muestra el menu
        opcion = mostrar_menu()
        
        if opcion == 5:
            print("Saliendo...")
            break
        
        # Se asigna la operación elegida y los operandos
        operaciones = {1: "sum", 2: "sub", 3: "mult", 4: "div"}
        operacion = operaciones[opcion]        
        print(f"\nOperación seleccionada: {operacion}")
        op1, op2 = obtener_operandos()
        
        # Generar un ID único para esta operación
        n+=1
        operacion_id = str(f"{operacion}{n}")
        
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

        # Esperamos la respuesta
        print(f"Esperando resultado para la operación: {op1} {operacion} {op2}...\n")
        data=cc.esperar_mensaje(operacion_id)
        print("Respuesta recibida.\n")
        if data["status"]==True:
            print(f"Resultado de la operacion con ID {data['id']} es: {data['result']}")
        else:
            print(f"Error del servidor: {data['error']}") 


if __name__ == "__main__":
    main()