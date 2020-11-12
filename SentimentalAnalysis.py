import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
import os 
import json
import time

okt = Okt()
OpinionReport = {}
def min_max_normalize(lst): #  min, Max 를 이용한 정규화 : 리스트를 넣으면 정규화된 값으로 반환함
    normalized = []
    normalizedlist = []
    for value in lst:
        normalized_num = (value - min(lst)) / (max(lst)-min(lst))
        normalizedlist.append(normalized_num)
    return normalizedlist

with open('C:/Users/b_jun/언어 감성 분석/data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
        data = json.load(f)

path_dir = "C:/Users/b_jun/언어 감성 분석/증권경시대회_20.11.11"
file_list = os.listdir(path_dir)
file_list.sort() # 파일 리스트 가져오기
et = 0
for n, j in enumerate(file_list):  # i 는 0부터 되어 있는 변수임
    n += 134
    et += 1
    if et > 20:
        time.sleep(30)
        et = 0
    rawperiod = str(re.findall(r'•(.*?)_', file_list[n]))
    rawCreator = str(re.findall(r'._(.*?)_', file_list[n]))
    parse = re.sub('[-=.#/?:$}\[\]]', '', rawperiod)
    parse = re.sub(' ', '-',parse)
    Date = parse
    parse2 = re.sub('[-=.#/?:$}\[\]]', '', rawCreator)
    CreatorName = parse2
    # 가져오기
    FileName = file_list[n]
    train_data = pd.read_table('C:/Users/b_jun/언어 감성 분석/증권경시대회_20.11.11/{}'.format(FileName), index_col=False, header=None)
    # 중복 확인 및 제거,아래 식은 중복이 없는 데이터의 수를 나타냄
    train_data.index.nunique(),  train_data[0].nunique()
    train_data.drop_duplicates(subset=[0], inplace=True)
    # 한글을 제외하고 전부 제거
    train_data[0] = train_data[0].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    # 빈행을 null으로 대체 후 제거
    train_data[0].replace('', np.nan, inplace=True)
    print(train_data.isnull().sum())
    train_data = train_data.dropna(how = 'any')
    print(len(train_data))
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    X_train = [] # 다시 빈 데이터
    for sentence in train_data[0]:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True) # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
        X_train.append(temp_X) 
    # 하나의 리스트로 바꾸기
    WordsFromTest = []
    for i in range(len(X_train)):
        for w in X_train[i]:
            WordsFromTest.append(w)
    NumtotalSentient = 0 # 전체 감성어 수 
    Totalwordlen = len(WordsFromTest)  # 전체 단어 개수
    CountNone = 0 # 감성어 아닌 수
    CountPos = 0 # 긍정어 수
    CountNeg = 0 # 부정어 수 
    CountNuetral = 0 # 중립어 수
    TotalGrade = 0 # 전체 점수 
    NormalizedGrd = 0 # 정규화 된 점수
    GradeList = []
    # with open('C:/Users/b_jun/언어 감성 분석/data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
    for wordname in WordsFromTest:
        for i in range (0, len(data)):
            if data[i]['word'] == wordname:
                NumtotalSentient += 1
                rawgrade = float(data[i]['polarity'])
                GradeList.append(rawgrade)
                if rawgrade > 0:
                    TotalGrade += int(data[i]['polarity'])
                    CountPos += 1
                elif rawgrade == 0:
                    TotalGrade += int(data[i]['polarity'])
                    CountNuetral += 1
                elif rawgrade < 0:
                    TotalGrade += int(data[i]['polarity'])
                    CountNeg += 1 
    Normal_List_Sum = sum(min_max_normalize(GradeList))
    FinalOpinion = Normal_List_Sum/ NumtotalSentient
    OpinionReport[n] = {
                          "Creator":CreatorName, 
                          "Date":Date,
                          "Totalword":Totalwordlen,
                          "totalSenti":NumtotalSentient,
                          "CountPos":CountPos,
                          "CountNuetral":CountNuetral,
                          "CountNeg":CountNeg,
                          "TotalGrade":TotalGrade,
                          "TotalOpinion":Normal_List_Sum,
                          "FinalOpinion":FinalOpinion,
                          }
    

OpinionReport2 = pd.DataFrame.from_dict(OpinionReport, orient='index') 
OpinionReport2.to_excel('C:/Users/b_jun/언어 감성 분석/FinalData/{}.xlsx'.format(CreatorName))  
Youtubelist = pd.DataFrame(file_list) 
Youtubelist.to_excel('C:/Users/b_jun/언어 감성 분석/FinalData/{}_리스트.xlsx'.format(CreatorName)) 
# rawperiodList = []
# rawCreatorList= []
# periodList = []
# CreatorList= [] 
# parse1=""
# parse2 = ""
# n = 0
# for i, j in enumerate(file_list):
#     rawperiodList.append(str(re.findall(r'•(.*?)_', file_list[i])))
#     rawCreatorList.append(str(re.findall(r'._(.*?)_', file_list[i])))
# for i, j in zip(range(len(rawperiodList)), range(len(rawCreatorList))):
#     text = rawperiodList[i]
#     parse = re.sub('[-=.#/?:$}\[\]]', '', text)
#     parse = re.sub(' ', '-',parse)
#     periodList.append(parse)
#     text2 = rawCreatorList[j]
#     parse2 = re.sub('[-=.#/?:$}\[\]]', '', text2)
#     CreatorList.append(parse2)

              
