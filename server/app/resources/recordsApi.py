# !/usr/bin/env python
# -*- coding:utf8 -*-
# 记录接口（post：新增记录，get：获取用户记录信息）

from . import *
import app.resources.algorithm.process as al
# from app.resources.algorithm.process import *
import requests
from app.resources.algorithm.process import *
import re
import json

# 临时使用随机数生成成绩
import random
import _thread
import time
import threading

# import pycorrector
# from stanfordcorenlp import StanfordCoreNLP
import jieba
import re


newjuFa_Score = 0
corrected_wenzhang = []

#这个函数应该是有问题的
def juFa(fenJu_WenZhang, stanfordPath):

    juFa_WenZhang = []
    kuoHao_Stack = []

    nlp = StanfordCoreNLP(stanfordPath, lang="zh")
    for juZi in fenJu_WenZhang:
        shuGao = 0
        kuoHao_Stack = []
        # print(nlp.parse(juZi))
        # print(juZi)
        try:
            for character in nlp.parse(juZi):
                # print(character)
                if(character == '('):
                    if(len(kuoHao_Stack) == shuGao):
                        shuGao += 1
                    kuoHao_Stack.append("1")
                elif(character == ')'):
                    kuoHao_Stack.pop()
        except:
            # print(juZi)
            break
        # print(shuGao)
        juFa_WenZhang.append(shuGao)
    # avg(juFa_WenZhang)

    newjuFa_Score = averagenum(juFa_WenZhang)  # ztz


# def correct(fenJu_WenZhang):
#     corrected_wenzhang = []
#     wrong_words = []
#     original_wenzhang = []
# 
#     # zhy
#     for sent in fenJu_WenZhang:
#         corrected_sent, detail = pycorrector.correct(sent)
#         # print(corrected_sent)
#         corrected_wenzhang.append(corrected_sent)
#         temp_list = list(corrected_sent)# 把正确的句子先变成list
#         for wrong_word in detail:
#             wrong_words.append(wrong_word)
#             temp_list[wrong_word[2]:wrong_word[3]] = '*'+wrong_word[0]+'*'# 在错词的两边添加了标记“*”
#         original_sent = "".join(temp_list)
#         original_wenzhang.append(original_sent)
# 
# 
#         # wrong_words.append(detail)# detail 是一个[[], [], []]
#     corrected_wenzhang = corrected_wenzhang, wrong_words, original_wenzhang# ztz


def correct_byWenXin(essay):
    
    headers = {
        "Accept":"pplication/json, text/plain, */*", 
        "Accept-Encoding":"gzip, deflate", 
        "Accept-Language":"zh-CN, zh;q = 0.9", 
        "Content-Type":"application/x-www-form-urlencoded;charset = UTF-8"
    }
    
    data_write = {
        "content":essay
    }
    # print(essay)
    data_write = json.dumps(data_write)
    url_write = "http://202.112.194.61:8091/api/gec/write"
    r = requests.post(url=url_write, headers=headers, data=data_write)
    # print(re.search('\d+', r.text))
    data_check = {
        "id":re.search('\d+', r.text).group(0)
    }
    data_check = json.dumps(data_check)
    url_check = "http://202.112.194.61:8091/api/gec/check"
    r = requests.post(url=url_check, headers=headers, data=data_check)
    result = r.json()
    return result, result["essay"]["origin"], result["essay"]["correct"], result["essay"]["problem_detail"], result["essay"]["origin_html"]


class RecordsApi(Resource):

    @auth.login_required
    def post(self):

        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")

        # TODO： 这里调用计算函数
        articleTitle = req.get("title")
        articleContent = req.get("article")# 拿到数据


# ******计算各种得分********
        from result_code.score_forTrain_old import wenmind_score
        from result_code.LDA_final import LDA
        import math
        import time

        # TODO 修改路径
        dict_word_level_path = r"app/resources/algorithm/dict_word_level.json"

        # TODO 这里初始化了一个作文评分的类，我想可以把这个类初始化在init里
        wenmind = wenmind_score(dict_word_level_path)

        print("重新计时")

        t1 = time.time()
        fenJu_WenZhang = []
        fenCi_WenZhang = []
        paragragh_WenZhang = []

        # juFa_WenZhang=[]
        corrected_wenzhang = []

        essay = articleContent
        # 对文章进行分句
        fenCi_WenZhang = wenmind.ssplit_tokenize(essay)

        print("运行时间")
        print(time.time()-t1)

        word_score, fenbu, totalWord_num = wenmind.word(
            fenCi_WenZhang)
        hsk_fenbu = fenbu.copy()
        # # 求词汇水平的打分，是对这篇文章之中不重复的词，找出其hsk难度，求平均
        # # 并给出词汇难度的分布
        print("词汇裸分："+str(word_score))
        word_trueScore = math.pow(word_score / 6, 0.24) * 5
        print("词汇真实分："+str(word_trueScore))

        print("运行时间")
        print(time.time() - t1)

        # 获得改错
        paragragh = "|"
        origin, corrected, problem_detail, origin_html = wenmind.correct_byWenXin(
            paragragh.join(essay.split("\n")))
        huanhang = "\n"
        print(origin_html)
        print("错误个数")
        # corrected = str(huanhang.join(corrected_wenzhang))
        incorrect_num = len(origin_html.split("</span>")) - 1
        print("错误个数" + str(incorrect_num))
        incorrect_possibility = incorrect_num / totalWord_num
        print("错词率：" + str(incorrect_possibility))

        incorrect_trueScore = (
            1 - math.pow(incorrect_possibility, 0.33)) * 5
        print("错误真实分：" + str(incorrect_trueScore))

        print("运行时间")
        print(time.time() - t1)

        # 获得句法打分
        juFaTree_Score, conjunction_score, avg_len = wenmind.juFa(
            fenCi_WenZhang)
        print("句法树裸分："+str(juFaTree_Score))
        conjunction_score = conjunction_score / avg_len
        print("连接裸分："+str(conjunction_score))
        print("句长裸分："+str(avg_len))

        if(juFaTree_Score > 20):
            juFaTree_Score = 20
        if(avg_len > 28):
            avg_len = 28

        juFaTree_trueScore = math.pow(juFaTree_Score / 20, 0.42) * 5
        conjunction_trueScore = math.pow(conjunction_score, 0.17) * 5
        avg_truelen = math.pow(avg_len / 28, 0.73) * 5

        print("句法树真实分："+str(juFaTree_trueScore))
        print("连接真实分："+str(conjunction_trueScore))
        print("句长真实分："+str(avg_truelen))

        juFa_trueScore = (juFaTree_trueScore +
                        conjunction_trueScore + avg_truelen) / 3
        print("句法真实分："+str(juFa_trueScore))

        print("运行时间")
        print(time.time() - t1)

        LDA_sim = LDA(articleTitle, essay)
        print(LDA_sim)

        print("运行时间")
        print(time.time() - t1)

        result = {
            "essay": essay,
            "articleTitle": articleTitle,
            "word_score": word_score,
            "LDA_sim": LDA_sim,
            "incorrect_possibility": incorrect_possibility,
            "origin_html": origin_html,
            "word_trueScore": word_trueScore,
            "juFa_trueScore": juFa_trueScore,
            "incorrect_trueScore": incorrect_trueScore,
            "LDA_trueSim": LDA_sim * 5,
        }
# *************************


# ******************************ztz 添加的代码**************************************************
        # 输入UTF8编码文章，输出词汇难度，句法难度，修改错别字
        fenJu_WenZhang = []
        fenCi_WenZhang = []
        # juFa_WenZhang = []
        corrected_wenzhang = []

        ciBiao_Path = r"app/resources/algorithm/hsk_word.txt"
        filePath = r"app/resources/algorithm/作文_卢.txt"
        # stanfordPath = r"/root/stanfordCoreNlp/stanford-corenlp-full-2018-10-05"
        dict_word_level_path = r"app/resources/algorithm/dict_word_level.json"
        import sys

        # 对文章进行分句
        fenJu_WenZhang, wenzhang, paragragh_WenZhang = al.cut(articleContent)

        fenCi_WenZhang = al.cut_word(fenJu_WenZhang, ciBiao_Path)
        # 对每一句话进行分词
        # 使用jieba，添加hsk词入新增词表
        word_score, fenbu = al.word(fenCi_WenZhang, dict_word_level_path)
        # 求词汇水平的打分，是对这篇文章之中不重复的词，找出其hsk难度，求平均
        # 并给出词汇难度的分布
        # print("词汇打分："+str(word_score))

        # juFa_Score = al.juFa(fenJu_WenZhang, stanfordPath)
        # 根据standfordCoreNlp的parse生成句法树
        # 根据句法树的高度给出打分
        # print("句法打分："+str(juFa_Score))
        juFa_Score = random.random() * 5
        import sys

        # womendewenzhang = al.correct(fenJu_WenZhang)

        paragragh = "|"
        correct_result_json, origin, corrected, problem_detail, origin_html = correct_byWenXin(paragragh.join(paragragh_WenZhang))
        wrong_words = []
        for word in problem_detail:
            origin_text = word['origin_text']
            origin_text_html = word['origin_text_html']
            correct_text = word['correct_text']
            correct_text_html = word['correct_text_html']
            origin_start_index = word['origin_start_index']
            origin_end_index = word['origin_end_index']
            correct_start_index = word['correct_start_index']
            correct_end_index = word['correct_end_index']
            create_time = word['create_time']
            update_time = word['update_time']
            problem_type_zh = word['problem_type_zh']
            problem_type_en = word['problem_type_en']
            paragraph_index = word['paragraph_index']
            sentence_index = word['sentence_index']
            problem_status = word['problem_status']
            corpus_id = word['corpus_id']
            token_array = word['token_array']
            token_str = word['token_str']
            token_strs = word['token_strs']
            wrong_words.append(origin_text)

# ***************************************************************************************************************
        # 查字典V1
        # file = open("app/resources/xdhydcd_json_data.json", 'r', encoding='UTF-8')
        # new_dict = {}  # {"你好"：{"pinyin":"nihao", "main":[{}..]}}
        # for data in file.readlines():
        #     dic = json.loads(data)
        #     if not new_dict.get(dic['word']):
        #         new_dict[dic['word']] = {}
        #         new_dict[dic['word']]['main'] = dic['main']
        #         new_dict[dic['word']]['pinyin'] = dic['pinyin']
        # file.close()
        # suggestion = {}  # dict includes dicts
        # for wrong_word in wrong_words:
        #     if not new_dict.get(wrong_word):
        #         continue
        #     suggestion[wrong_word] = new_dict[wrong_word]
        # suggestion = json.dumps(suggestion)
        #查字典V2
        suggestion={}
        file=open("app/resources/hsk_dic.json","r")
        new_dict=json.load(file)
        for wrong_word in wrong_words:
            modified_list=[]
            if not new_dict.get(wrong_word):
                continue
            cnt=0
            for sen in new_dict[wrong_word]:
                if cnt==5:
                    break
                modified_sen=[]
                modified_sen.append(sen[0])
                replaced_sen1=sen[1].replace(wrong_word,'<span+class="example_key">' + wrong_word + '</span>')
                temp_sen="".join(replaced_sen1.split(" "))
                fi_replaced=temp_sen.replace("+"," ")
                modified_sen.append(fi_replaced)
                modified_sen.append(sen[2])
                modified_sen.append(sen[3])
                modified_list.append(modified_sen)
                cnt+=1
            suggestion[wrong_word]=modified_list
        suggestion=json.dumps(suggestion)


# *******************************************************************************************************************
        # 计算TWE文本相似度（主题得分）
        # from app.resources.query_doc_sim import query_doc_sim
        # similary = query_doc_sim(articleTitle, articleContent)
        similary = random.random() * 5
        # print("reach")
# *******************************************************************************************************************

        # 输出到页面上
        vocabularyLevel = round(result["word_trueScore"], 1)
        titleRelativity = round(result["LDA_trueSim"], 1)
        incorrectScore = round(result["incorrect_trueScore"], 1)
        sentenceDifficulty =  round(result["juFa_trueScore"], 1)
        articleComment  = origin_html
        #得出文章篇幅分数
        temp=len(essay)
        length_score=0
        if temp > 0 and temp <= 200:
            length_score=1
        if temp > 200 and temp <= 300:
            length_score =2
        if temp > 300 and temp <= 400:
            length_score = 3
        if temp > 400 and temp <= 500:
            length_score = 4
        if temp > 500:
            length_score = 5
        totalScore = round(
            (0.29868224  * titleRelativity * 5) + (8.92161381  * vocabularyLevel) + (2.90256939  * sentenceDifficulty) + (
                    6.4802768 * incorrectScore) +(0.45716631*length_score)- 0.646608914288862, 1)
        # articleComment = huanhang.join(original_wenzhang)# 带有标记的原文章放到原文点评（zhy）
        # suggestion = "先草率地随意留个提升建议"
        # vocabularyDevelopment = str(ans)
        print("hsk: ", hsk_fenbu)
        print("篇幅分数:",length_score)
        for i in range(7):
            try:
                tm_string=hsk_fenbu[i]
            except:
                hsk_fenbu[i]=0
        hsk1 = hsk_fenbu[1]
        hsk2 = hsk_fenbu[2]
        hsk3 = hsk_fenbu[3]
        hsk4 = hsk_fenbu[4]
        hsk5 = hsk_fenbu[5]
        hsk6 = hsk_fenbu[6]
        r = RecordModel(articleTitle, articleContent, totalScore, vocabularyLevel, titleRelativity, incorrectScore, sentenceDifficulty,length_score ,articleComment, suggestion, hsk1, hsk2, hsk3, hsk4, hsk5, hsk6, g.user.id)
        r.add_record()
            
        for word in problem_detail:
            origin_text = word['origin_text']
            origin_text_html = word['origin_text_html']
            correct_text = word['correct_text']
            correct_text_html = word['correct_text_html']
            origin_start_index = word['origin_start_index']
            origin_end_index = word['origin_end_index']
            correct_start_index = word['correct_start_index']
            correct_end_index = word['correct_end_index']
            create_time = word['create_time']
            update_time = word['update_time']
            problem_type_zh = word['problem_type_zh']
            problem_type_en = word['problem_type_en']
            paragraph_index = word['paragraph_index']
            sentence_index = word['sentence_index']
            problem_status = word['problem_status']
            corpus_id = word['corpus_id']
            token_array = word['token_array']
            token_str = word['token_str']
            token_strs = word['token_strs']
            problem_detail_data = WrongCharModel(origin_text, origin_text_html, correct_text, correct_text_html, origin_start_index, origin_end_index, correct_start_index, correct_end_index, create_time, update_time, problem_type_zh, problem_type_en, paragraph_index, sentence_index, problem_status, corpus_id, token_array, token_str, token_strs, r.id)   # 这边要装此次的record id, 但是不知道为什么g.user.id不行（zhy）
            problem_detail_data.add_wrongchar_record()

        # 将correct结果的json存为文件
        # 以 correct_record的id 命名
        with open('app/resources/correct_jsons/correct_' + str(r.id) + '.json', 'w') as f:
            json.dump(correct_result_json, f)
        # print(correct_result_json)

        return jsonify(code = 200, message = "成功", recordId = r.id)

    @auth.login_required
    def get(self):

        records = g.user.records
        if records is None:
            return jsonify(code = 200, message = "该用户无评分记录")

        data = []

        for record in records:
            data.append(
                {
                "recordId": record.id,
                "commitTime": record.commit_time,
                "articleTitle": record.article_title,
                "articleContent": record.article_content,
                "totalScore": record.total_score
                }
            )
        # 返回文章内容
        return jsonify(code = 200, message = "成功", records = data)
