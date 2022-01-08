from ltp import LTP


def semantic_analysis(ltp, sentence):
    seg, hidden = ltp.seg([sentence])
    result = ltp.sdp(hidden, mode='tree')[0]
    root = [x for x in result if x[1] == 0 and x[2] == 'Root'][0][0]
    root_relation = [x for x in result if x[1] == root]
    relation = []
    relation_result = []
    for rela in root_relation:
        relation.append((rela[2], seg[0][rela[0] - 1]))
    relation.append(('Root', seg[0][root - 1]))
    relation = [x for x in relation if x[0] not in ['mRELA', 'mPUNC', 'mDEPD']]

    esucc_relation = [x[0] for x in result if x[1] == root and x[2] == 'eSUCC']
    for esucc in esucc_relation:
        esucc_rela = [x for x in result if x[1] == esucc]
        rela_result = []
        for rela in esucc_rela:
            rela_result.append((rela[2], seg[0][rela[0] - 1]))
        rela_result.append(('Root', seg[0][esucc - 1]))
        rela_result = [x for x in rela_result if x[0] not in ['mRELA', 'mPUNC', 'mDEPD']]
        relation_result.append(rela_result)
    relation_result.append(relation)
    return relation_result


def semantic_analysis_for_detect(ltp, sentence):
    seg, hidden = ltp.seg([sentence])
    result = ltp.sdp(hidden, mode='tree')[0]
    root = [x for x in result if x[1] == 0 and x[2] == 'Root'][0][0]
    root_relation = [x for x in result if x[1] == root]
    relation = []
    relation_result = []
    for rela in root_relation:
        relation.append((rela[2], seg[0][rela[0] - 1]))
    relation.append(('Root', seg[0][root - 1]))
    relation = [x for x in relation if x[0] not in ['mRELA', 'mPUNC', 'mDEPD', 'MEAS', 'DATV']]

    esucc_relation = [x[0] for x in result if x[1] == root and x[2] == 'eSUCC']
    for esucc in esucc_relation:
        esucc_rela = [x for x in result if x[1] == esucc]
        rela_result = []
        for rela in esucc_rela:
            rela_result.append((rela[2], seg[0][rela[0] - 1]))
        rela_result.append(('Root', seg[0][esucc - 1]))
        rela_result = [x for x in rela_result if x[0] not in ['mRELA', 'mPUNC', 'mDEPD', 'MEAS', 'DATV']]
        relation_result.append(rela_result)
    relation_result.append(relation)
    return relation_result
