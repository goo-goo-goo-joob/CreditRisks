from concurrent import futures
import time
import logging

import grpc

import calc_service_pb2_grpc
import calc_service_pb2


class Greeter(calc_service_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return calc_service_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calc_service_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
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
