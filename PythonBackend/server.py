import datetime
import logging
import os
import sys
from concurrent import futures

import calc_service_pb2
import calc_service_pb2_grpc
import grpc
from calculation_handler import CalcHandler

LOGGER = logging.getLogger(__name__)
LISTEN_PORT = os.getenv("LISTEN_PORT", 9000)
ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = 1  # some bug in grpc
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
        image = self.calc_handler.get_impact(request.ModelName, request.Data, request.Feature, request.Head,
                                             request.Tail)
        return calc_service_pb2.ImpactReply(Image=image)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_PROCESS_COUNT))
    calc_service_pb2_grpc.add_CalcServiceServicer_to_server(Handler(), server)
    server.add_insecure_port('[::]:{}'.format(LISTEN_PORT))
    server.start()
    LOGGER.info('server started')
    server.wait_for_termination()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)
    main()
