import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

COLUMNS_NAME = ['name', 'okpo', 'okopf', 'okfs', 'okved', 'inn', 'measure', 'type', ]
COLUMNS_VALUE = ['11103', '11104', '11203', '11204', '11303', '11304', '11403', '11404', '11503', '11504', '11603', '11604', '11703', '11704', '11803', '11804', '11903', '11904', '11003',
                 '11004', '12103', '12104', '12203', '12204', '12303', '12304', '12403', '12404', '12503', '12504', '12603', '12604', '12003', '12004', '16003', '16004', '13103', '13104', '13203', '13204', '13403', '13404', '13503', '13504', '13603',
                 '13604', '13703', '13704', '13003', '13004', '14103', '14104', '14203', '14204', '14303', '14304', '14503', '14504', '14003', '14004', '15103', '15104', '15203', '15204', '15303', '15304', '15403', '15404', '15503', '15504', '15003',
                 '15004', '17003', '17004', '21103', '21104', '21203', '21204', '21003', '21004', '22103', '22104', '22203', '22204', '22003', '22004', '23103', '23104', '23203', '23204', '23303', '23304', '23403', '23404', '23503', '23504', '23003',
                 '23004', '24103', '24104', '24213', '24214', '24303', '24304', '24503', '24504', '24603', '24604', '24003', '24004', '25103', '25104', '25203', '25204', '25003', '25004', '32003', '32004', '32005', '32006', '32007', '32008', '33103',
                 '33104', '33105', '33106', '33107', '33108', '33117', '33118', '33125', '33127', '33128', '33135', '33137', '33138', '33143', '33144', '33145', '33148', '33153', '33154', '33155', '33157', '33163', '33164', '33165', '33166', '33167',
                 '33168', '33203', '33204', '33205', '33206', '33207', '33208', '33217', '33218', '33225', '33227', '33228', '33235', '33237', '33238', '33243', '33244', '33245', '33247', '33248', '33253', '33254', '33255', '33257', '33258', '33263',
                 '33264', '33265', '33266', '33267', '33268', '33277', '33278', '33305', '33306', '33307', '33406', '33407', '33003', '33004', '33005', '33006', '33007', '33008', '36003', '36004', '41103', '41113', '41123', '41133', '41193', '41203',
                 '41213', '41223', '41233', '41243', '41293', '41003', '42103', '42113', '42123', '42133', '42143', '42193', '42203', '42213', '42223', '42233', '42243', '42293', '42003', '43103', '43113', '43123', '43133', '43143', '43193', '43203',
                 '43213', '43223', '43233', '43293', '43003', '44003', '44903', '61003', '62103', '62153', '62203', '62303', '62403', '62503', '62003', '63103', '63113', '63123', '63133', '63203', '63213', '63223', '63233', '63243', '63253', '63263',
                 '63303', '63503', '63003', '64003']
COLUMNS = COLUMNS_NAME + COLUMNS_VALUE
YEAR_FIRST = 2012
YEAR_LAST = 2018
NUM_WRITE = -1
RESULT_DTYPES = {'inn': np.uint64, 'region': np.uint8, 'target': np.uint8, 'year_-1': np.uint16, 'year_-1_11003': np.int64, 'year_-1_11004': np.int64, 'year_-1_11103': np.int64, 'year_-1_11104': np.int64, 'year_-1_11203': np.int32, 'year_-1_11204': np.int32,
     'year_-1_11303': np.int32, 'year_-1_11304': np.int32, 'year_-1_11403': np.int32, 'year_-1_11404': np.int32, 'year_-1_11503': np.int32, 'year_-1_11504': np.int32, 'year_-1_11603': np.int32, 'year_-1_11604': np.int32, 'year_-1_11703': np.int64,
     'year_-1_11704': np.int64, 'year_-1_11803': np.int32, 'year_-1_11804': np.int32, 'year_-1_11903': np.int32, 'year_-1_11904': np.int32, 'year_-1_12003': np.int64, 'year_-1_12004': np.int64, 'year_-1_12103': np.int64, 'year_-1_12104': np.int64,
     'year_-1_12203': np.int32, 'year_-1_12204': np.int32, 'year_-1_12303': np.int32, 'year_-1_12304': np.int32, 'year_-1_12403': np.int64, 'year_-1_12404': np.int64, 'year_-1_12503': np.int32, 'year_-1_12504': np.int32, 'year_-1_12603': np.int32,
     'year_-1_12604': np.int32, 'year_-1_13003': np.int64, 'year_-1_13004': np.int64, 'year_-1_13103': np.int64, 'year_-1_13104': np.int64, 'year_-1_13203': np.int32, 'year_-1_13204': np.int32, 'year_-1_13403': np.int32, 'year_-1_13404': np.int32,
     'year_-1_13503': np.int32, 'year_-1_13504': np.int32, 'year_-1_13603': np.int32, 'year_-1_13604': np.int32, 'year_-1_13703': np.int64, 'year_-1_13704': np.int64, 'year_-1_14003': np.int64, 'year_-1_14004': np.int64, 'year_-1_14103': np.int32,
     'year_-1_14104': np.int32, 'year_-1_14203': np.int32, 'year_-1_14204': np.int32, 'year_-1_14303': np.int64, 'year_-1_14304': np.int64, 'year_-1_14503': np.int64, 'year_-1_14504': np.int64, 'year_-1_15003': np.int64, 'year_-1_15004': np.int64,
     'year_-1_15103': np.int32, 'year_-1_15104': np.int32, 'year_-1_15203': np.int64, 'year_-1_15204': np.int64, 'year_-1_15303': np.int32, 'year_-1_15304': np.int32, 'year_-1_15403': np.int32, 'year_-1_15404': np.int32, 'year_-1_15503': np.int32,
     'year_-1_15504': np.int32, 'year_-1_16003': np.int64, 'year_-1_16004': np.int64, 'year_-1_17003': np.int64, 'year_-1_17004': np.int64, 'year_-1_21003': np.int32, 'year_-1_21004': np.int32, 'year_-1_21103': np.int64, 'year_-1_21104': np.int64,
     'year_-1_21203': np.int64, 'year_-1_21204': np.int64, 'year_-1_22003': np.int32, 'year_-1_22004': np.int32, 'year_-1_22103': np.int64, 'year_-1_22104': np.int64, 'year_-1_22203': np.int32, 'year_-1_22204': np.int32, 'year_-1_23003': np.int32,
     'year_-1_23004': np.int32, 'year_-1_23103': np.int32, 'year_-1_23104': np.int32, 'year_-1_23203': np.int32, 'year_-1_23204': np.int32, 'year_-1_23303': np.int32, 'year_-1_23304': np.int32, 'year_-1_23403': np.int64, 'year_-1_23404': np.int64,
     'year_-1_23503': np.int32, 'year_-1_23504': np.int32, 'year_-1_24003': np.int32, 'year_-1_24004': np.int32, 'year_-1_24103': np.int32, 'year_-1_24104': np.int32, 'year_-1_24213': np.int64, 'year_-1_24214': np.int64, 'year_-1_24303': np.int32,
     'year_-1_24304': np.int32, 'year_-1_24503': np.int32, 'year_-1_24504': np.int32, 'year_-1_24603': np.int32, 'year_-1_24604': np.int32, 'year_-1_25003': np.int32, 'year_-1_25004': np.int32, 'year_-1_25103': np.int32, 'year_-1_25104': np.int32,
     'year_-1_25203': np.int32, 'year_-1_25204': np.int32, 'year_-1_32003': np.int32, 'year_-1_32004': np.int32, 'year_-1_32005': np.int32, 'year_-1_32006': np.int32, 'year_-1_32007': np.int64, 'year_-1_32008': np.int64, 'year_-1_33003': np.int32,
     'year_-1_33004': np.int32, 'year_-1_33005': np.int32, 'year_-1_33006': np.int32, 'year_-1_33007': np.int64, 'year_-1_33008': np.int64, 'year_-1_33103': np.int32, 'year_-1_33104': np.int32, 'year_-1_33105': np.int32, 'year_-1_33106': np.int32,
     'year_-1_33107': np.int32, 'year_-1_33108': np.int32, 'year_-1_33117': np.int32, 'year_-1_33118': np.int32, 'year_-1_33125': np.int32, 'year_-1_33127': np.int32, 'year_-1_33128': np.int32, 'year_-1_33135': np.int32, 'year_-1_33137': np.int32,
     'year_-1_33138': np.int32, 'year_-1_33143': np.int32, 'year_-1_33144': np.int32, 'year_-1_33145': np.int32, 'year_-1_33148': np.int32, 'year_-1_33153': np.int32, 'year_-1_33154': np.int32, 'year_-1_33155': np.int32, 'year_-1_33157': np.int32,
     'year_-1_33163': np.int32, 'year_-1_33164': np.int32, 'year_-1_33165': np.int32, 'year_-1_33166': np.int32, 'year_-1_33167': np.int32, 'year_-1_33168': np.int32, 'year_-1_33203': np.int32, 'year_-1_33204': np.int32, 'year_-1_33205': np.int32,
     'year_-1_33206': np.int32, 'year_-1_33207': np.int32, 'year_-1_33208': np.int32, 'year_-1_33217': np.int32, 'year_-1_33218': np.int32, 'year_-1_33225': np.int32, 'year_-1_33227': np.int32, 'year_-1_33228': np.int32, 'year_-1_33235': np.int32,
     'year_-1_33237': np.int32, 'year_-1_33238': np.int32, 'year_-1_33243': np.int32, 'year_-1_33244': np.int32, 'year_-1_33245': np.int32, 'year_-1_33247': np.int32, 'year_-1_33248': np.int32, 'year_-1_33253': np.int32, 'year_-1_33254': np.int32,
     'year_-1_33255': np.int32, 'year_-1_33257': np.int32, 'year_-1_33258': np.int32, 'year_-1_33263': np.int32, 'year_-1_33264': np.int32, 'year_-1_33265': np.int32, 'year_-1_33266': np.int32, 'year_-1_33267': np.int32, 'year_-1_33268': np.int32,
     'year_-1_33277': np.int32, 'year_-1_33278': np.int32, 'year_-1_33305': np.int32, 'year_-1_33306': np.int32, 'year_-1_33307': np.int32, 'year_-1_33406': np.int32, 'year_-1_33407': np.int32, 'year_-1_36003': np.int64, 'year_-1_36004': np.int64,
     'year_-1_41003': np.int32, 'year_-1_41103': np.int64, 'year_-1_41113': np.int64, 'year_-1_41123': np.int32, 'year_-1_41133': np.int32, 'year_-1_41193': np.int64, 'year_-1_41203': np.int64, 'year_-1_41213': np.int64, 'year_-1_41223': np.int32,
     'year_-1_41233': np.int32, 'year_-1_41243': np.int32, 'year_-1_41293': np.int64, 'year_-1_42003': np.int32, 'year_-1_42103': np.int64, 'year_-1_42113': np.int64, 'year_-1_42123': np.int64, 'year_-1_42133': np.int64, 'year_-1_42143': np.int64,
     'year_-1_42193': np.int32, 'year_-1_42203': np.int64, 'year_-1_42213': np.int64, 'year_-1_42223': np.int64, 'year_-1_42233': np.int64, 'year_-1_42243': np.int64, 'year_-1_42293': np.int32, 'year_-1_43003': np.int32, 'year_-1_43103': np.int64,
     'year_-1_43113': np.int64, 'year_-1_43123': np.int64, 'year_-1_43133': np.int64, 'year_-1_43143': np.int64, 'year_-1_43193': np.int32, 'year_-1_43203': np.int32, 'year_-1_43213': np.int32, 'year_-1_43223': np.int32, 'year_-1_43233': np.int32,
     'year_-1_43293': np.int32, 'year_-1_44003': np.int32, 'year_-1_44903': np.int32, 'year_-1_61003': np.int32, 'year_-1_62003': np.int32, 'year_-1_62103': np.int32, 'year_-1_62153': np.int32, 'year_-1_62203': np.int32, 'year_-1_62303': np.int32,
     'year_-1_62403': np.int32, 'year_-1_62503': np.int32, 'year_-1_63003': np.int32, 'year_-1_63103': np.int32, 'year_-1_63113': np.int32, 'year_-1_63123': np.int32, 'year_-1_63133': np.int32, 'year_-1_63203': np.int32, 'year_-1_63213': np.int32,
     'year_-1_63223': np.int32, 'year_-1_63233': np.int32, 'year_-1_63243': np.int32, 'year_-1_63253': np.int32, 'year_-1_63263': np.int32, 'year_-1_63303': np.int32, 'year_-1_63503': np.int32, 'year_-1_64003': np.int32, 'year_-1_okfs': np.uint8,
     'year_-1_okopf': np.uint32, 'year_-1_type': np.uint8, 'year_-1_okved': str, 'year_0': np.uint16, 'year_0_11003': np.int64, 'year_0_11004': np.int64, 'year_0_11103': np.int64, 'year_0_11104': np.int64, 'year_0_11203': np.int32,
     'year_0_11204': np.int32, 'year_0_11303': np.int32, 'year_0_11304': np.int32, 'year_0_11403': np.int32, 'year_0_11404': np.int32, 'year_0_11503': np.int32, 'year_0_11504': np.int32, 'year_0_11603': np.int32, 'year_0_11604': np.int32,
     'year_0_11703': np.int64, 'year_0_11704': np.int64, 'year_0_11803': np.int32, 'year_0_11804': np.int32, 'year_0_11903': np.int32, 'year_0_11904': np.int32, 'year_0_12003': np.int64, 'year_0_12004': np.int64, 'year_0_12103': np.int64,
     'year_0_12104': np.int64, 'year_0_12203': np.int32, 'year_0_12204': np.int32, 'year_0_12303': np.int32, 'year_0_12304': np.int32, 'year_0_12403': np.int64, 'year_0_12404': np.int64, 'year_0_12503': np.int32, 'year_0_12504': np.int32,
     'year_0_12603': np.int32, 'year_0_12604': np.int32, 'year_0_13003': np.int64, 'year_0_13004': np.int64, 'year_0_13103': np.int64, 'year_0_13104': np.int64, 'year_0_13203': np.int32, 'year_0_13204': np.int32, 'year_0_13403': np.int32,
     'year_0_13404': np.int32, 'year_0_13503': np.int32, 'year_0_13504': np.int32, 'year_0_13603': np.int32, 'year_0_13604': np.int32, 'year_0_13703': np.int64, 'year_0_13704': np.int64, 'year_0_14003': np.int64, 'year_0_14004': np.int64,
     'year_0_14103': np.int32, 'year_0_14104': np.int32, 'year_0_14203': np.int32, 'year_0_14204': np.int32, 'year_0_14303': np.int64, 'year_0_14304': np.int64, 'year_0_14503': np.int64, 'year_0_14504': np.int64, 'year_0_15003': np.int64,
     'year_0_15004': np.int64, 'year_0_15103': np.int32, 'year_0_15104': np.int32, 'year_0_15203': np.int64, 'year_0_15204': np.int64, 'year_0_15303': np.int32, 'year_0_15304': np.int32, 'year_0_15403': np.int32, 'year_0_15404': np.int32,
     'year_0_15503': np.int32, 'year_0_15504': np.int32, 'year_0_16003': np.int64, 'year_0_16004': np.int64, 'year_0_17003': np.int64, 'year_0_17004': np.int64, 'year_0_21003': np.int32, 'year_0_21004': np.int32, 'year_0_21103': np.int64,
     'year_0_21104': np.int64, 'year_0_21203': np.int64, 'year_0_21204': np.int64, 'year_0_22003': np.int32, 'year_0_22004': np.int32, 'year_0_22103': np.int64, 'year_0_22104': np.int64, 'year_0_22203': np.int32, 'year_0_22204': np.int32,
     'year_0_23003': np.int32, 'year_0_23004': np.int32, 'year_0_23103': np.int32, 'year_0_23104': np.int32, 'year_0_23203': np.int32, 'year_0_23204': np.int32, 'year_0_23303': np.int32, 'year_0_23304': np.int32, 'year_0_23403': np.int64,
     'year_0_23404': np.int64, 'year_0_23503': np.int32, 'year_0_23504': np.int32, 'year_0_24003': np.int32, 'year_0_24004': np.int32, 'year_0_24103': np.int32, 'year_0_24104': np.int32, 'year_0_24213': np.int64, 'year_0_24214': np.int64,
     'year_0_24303': np.int32, 'year_0_24304': np.int32, 'year_0_24503': np.int32, 'year_0_24504': np.int32, 'year_0_24603': np.int32, 'year_0_24604': np.int32, 'year_0_25003': np.int32, 'year_0_25004': np.int32, 'year_0_25103': np.int32,
     'year_0_25104': np.int32, 'year_0_25203': np.int32, 'year_0_25204': np.int32, 'year_0_32003': np.int32, 'year_0_32004': np.int32, 'year_0_32005': np.int32, 'year_0_32006': np.int32, 'year_0_32007': np.int64, 'year_0_32008': np.int64,
     'year_0_33003': np.int32, 'year_0_33004': np.int32, 'year_0_33005': np.int32, 'year_0_33006': np.int32, 'year_0_33007': np.int64, 'year_0_33008': np.int64, 'year_0_33103': np.int32, 'year_0_33104': np.int32, 'year_0_33105': np.int32,
     'year_0_33106': np.int32, 'year_0_33107': np.int32, 'year_0_33108': np.int32, 'year_0_33117': np.int32, 'year_0_33118': np.int32, 'year_0_33125': np.int32, 'year_0_33127': np.int32, 'year_0_33128': np.int32, 'year_0_33135': np.int32,
     'year_0_33137': np.int32, 'year_0_33138': np.int32, 'year_0_33143': np.int32, 'year_0_33144': np.int32, 'year_0_33145': np.int32, 'year_0_33148': np.int32, 'year_0_33153': np.int32, 'year_0_33154': np.int32, 'year_0_33155': np.int32,
     'year_0_33157': np.int32, 'year_0_33163': np.int32, 'year_0_33164': np.int32, 'year_0_33165': np.int32, 'year_0_33166': np.int32, 'year_0_33167': np.int32, 'year_0_33168': np.int32, 'year_0_33203': np.int32, 'year_0_33204': np.int32,
     'year_0_33205': np.int32, 'year_0_33206': np.int32, 'year_0_33207': np.int32, 'year_0_33208': np.int32, 'year_0_33217': np.int32, 'year_0_33218': np.int32, 'year_0_33225': np.int32, 'year_0_33227': np.int32, 'year_0_33228': np.int32,
     'year_0_33235': np.int32, 'year_0_33237': np.int32, 'year_0_33238': np.int32, 'year_0_33243': np.int32, 'year_0_33244': np.int32, 'year_0_33245': np.int32, 'year_0_33247': np.int32, 'year_0_33248': np.int32, 'year_0_33253': np.int32,
     'year_0_33254': np.int32, 'year_0_33255': np.int32, 'year_0_33257': np.int32, 'year_0_33258': np.int32, 'year_0_33263': np.int32, 'year_0_33264': np.int32, 'year_0_33265': np.int32, 'year_0_33266': np.int32, 'year_0_33267': np.int32,
     'year_0_33268': np.int32, 'year_0_33277': np.int32, 'year_0_33278': np.int32, 'year_0_33305': np.int32, 'year_0_33306': np.int32, 'year_0_33307': np.int32, 'year_0_33406': np.int32, 'year_0_33407': np.int32, 'year_0_36003': np.int64,
     'year_0_36004': np.int64, 'year_0_41003': np.int32, 'year_0_41103': np.int64, 'year_0_41113': np.int64, 'year_0_41123': np.int32, 'year_0_41133': np.int32, 'year_0_41193': np.int64, 'year_0_41203': np.int64, 'year_0_41213': np.int64,
     'year_0_41223': np.int32, 'year_0_41233': np.int32, 'year_0_41243': np.int32, 'year_0_41293': np.int64, 'year_0_42003': np.int32, 'year_0_42103': np.int64, 'year_0_42113': np.int64, 'year_0_42123': np.int64, 'year_0_42133': np.int64,
     'year_0_42143': np.int64, 'year_0_42193': np.int32, 'year_0_42203': np.int64, 'year_0_42213': np.int64, 'year_0_42223': np.int64, 'year_0_42233': np.int64, 'year_0_42243': np.int64, 'year_0_42293': np.int32, 'year_0_43003': np.int32,
     'year_0_43103': np.int64, 'year_0_43113': np.int64, 'year_0_43123': np.int64, 'year_0_43133': np.int64, 'year_0_43143': np.int64, 'year_0_43193': np.int32, 'year_0_43203': np.int32, 'year_0_43213': np.int32, 'year_0_43223': np.int32,
     'year_0_43233': np.int32, 'year_0_43293': np.int32, 'year_0_44003': np.int32, 'year_0_44903': np.int32, 'year_0_61003': np.int32, 'year_0_62003': np.int32, 'year_0_62103': np.int32, 'year_0_62153': np.int32, 'year_0_62203': np.int32,
     'year_0_62303': np.int32, 'year_0_62403': np.int32, 'year_0_62503': np.int32, 'year_0_63003': np.int32, 'year_0_63103': np.int32, 'year_0_63113': np.int32, 'year_0_63123': np.int32, 'year_0_63133': np.int32, 'year_0_63203': np.int32,
     'year_0_63213': np.int32, 'year_0_63223': np.int32, 'year_0_63233': np.int32, 'year_0_63243': np.int32, 'year_0_63253': np.int32, 'year_0_63263': np.int32, 'year_0_63303': np.int32, 'year_0_63503': np.int32, 'year_0_64003': np.int32,
     'year_0_okfs': np.uint8, 'year_0_okopf': np.uint32, 'year_0_type': np.uint8, 'year_0_okved': str, }

def plot_corr(D, size):
    corr = D.corr()
    corr = np.abs(corr)
    f, ax = plt.subplots(figsize=(size, size))
    cmap = plt.cm.Oranges
    sns.heatmap(corr, cmap=cmap,
                xticklabels=corr.columns,
                yticklabels=corr.columns)
