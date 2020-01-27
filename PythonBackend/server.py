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
import numpy as np
import pandas as pd

import calc_service_pb2
import calc_service_pb2_grpc
import feature_impact
from calc_model import get_models

LOGGER = logging.getLogger(__name__)
LISTEN_PORT = os.getenv("LISTEN_PORT", 9000)
ONE_DAY = datetime.timedelta(days=1)
if sys.platform.startswith('linux'):
    _PROCESS_COUNT = multiprocessing.cpu_count()
elif sys.platform.startswith('win32'):
    _PROCESS_COUNT = 1
else:
    raise Exception("Unsupported OS")
_THREAD_CONCURRENCY = _PROCESS_COUNT
RESULT_DTYPES = {'region': np.uint8, 'year_-1': np.uint16, 'year_-1_11003': np.int64, 'year_-1_11004': np.int64,
                 'year_-1_11103': np.int64, 'year_-1_11104': np.int64, 'year_-1_11203': np.int32,
                 'year_-1_11204': np.int32, 'year_-1_11303': np.int32, 'year_-1_11304': np.int32,
                 'year_-1_11403': np.int32, 'year_-1_11404': np.int32, 'year_-1_11503': np.int32,
                 'year_-1_11504': np.int32, 'year_-1_11603': np.int32, 'year_-1_11604': np.int32,
                 'year_-1_11703': np.int64, 'year_-1_11704': np.int64, 'year_-1_11803': np.int32,
                 'year_-1_11804': np.int32, 'year_-1_11903': np.int32, 'year_-1_11904': np.int32,
                 'year_-1_12003': np.int64, 'year_-1_12004': np.int64, 'year_-1_12103': np.int64,
                 'year_-1_12104': np.int64, 'year_-1_12203': np.int32, 'year_-1_12204': np.int32,
                 'year_-1_12303': np.int32, 'year_-1_12304': np.int32, 'year_-1_12403': np.int64,
                 'year_-1_12404': np.int64, 'year_-1_12503': np.int32, 'year_-1_12504': np.int32,
                 'year_-1_12603': np.int32, 'year_-1_12604': np.int32, 'year_-1_13003': np.int64,
                 'year_-1_13004': np.int64, 'year_-1_13103': np.int64, 'year_-1_13104': np.int64,
                 'year_-1_13203': np.int32, 'year_-1_13204': np.int32, 'year_-1_13403': np.int32,
                 'year_-1_13404': np.int32, 'year_-1_13503': np.int32, 'year_-1_13504': np.int32,
                 'year_-1_13603': np.int32, 'year_-1_13604': np.int32, 'year_-1_13703': np.int64,
                 'year_-1_13704': np.int64, 'year_-1_14003': np.int64, 'year_-1_14004': np.int64,
                 'year_-1_14103': np.int32, 'year_-1_14104': np.int32, 'year_-1_14203': np.int32,
                 'year_-1_14204': np.int32, 'year_-1_14303': np.int64, 'year_-1_14304': np.int64,
                 'year_-1_14503': np.int64, 'year_-1_14504': np.int64, 'year_-1_15003': np.int64,
                 'year_-1_15004': np.int64, 'year_-1_15103': np.int32, 'year_-1_15104': np.int32,
                 'year_-1_15203': np.int64, 'year_-1_15204': np.int64, 'year_-1_15303': np.int32,
                 'year_-1_15304': np.int32, 'year_-1_15403': np.int32, 'year_-1_15404': np.int32,
                 'year_-1_15503': np.int32, 'year_-1_15504': np.int32, 'year_-1_16003': np.int64,
                 'year_-1_16004': np.int64, 'year_-1_17003': np.int64, 'year_-1_17004': np.int64,
                 'year_-1_21003': np.int32, 'year_-1_21004': np.int32, 'year_-1_21103': np.int64,
                 'year_-1_21104': np.int64, 'year_-1_21203': np.int64, 'year_-1_21204': np.int64,
                 'year_-1_22003': np.int32, 'year_-1_22004': np.int32, 'year_-1_22103': np.int64,
                 'year_-1_22104': np.int64, 'year_-1_22203': np.int32, 'year_-1_22204': np.int32,
                 'year_-1_23003': np.int32, 'year_-1_23004': np.int32, 'year_-1_23103': np.int32,
                 'year_-1_23104': np.int32, 'year_-1_23203': np.int32, 'year_-1_23204': np.int32,
                 'year_-1_23303': np.int32, 'year_-1_23304': np.int32, 'year_-1_23403': np.int64,
                 'year_-1_23404': np.int64, 'year_-1_23503': np.int32, 'year_-1_23504': np.int32,
                 'year_-1_24003': np.int32, 'year_-1_24004': np.int32, 'year_-1_24103': np.int32,
                 'year_-1_24104': np.int32, 'year_-1_24213': np.int64, 'year_-1_24214': np.int64,
                 'year_-1_24303': np.int32, 'year_-1_24304': np.int32, 'year_-1_24503': np.int32,
                 'year_-1_24504': np.int32, 'year_-1_24603': np.int32, 'year_-1_24604': np.int32,
                 'year_-1_25003': np.int32, 'year_-1_25004': np.int32, 'year_-1_25103': np.int32,
                 'year_-1_25104': np.int32, 'year_-1_25203': np.int32, 'year_-1_25204': np.int32,
                 'year_-1_32003': np.int32, 'year_-1_32004': np.int32, 'year_-1_32005': np.int32,
                 'year_-1_32006': np.int32, 'year_-1_32007': np.int64, 'year_-1_32008': np.int64,
                 'year_-1_33003': np.int32, 'year_-1_33004': np.int32, 'year_-1_33005': np.int32,
                 'year_-1_33006': np.int32, 'year_-1_33007': np.int64, 'year_-1_33008': np.int64,
                 'year_-1_33103': np.int32, 'year_-1_33104': np.int32, 'year_-1_33105': np.int32,
                 'year_-1_33106': np.int32, 'year_-1_33107': np.int32, 'year_-1_33108': np.int32,
                 'year_-1_33117': np.int32, 'year_-1_33118': np.int32, 'year_-1_33125': np.int32,
                 'year_-1_33127': np.int32, 'year_-1_33128': np.int32, 'year_-1_33135': np.int32,
                 'year_-1_33137': np.int32, 'year_-1_33138': np.int32, 'year_-1_33143': np.int32,
                 'year_-1_33144': np.int32, 'year_-1_33145': np.int32, 'year_-1_33148': np.int32,
                 'year_-1_33153': np.int32, 'year_-1_33154': np.int32, 'year_-1_33155': np.int32,
                 'year_-1_33157': np.int32, 'year_-1_33163': np.int32, 'year_-1_33164': np.int32,
                 'year_-1_33165': np.int32, 'year_-1_33166': np.int32, 'year_-1_33167': np.int32,
                 'year_-1_33168': np.int32, 'year_-1_33203': np.int32, 'year_-1_33204': np.int32,
                 'year_-1_33205': np.int32, 'year_-1_33206': np.int32, 'year_-1_33207': np.int32,
                 'year_-1_33208': np.int32, 'year_-1_33217': np.int32, 'year_-1_33218': np.int32,
                 'year_-1_33225': np.int32, 'year_-1_33227': np.int32, 'year_-1_33228': np.int32,
                 'year_-1_33235': np.int32, 'year_-1_33237': np.int32, 'year_-1_33238': np.int32,
                 'year_-1_33243': np.int32, 'year_-1_33244': np.int32, 'year_-1_33245': np.int32,
                 'year_-1_33247': np.int32, 'year_-1_33248': np.int32, 'year_-1_33253': np.int32,
                 'year_-1_33254': np.int32, 'year_-1_33255': np.int32, 'year_-1_33257': np.int32,
                 'year_-1_33258': np.int32, 'year_-1_33263': np.int32, 'year_-1_33264': np.int32,
                 'year_-1_33265': np.int32, 'year_-1_33266': np.int32, 'year_-1_33267': np.int32,
                 'year_-1_33268': np.int32, 'year_-1_33277': np.int32, 'year_-1_33278': np.int32,
                 'year_-1_33305': np.int32, 'year_-1_33306': np.int32, 'year_-1_33307': np.int32,
                 'year_-1_33406': np.int32, 'year_-1_33407': np.int32, 'year_-1_36003': np.int64,
                 'year_-1_36004': np.int64, 'year_-1_41003': np.int32, 'year_-1_41103': np.int64,
                 'year_-1_41113': np.int64, 'year_-1_41123': np.int32, 'year_-1_41133': np.int32,
                 'year_-1_41193': np.int64, 'year_-1_41203': np.int64, 'year_-1_41213': np.int64,
                 'year_-1_41223': np.int32, 'year_-1_41233': np.int32, 'year_-1_41243': np.int32,
                 'year_-1_41293': np.int64, 'year_-1_42003': np.int32, 'year_-1_42103': np.int64,
                 'year_-1_42113': np.int64, 'year_-1_42123': np.int64, 'year_-1_42133': np.int64,
                 'year_-1_42143': np.int64, 'year_-1_42193': np.int32, 'year_-1_42203': np.int64,
                 'year_-1_42213': np.int64, 'year_-1_42223': np.int64, 'year_-1_42233': np.int64,
                 'year_-1_42243': np.int64, 'year_-1_42293': np.int32, 'year_-1_43003': np.int32,
                 'year_-1_43103': np.int64, 'year_-1_43113': np.int64, 'year_-1_43123': np.int64,
                 'year_-1_43133': np.int64, 'year_-1_43143': np.int64, 'year_-1_43193': np.int32,
                 'year_-1_43203': np.int32, 'year_-1_43213': np.int32, 'year_-1_43223': np.int32,
                 'year_-1_43233': np.int32, 'year_-1_43293': np.int32, 'year_-1_44003': np.int32,
                 'year_-1_44903': np.int32, 'year_-1_61003': np.int32, 'year_-1_62003': np.int32,
                 'year_-1_62103': np.int32, 'year_-1_62153': np.int32, 'year_-1_62203': np.int32,
                 'year_-1_62303': np.int32, 'year_-1_62403': np.int32, 'year_-1_62503': np.int32,
                 'year_-1_63003': np.int32, 'year_-1_63103': np.int32, 'year_-1_63113': np.int32,
                 'year_-1_63123': np.int32, 'year_-1_63133': np.int32, 'year_-1_63203': np.int32,
                 'year_-1_63213': np.int32, 'year_-1_63223': np.int32, 'year_-1_63233': np.int32,
                 'year_-1_63243': np.int32, 'year_-1_63253': np.int32, 'year_-1_63263': np.int32,
                 'year_-1_63303': np.int32, 'year_-1_63503': np.int32, 'year_-1_64003': np.int32,
                 'year_-1_okfs': np.uint8, 'year_-1_okopf': np.uint32, 'year_-1_type': np.uint8, 'year_-1_okved': str,
                 'year_0': np.uint16, 'year_0_11003': np.int64, 'year_0_11004': np.int64, 'year_0_11103': np.int64,
                 'year_0_11104': np.int64, 'year_0_11203': np.int32, 'year_0_11204': np.int32, 'year_0_11303': np.int32,
                 'year_0_11304': np.int32, 'year_0_11403': np.int32, 'year_0_11404': np.int32, 'year_0_11503': np.int32,
                 'year_0_11504': np.int32, 'year_0_11603': np.int32, 'year_0_11604': np.int32, 'year_0_11703': np.int64,
                 'year_0_11704': np.int64, 'year_0_11803': np.int32, 'year_0_11804': np.int32, 'year_0_11903': np.int32,
                 'year_0_11904': np.int32, 'year_0_12003': np.int64, 'year_0_12004': np.int64, 'year_0_12103': np.int64,
                 'year_0_12104': np.int64, 'year_0_12203': np.int32, 'year_0_12204': np.int32, 'year_0_12303': np.int32,
                 'year_0_12304': np.int32, 'year_0_12403': np.int64, 'year_0_12404': np.int64, 'year_0_12503': np.int32,
                 'year_0_12504': np.int32, 'year_0_12603': np.int32, 'year_0_12604': np.int32, 'year_0_13003': np.int64,
                 'year_0_13004': np.int64, 'year_0_13103': np.int64, 'year_0_13104': np.int64, 'year_0_13203': np.int32,
                 'year_0_13204': np.int32, 'year_0_13403': np.int32, 'year_0_13404': np.int32, 'year_0_13503': np.int32,
                 'year_0_13504': np.int32, 'year_0_13603': np.int32, 'year_0_13604': np.int32, 'year_0_13703': np.int64,
                 'year_0_13704': np.int64, 'year_0_14003': np.int64, 'year_0_14004': np.int64, 'year_0_14103': np.int32,
                 'year_0_14104': np.int32, 'year_0_14203': np.int32, 'year_0_14204': np.int32, 'year_0_14303': np.int64,
                 'year_0_14304': np.int64, 'year_0_14503': np.int64, 'year_0_14504': np.int64, 'year_0_15003': np.int64,
                 'year_0_15004': np.int64, 'year_0_15103': np.int32, 'year_0_15104': np.int32, 'year_0_15203': np.int64,
                 'year_0_15204': np.int64, 'year_0_15303': np.int32, 'year_0_15304': np.int32, 'year_0_15403': np.int32,
                 'year_0_15404': np.int32, 'year_0_15503': np.int32, 'year_0_15504': np.int32, 'year_0_16003': np.int64,
                 'year_0_16004': np.int64, 'year_0_17003': np.int64, 'year_0_17004': np.int64, 'year_0_21003': np.int32,
                 'year_0_21004': np.int32, 'year_0_21103': np.int64, 'year_0_21104': np.int64, 'year_0_21203': np.int64,
                 'year_0_21204': np.int64, 'year_0_22003': np.int32, 'year_0_22004': np.int32, 'year_0_22103': np.int64,
                 'year_0_22104': np.int64, 'year_0_22203': np.int32, 'year_0_22204': np.int32, 'year_0_23003': np.int32,
                 'year_0_23004': np.int32, 'year_0_23103': np.int32, 'year_0_23104': np.int32, 'year_0_23203': np.int32,
                 'year_0_23204': np.int32, 'year_0_23303': np.int32, 'year_0_23304': np.int32, 'year_0_23403': np.int64,
                 'year_0_23404': np.int64, 'year_0_23503': np.int32, 'year_0_23504': np.int32, 'year_0_24003': np.int32,
                 'year_0_24004': np.int32, 'year_0_24103': np.int32, 'year_0_24104': np.int32, 'year_0_24213': np.int64,
                 'year_0_24214': np.int64, 'year_0_24303': np.int32, 'year_0_24304': np.int32, 'year_0_24503': np.int32,
                 'year_0_24504': np.int32, 'year_0_24603': np.int32, 'year_0_24604': np.int32, 'year_0_25003': np.int32,
                 'year_0_25004': np.int32, 'year_0_25103': np.int32, 'year_0_25104': np.int32, 'year_0_25203': np.int32,
                 'year_0_25204': np.int32, 'year_0_32003': np.int32, 'year_0_32004': np.int32, 'year_0_32005': np.int32,
                 'year_0_32006': np.int32, 'year_0_32007': np.int64, 'year_0_32008': np.int64, 'year_0_33003': np.int32,
                 'year_0_33004': np.int32, 'year_0_33005': np.int32, 'year_0_33006': np.int32, 'year_0_33007': np.int64,
                 'year_0_33008': np.int64, 'year_0_33103': np.int32, 'year_0_33104': np.int32, 'year_0_33105': np.int32,
                 'year_0_33106': np.int32, 'year_0_33107': np.int32, 'year_0_33108': np.int32, 'year_0_33117': np.int32,
                 'year_0_33118': np.int32, 'year_0_33125': np.int32, 'year_0_33127': np.int32, 'year_0_33128': np.int32,
                 'year_0_33135': np.int32, 'year_0_33137': np.int32, 'year_0_33138': np.int32, 'year_0_33143': np.int32,
                 'year_0_33144': np.int32, 'year_0_33145': np.int32, 'year_0_33148': np.int32, 'year_0_33153': np.int32,
                 'year_0_33154': np.int32, 'year_0_33155': np.int32, 'year_0_33157': np.int32, 'year_0_33163': np.int32,
                 'year_0_33164': np.int32, 'year_0_33165': np.int32, 'year_0_33166': np.int32, 'year_0_33167': np.int32,
                 'year_0_33168': np.int32, 'year_0_33203': np.int32, 'year_0_33204': np.int32, 'year_0_33205': np.int32,
                 'year_0_33206': np.int32, 'year_0_33207': np.int32, 'year_0_33208': np.int32, 'year_0_33217': np.int32,
                 'year_0_33218': np.int32, 'year_0_33225': np.int32, 'year_0_33227': np.int32, 'year_0_33228': np.int32,
                 'year_0_33235': np.int32, 'year_0_33237': np.int32, 'year_0_33238': np.int32, 'year_0_33243': np.int32,
                 'year_0_33244': np.int32, 'year_0_33245': np.int32, 'year_0_33247': np.int32, 'year_0_33248': np.int32,
                 'year_0_33253': np.int32, 'year_0_33254': np.int32, 'year_0_33255': np.int32, 'year_0_33257': np.int32,
                 'year_0_33258': np.int32, 'year_0_33263': np.int32, 'year_0_33264': np.int32, 'year_0_33265': np.int32,
                 'year_0_33266': np.int32, 'year_0_33267': np.int32, 'year_0_33268': np.int32, 'year_0_33277': np.int32,
                 'year_0_33278': np.int32, 'year_0_33305': np.int32, 'year_0_33306': np.int32, 'year_0_33307': np.int32,
                 'year_0_33406': np.int32, 'year_0_33407': np.int32, 'year_0_36003': np.int64, 'year_0_36004': np.int64,
                 'year_0_41003': np.int32, 'year_0_41103': np.int64, 'year_0_41113': np.int64, 'year_0_41123': np.int32,
                 'year_0_41133': np.int32, 'year_0_41193': np.int64, 'year_0_41203': np.int64, 'year_0_41213': np.int64,
                 'year_0_41223': np.int32, 'year_0_41233': np.int32, 'year_0_41243': np.int32, 'year_0_41293': np.int64,
                 'year_0_42003': np.int32, 'year_0_42103': np.int64, 'year_0_42113': np.int64, 'year_0_42123': np.int64,
                 'year_0_42133': np.int64, 'year_0_42143': np.int64, 'year_0_42193': np.int32, 'year_0_42203': np.int64,
                 'year_0_42213': np.int64, 'year_0_42223': np.int64, 'year_0_42233': np.int64, 'year_0_42243': np.int64,
                 'year_0_42293': np.int32, 'year_0_43003': np.int32, 'year_0_43103': np.int64, 'year_0_43113': np.int64,
                 'year_0_43123': np.int64, 'year_0_43133': np.int64, 'year_0_43143': np.int64, 'year_0_43193': np.int32,
                 'year_0_43203': np.int32, 'year_0_43213': np.int32, 'year_0_43223': np.int32, 'year_0_43233': np.int32,
                 'year_0_43293': np.int32, 'year_0_44003': np.int32, 'year_0_44903': np.int32, 'year_0_61003': np.int32,
                 'year_0_62003': np.int32, 'year_0_62103': np.int32, 'year_0_62153': np.int32, 'year_0_62203': np.int32,
                 'year_0_62303': np.int32, 'year_0_62403': np.int32, 'year_0_62503': np.int32, 'year_0_63003': np.int32,
                 'year_0_63103': np.int32, 'year_0_63113': np.int32, 'year_0_63123': np.int32, 'year_0_63133': np.int32,
                 'year_0_63203': np.int32, 'year_0_63213': np.int32, 'year_0_63223': np.int32, 'year_0_63233': np.int32,
                 'year_0_63243': np.int32, 'year_0_63253': np.int32, 'year_0_63263': np.int32, 'year_0_63303': np.int32,
                 'year_0_63503': np.int32, 'year_0_64003': np.int32, 'year_0_okfs': np.uint8, 'year_0_okopf': np.uint32,
                 'year_0_type': np.uint8, 'year_0_okved': str, }


class Handler(calc_service_pb2_grpc.CalcServiceServicer):
    models = None

    def __init__(self):
        self.models = get_models(host=os.getenv("DB_HOST"),
                                 port=int(os.getenv("DB_PORT")),
                                 user=os.getenv("DB_USER"),
                                 password=os.getenv("DB_PASSWORD"),
                                 database=os.getenv("DB_DATABASE"))

    def _dict_to_df(self, data):
        df = pd.DataFrame.from_dict(data, orient='index').T
        return df.astype(dtype=RESULT_DTYPES)

    def CalcProbability(self, request, context):
        df = self._dict_to_df(request.Params)
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

    def GetImpact(self, request, context):
        image = feature_impact.plt_graph_to_base64(
            model=self.models[request.ModelName],
            data=self._dict_to_df(request.Data),
            feature=request.Feature,
            head=request.Head,
            tail=request.Tail
        )
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY),
                         options=(('grpc.so_reuseport', 1),))
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
