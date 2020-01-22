import logging
import os
import time
from concurrent import futures

import grpc
import pandas as pd

import calc_service_pb2
import calc_service_pb2_grpc
from calc_model import get_models

LISTEN_ADDR = os.getenv("LISTEN_ADDR", "[::]:9000")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))


class Handler(calc_service_pb2_grpc.CalcServiceServicer):
    models = None

    def __init__(self):
        self.models = get_models(host=os.getenv("DB_HOST"),
                                 port=int(os.getenv("DB_PORT")),
                                 user=os.getenv("DB_USER"),
                                 password=os.getenv("DB_PASSWORD"),
                                 database=os.getenv("DB_DATABASE"))

    def CalcProbability(self, request, context):
        df = pd.DataFrame.from_dict(request.Params, orient='index')
        df = pd.DataFrame(pd.to_numeric(df[0], errors='coerce')).T
        result = {}
        for name, model in self.models.items():
            value = None
            try:
                value = model.predict_proba(df)
            except Exception as e:
                value = float('nan')
            finally:
                result[name] = value
        return calc_service_pb2.CalcReply(Result=result)

    def GetModelInfo(self, request, context):
        return calc_service_pb2.ModelInfoReply(Result=self.models[request.ModelName].plots)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS), options=(('grpc.so_reuseport', 0),))
    calc_service_pb2_grpc.add_CalcServiceServicer_to_server(Handler(), server)
    if server.add_insecure_port(LISTEN_ADDR) == 0:
        print('cannot bind port')
        exit(1)
    server.start()
    try:
        print('start serving')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
