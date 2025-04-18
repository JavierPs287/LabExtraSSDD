"""calculator server application."""

import logging
import Ice
import threading
import subprocess
import sys
import os

from calculator.calculator import Calculator
from calculator.producer_servidor import generar_producer

class Server(Ice.Application):
    """Ice.Application for the server."""

    def __init__(self) -> None:
        """Initialise the Server objects."""
        super().__init__()
        self.logger = logging.getLogger(__file__)
        self.kafka_producer = generar_producer()

    def run(self, args: list[str]) -> int:
        """Execute the main server actions."""
        # Iniciar el consumidor de Kafka en segundo plano
        self._start_kafka_consumer()
        
        servant = Calculator()
        adapter = self.communicator().createObjectAdapter("calculator")
        proxy = adapter.add(servant, self.communicator().stringToIdentity("calculator"))
        self.logger.info('Proxy: "%s"', proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

    def _start_kafka_consumer(self):
        """Inicia el consumer_servidor.py en un proceso separado."""
        consumer_path = os.path.join(os.path.dirname(__file__), 'consumer_servidor.py')
        subprocess.Popen([sys.executable, consumer_path])
        self.logger.info("Kafka consumer started in background")