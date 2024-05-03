from rich.console import Console
from rich.table import Table
import psutil
import time
import os
from collections import deque

# Solicita el PID el cual quieres monitorear
pid = int(input("Por favor, introduce el PID el cual quieres monitorear: "))

# Inicializa las variables para almacenar los usos máximos
max_cpu_usage = 0
max_memory_usage = 0

# Inicializa una cola para almacenar las últimas 15 direcciones IP
ip_queue = deque(maxlen=15)

console = Console()  # Crea una nueva instancia de Console
os.system('cls')  # Limpia la consola completamente

while True:
    # Crea la tabla de métricas
    metrics_table = Table()
    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")

    current_cpu_usage = psutil.cpu_percent()  # Obtiene el uso de la CPU del sistema
    current_memory_usage = None
    try:
        process = psutil.Process(pid)
        current_memory_usage = process.memory_info().rss / 1024 / 1024

        # Actualiza los usos máximos si es necesario
        max_cpu_usage = max(max_cpu_usage, current_cpu_usage)
        max_memory_usage = max(max_memory_usage, current_memory_usage)
    except psutil.NoSuchProcess:
        metrics_table.add_row("Error", f"No se está ejecutando ningún proceso con el ID {pid}.")

    if current_cpu_usage is not None and current_memory_usage is not None:
        metrics_table.add_row("Uso actual de CPU", f"{current_cpu_usage}%")
        metrics_table.add_row("Uso máximo de CPU", f"{max_cpu_usage}%")
        metrics_table.add_row("Uso actual de memoria", f"{current_memory_usage} MB")
        metrics_table.add_row("Uso máximo de memoria", f"{max_memory_usage} MB")

    # Crea la tabla de direcciones IP
    ip_table = Table()
    ip_table.add_column("Últimas 15 direcciones IP")

    # Obtiene las conexiones de red del PID
    try:
        connections = process.connections()
    except psutil.NoSuchProcess:
        connections = []

    # Filtra las direcciones IP únicas y las añade a la cola
    for connection in connections:
        if connection.raddr:
            ip = connection.raddr.ip
            if ip not in ip_queue:
                ip_queue.appendleft(ip)

    # Añade las direcciones IP de la cola a la tabla
    for ip in ip_queue:
        ip_table.add_row(ip)

    console.clear()  # Limpia la consola antes de imprimir las tablas
    console.print(metrics_table)  # Imprime la tabla de métricas
    console.print(ip_table)  # Imprime la tabla de direcciones IP

    time.sleep(0.3)  # Espera 0.3 segundos
