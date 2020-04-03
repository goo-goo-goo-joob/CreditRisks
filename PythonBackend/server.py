import contextlib
import datetime
import logging
import multiprocessing
import os
import socket
import sys
import time
from concurrent import futures

import grpc

import calc_service_pb2
import calc_service_pb2_grpc
from calculation_handler import CalcHandler

LOGGER = logging.getLogger(__name__)
LISTEN_PORT = os.getenv("LISTEN_PORT", 9000)
ONE_DAY = datetime.timedelta(days=1)
if sys.platform.startswith('linux'):
    _PROCESS_COUNT = int(os.getenv("PROCESS_COUNT", multiprocessing.cpu_count()))
elif sys.platform.startswith('win32'):
    _PROCESS_COUNT = 1
else:
    raise Exception("Unsupported OS")
_MODEL_PATH = os.getenv("MODEL_PATH")


class Handler(calc_service_pb2_grpc.CalcServiceServicer):
    def __init__(self):
        self.calc_handler = CalcHandler(_MODEL_PATH)
        print("SERVER READY")

    def CalcProbability(self, request, context):
        result = self.calc_handler.calc_probability(request.Params)
        return calc_service_pb2.CalcReply(Result=result)

    def GetModelInfo(self, request, context):
        result = self.calc_handler.get_plots(request.ModelName)
        return calc_service_pb2.ModelInfoReply(Result=result)

    def GetImpact(self, request, context):
        image = self.calc_handler.get_impact(request.ModelName, request.Data, request.Feature, request.Head, request.Tail)
        return calc_service_pb2.ImpactReply(Image=image)


def _wait_forever(server):
    try:
        while True:
            time.sleep(ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


def _run_server(bind_address):
    """Start a server in a subprocess."""
    LOGGER.info('Starting new server.')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_PROCESS_COUNT), options=(('grpc.so_reuseport', 1),))
    calc_service_pb2_grpc.add_CalcServiceServicer_to_server(Handler(), server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server)


@contextlib.contextmanager
def _reserve_port():
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if sys.platform.startswith('linux'):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
            raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', LISTEN_PORT))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()


def main():
    with _reserve_port() as port:
        bind_address = '[::]:{}'.format(port)
        LOGGER.info("Binding to '%s'", bind_address)
        sys.stdout.flush()
        workers = []
        for _ in range(_PROCESS_COUNT):
            worker = multiprocessing.Process(target=_run_server, args=(bind_address,))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)
    main()
