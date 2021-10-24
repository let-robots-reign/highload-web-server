import logging
import socket
import uvloop
import asyncio
from multiprocessing import Process
import coloredlogs
from config import Config
from server.spawner import Spawner


def main():
    coloredlogs.install(
        level=Config.log_level,
        fmt=Config.log_format,
        datefmt=Config.log_date_format,
    )
    # uvloop makes event loop more efficient
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    logging.info('Starting webserver')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((Config.addr, Config.port))
    server_socket.listen(Config.max_connections)
    server_socket.setblocking(False)

    logging.info(f'Webserver started on {Config.addr}:{Config.port}')
    logging.info(f'Serving from {Config.base_dir}/')
    spawned_processes = []
    for i in range(Config.workers_process_amount):
        spawner = Spawner(server_socket, i)
        spawner_process = Process(target=spawner.start)
        spawned_processes.append(spawner_process)
        spawner_process.start()

    try:
        for spawner_process in spawned_processes:
            spawner_process.join()
    except KeyboardInterrupt:
        for spawner_process in spawned_processes:
            spawner_process.terminate()
        server_socket.close()
        logging.info('Webserver stopped by user')


if __name__ == "__main__":
    main()
