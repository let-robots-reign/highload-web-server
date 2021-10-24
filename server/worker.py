import asyncio
import logging
from utils.request import Request
from utils.response import Response
from config import Config
import os.path


async def perform_task(client_socket, worker_name):
    """
    Корутина для формирования request и отправки response.
    Должна передаваться в create_task в событийном цикле asyncio
    :param client_socket: объект сокета
    :param worker_name: название воркера, используется в логах
    :return:
    """
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
    ends_on_slash = request.url.endswith('/')
    slash_after_filename = ends_on_slash and '.' in request.url.split('/')[-2]
    if ends_on_slash:
        filepath += Config.index_filename
    file_exists = os.path.exists(filepath)

    # CREATE RESPONSE

    status, path = 200, None
    if request.method not in ['GET', 'HEAD']:
        status = 405
    elif slash_after_filename:
        status = 404
    elif '/..' in request.url or (ends_on_slash and not file_exists):
        status = 403
    elif (not file_exists) or (not request.is_valid):
        status = 404
    else:
        path = filepath

    response = Response(method=request.method, protocol=request.protocol, status=status, filepath=path)

    logging.info(f'WORKER {worker_name}: {response.status} {request.method} {request.url}')

    # SEND RESPONSE
    await response.send(client_socket)

    # END WORKER
    client_socket.close()

    if Config.log_worker_verbose:
        logging.debug(f'WORKER {worker_name}: closed client socket')
    if Config.log_worker_verbose:
        logging.debug(f'WORKER {worker_name}: finished job')
