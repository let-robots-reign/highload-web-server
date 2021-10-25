import logging
import pathlib

TEST_DIR = '/http-test-suite'


class Config:
    base_dir = str(pathlib.Path().absolute()) + TEST_DIR
    index_filename = 'index.html'

    # CONNECTION
    addr = '0.0.0.0'
    port = 3000
    max_connections = 100
    bytes_per_recv = 1024
    bytes_per_send = 1024

    # WORKERS
    workers_process_amount = 4

    # LOGGING
    log_level = logging.DEBUG
    log_format = '%(asctime)s %(levelname)s\t%(name)s[%(process)d]  \t%(message)s'
    log_date_format = '%H:%M:%S'

    log_spawner_verbose = False
    log_worker_verbose = False
