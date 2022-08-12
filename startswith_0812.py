# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 12:45:18 2022

@author: Master
"""
from konlpy.tag import Okt 
import pandas as pd
import re
import numpy as np
from konlpy.tag import Okt 
from collections import Counter #빈도 탐색 
from konlpy.tag import * 
okt = Okt()

df1 = pd.read_csv("C:/Users/Master/블로그_210701.csv")
df2 = pd.read_csv("C:/Users/Master/블로그_210718.csv")
df3 = pd.read_csv("C:/Users/Master/블로그_211028.csv")
df4 = pd.read_csv("C:/Users/Master/블로그_220124.csv")
df5 = pd.read_csv("C:/Users/Master/블로그_220407.csv")

allblogs = pd.concat([df1,df2,df3,df4,df5])

allblogs['main_text']
len(allblogs) #4423

##########################  중복글 제거 
# main_text에 중복이 있는지 확인. 처음 나온 값은 False 이고, 중복값부터 True 반환 
allblogs.duplicated(['main_text'], keep='first')


# keep = 'first' 중복값 중 처음값만 표시
c_allblogs = allblogs.drop_duplicates(['main_text'], keep='first')
len(c_allblogs) #4355


######################################################  특수문자 제거 정규표현식 
def clean_text(inputString):
  text = re.sub('[-=+,#/💙\?:^.@*\"※~ㆍ☆!』‘|\(\)\[\]`\'…》>\”\“\’·👇👊]', ' ', inputString)
  return text


########################################################## 특수문자 제거 반복문 
ct = []

for i in range(0, 4355) :
    sb = clean_text(c_allblogs.iloc[i,4])
    ct.append(sb)
    
len(ct)
ct_df = pd.DataFrame(ct)
ct_df.head()  #ct_df = main_text 열 특수문자 제거됨. 
ct_df.columns = ['main_text']
##############################################################################
########################## 불용어 제거 ########################################

stop_words.columns
sw = stop_words['stopwords']
sw = sw.to_list() #불용어 리스트

sts = ct_df['main_text']
sts = sts.to_list()  #sts = 블로그 원문 리스트 (특수문자, 불용어 제거됨)

[i for i in sts if i not in sw]

######################### 각 행(블로그 별) 마다 형태소로 나눠주고 품사 태깅 
##################  품사 태깅 반복문 
edf = pd.DataFrame()

collector_col = ['nouns', 'verbs', 'adjectives']
a_collector = pd.DataFrame(np.zeros((1, 3)), columns=collector_col)

pos = okt.pos(sts[0])

pdf = pd.DataFrame(pos)
pdf.head()
pdf.columns = ['words', 'pos']

nouns = pdf[pdf.pos == 'Noun']
verbs = pdf[pdf.pos == 'Verb']
adjective = pdf[pdf.pos == 'Adjective']

