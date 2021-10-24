import asyncio
import logging
from config import Config
from .worker import perform_task


class Spawner:
    """
    "Фабрика" воркеров.
    Каждый воркер на пришедший запрос создает корутину perform_task из worker.py и обрабатывает запрос
    """
    def __init__(self, server_socket, spawner_id):
        self._server_socket = server_socket
        self._spawner_id = spawner_id
        self._loop = None

    def start(self):
        self._loop = asyncio.get_event_loop()

        logging.info(f'SPAWNER {self._spawner_id}: started')

        try:
            self._loop.run_until_complete(self._worker_spawner())
        except KeyboardInterrupt:
            logging.warning(f'SPAWNER {self._spawner_id}: stopped by user')

    async def _worker_spawner(self):
        worker_num = 0

        while True:
            if Config.log_spawner_verbose:
                logging.debug(f'SPAWNER {self._spawner_id}: awaiting data')

            client_socket, _ = await self._loop.sock_accept(self._server_socket)

            worker_name = f'{self._spawner_id}_{worker_num}'
            if Config.log_spawner_verbose:
                logging.debug(f'SPAWNER {self._spawner_id}: spawning worker {worker_name}')

            self._loop.create_task(perform_task(client_socket, worker_name))
            worker_num += 1
