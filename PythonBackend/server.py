import logging
import os
import random
import time
from concurrent import futures

import grpc

import calc_service_pb2
import calc_service_pb2_grpc
from calc_model import RandomModel

LISTEN_ADDR = os.getenv("LISTEN_ADDR", "[::]:9000")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))


class Handler(calc_service_pb2_grpc.CalcServiceServicer):
    model = None

    def __init__(self):
        self.model = RandomModel('test_data/data.zip')

    def CalcProbability(self, request, context):
        return calc_service_pb2.CalcReply(Probability=self.model.predict_proba(request))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    calc_service_pb2_grpc.add_CalcServiceServicer_to_server(Handler(), server)
    server.add_insecure_port(LISTEN_ADDR)
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
