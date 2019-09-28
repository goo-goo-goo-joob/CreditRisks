import logging
import random
import time
from concurrent import futures

import grpc

import calc_service_pb2
import calc_service_pb2_grpc


class Handler(calc_service_pb2_grpc.CalcServiceServicer):

    def CalcProbability(self, request, context):
        return calc_service_pb2.CalcReply(Probability=random.random())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calc_service_pb2_grpc.add_CalcServiceServicer_to_server(Handler(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
