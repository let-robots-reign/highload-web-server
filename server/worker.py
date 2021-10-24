import asyncio
import logging
from utils.request import Request
from utils.response import Response
from config import Config
import os.path


async def perform_task(client_socket, worker_name):
    if Config.log_worker_verbose:
        logging.debug(f'WORKER {worker_name} spawned')

    # GET REQUEST

    loop = asyncio.get_event_loop()
    request_raw = ''
    while True:
        encoded = await loop.sock_recv(client_socket, Config.bytes_per_recv)
        request_part = encoded.decode()
        request_raw += request_part
        if '\r\n' in request_raw or len(request_part) == 0:
            break

    request = Request(request_raw)

    # GET FILENAME

    filepath = Config.base_dir + request.url
    search_folder = request.url.endswith('/')
    filepath += Config.index_filename if search_folder else ''
    file_exists = os.path.exists(filepath)

    # CREATE RESPONSE
    status, filepath = 200, filepath if file_exists else None
    if request.method not in ['GET', 'HEAD']:
        status = 405
    elif '/..' in request.url or (search_folder and not file_exists):
        status = 403
    elif (not file_exists) or (not request.is_valid):
        status = 404

    response = Response(method=request.method, protocol=request.protocol, status=status, filepath=filepath)

    logging.info(f'WORKER {worker_name}: {response.status} {request.method} {request.url}')

    # SEND RESPONSE
    await response.send(client_socket)

    # END WORKER
    client_socket.close()

    if Config.log_worker_verbose:
        logging.debug(f'WORKER {worker_name}: closed client socket')
    if Config.log_worker_verbose:
        logging.debug(f'WORKER {worker_name}: finished job')
