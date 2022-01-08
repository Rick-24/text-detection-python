from string import Template

from ltp import LTP

from text_detection.algorithm.ltp import semantic_analysis_for_detect
from text_detection.integration.docx import file_read


def detect(filePath, graph):
    sentence_list = file_read(filePath)
    ltp = LTP(path='G:/Downloads/base2.tgz')
    detect_result = []
    for sentence in sentence_list:
        temp = "".join([sentence['text']])
        result = semantic_analysis_for_detect(ltp, temp)
        match_list = neo4j_search(graph, result)
        if match_list:
            sentence_result = {'sentence': sentence, 'match_list': match_list}
            print(match_list)
            detect_result.append(sentence_result)

    return detect_result


def neo4j_search(graph, results):
    # MATCH(n: Root)-[: CONT]->(f),
    # (n) - [: DATV]->(e),
    # (n) - [: DATV]->(d)
    # WHERE(n.value = "给予") and (f.value="补助" and e.value="项目" and d.value = "贷款额")
    # RETURN
    # n, f

    rela_template = Template('(n: Root)-[: ${key1}]->(${key2})')
    root_template = Template(' WHERE(n.value = "${key1}")')
    condition_template = Template(' and ${key1}.value = "${key2}"')
    match_list = []
    for result in results:
        cypher = "MATCH "
        relation = ""
        condition = ""
        root = ""
        for i, rela in enumerate(result):
            if rela[0] in ["Root"]:
                root += root_template.substitute(key1=rela[1])
            else:
                condition += condition_template.substitute(key1=rela[0] + str(i), key2=rela[1])
                relation = relation + rela_template.substitute(key1=rela[0], key2=rela[0] + str(i)) + ","
        if len(result) == 1:
            relation = '(n:Root) '
        relation = relation[:-1]
        relation += ',(n)<-[:Include]-(f)'
        cypher = cypher + relation + root + condition + " RETURN n.segment_num,n.sentence_num,n.text,f.path,f.type"
        run = graph.run(cypher)
        for i in run:
            match = {'segment_num': i[0], 'sentence_num': i[1], 'text': i[2], 'path': i[3], 'type': i[4]}
            match_list.append(match)
        if len(match_list) > 10:
            match_list = []
    return match_list
