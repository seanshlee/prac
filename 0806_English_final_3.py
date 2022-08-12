# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 09:25:47 2022

@author: Master
"""
#!pip install konlpy
import nltk
from nltk import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags, ne_chunk
from pprint import pprint
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
import re
from nltk.stem import WordNetLemmatizer

from konlpy.tag import Okt 
import numpy as np
from konlpy.tag import Okt 
from collections import Counter #빈도 탐색 
from konlpy.tag import * 
#hannanum = Hannanum()
okt = Okt()

df1 = pd.read_csv("C:/Users/Master/Busan_Travel_180701.csv")
df2 = pd.read_csv("C:/Users/Master/Busan_Travel_20200327.csv")
df3 = pd.read_csv("C:/Users/Master/shap_Busan_space_Travel.csv")
df4 = pd.read_csv("C:/Users/Master/shap_BusanTravel.csv")


df_all = pd.concat([df1,df2,df3,df4])


#### 말뭉치 생성
df_all_corpus = ''.join(map(str, df_all['main_text']))



############################################################ 특수문자 제거 ########################################################
def remove_special_character(phrase, remove_number=False):
  """remove_special_character takes text and removes special charcters.
     ref: https://stackoverflow.com/a/18082370/4084039"""

  phrase = re.sub("\S*\d\S*", "", phrase).strip()
  if remove_number:
    phrase = re.sub('[^A-Za-z]+', ' ', phrase)
  else:
    phrase = re.sub('[^A-Za-z0-9]+', ' ', phrase)
  return phrase


df_all_corpus = remove_special_character(df_all_corpus, True)

df_all_corpus


############################# 축약형 natural로 바꾸기 ##############################################
def decontracted(phrase):
  """decontracted takes text and convert contractions into natural form.
     ref: https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python/47091490#47091490"""

  # specific
  phrase = re.sub(r"won\'t", "will not", phrase)
  phrase = re.sub(r"can\'t", "can not", phrase)
  phrase = re.sub(r"won\’t", "will not", phrase)
  phrase = re.sub(r"can\’t", "can not", phrase)

  # general
  phrase = re.sub(r"n\'t", " not", phrase)
  phrase = re.sub(r"\'re", " are", phrase)
  phrase = re.sub(r"\'s", " is", phrase)
  phrase = re.sub(r"\'d", " would", phrase)
  phrase = re.sub(r"\'ll", " will", phrase)
  phrase = re.sub(r"\'t", " not", phrase)
  phrase = re.sub(r"\'ve", " have", phrase)
  phrase = re.sub(r"\'m", " am", phrase)

  phrase = re.sub(r"n\’t", " not", phrase)
  phrase = re.sub(r"\’re", " are", phrase)
  phrase = re.sub(r"\’s", " is", phrase)
  phrase = re.sub(r"\’d", " would", phrase)
  phrase = re.sub(r"\’ll", " will", phrase)
  phrase = re.sub(r"\’t", " not", phrase)
  phrase = re.sub(r"\’ve", " have", phrase)
  phrase = re.sub(r"\’m", " am", phrase)

  return phrase

df_all_corpus  = decontracted(df_all_corpus)
df_all_corpus



#########################################  url 제거  ###############################3

def remove_url(text_data):
  """remove_url takes raw text and removes urls from the text.
     https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python/40823105#40823105
     """
  return re.sub(r"http\S+", "", text_data)

df_all_corpus = remove_url(df_all_corpus)

dfl = df_all_corpus.split() ############### 문자열을 리스트로 
dfl

dfd = pd.DataFrame(dfl) ############## 리스트를 데이터프레임으로 
dfd.head()


dfd.columns = ['words']
dfd.head()


#lwc = wc.to_list() ################### 시리즈를 리스트로 

#글자 수 열 추가하기 

###############  글자 수 세기 함수 
def count_character(data):
    count = 0
    for i in data :
        count += len(i)
    return  count

listw = []

for i in range(0,len(dfd)): 
    text = dfd.iloc[i,0]
    s = count_character(text)
    listw.append(s)
    
type(listw)
lwc = pd.DataFrame(listw)

lwc.columns = ['wc']

df_ = pd.concat([dfd,lwc], axis = 1)
df_.head()

#####################################################     단어 글자 수가 1글자인 행 삭제하기 
dfc_ = df_[df_.wc > 1]

######################################## 불용어 삭제하기 ############################################
#nltk.download('stopwords')
from nltk.corpus import stopwords
#stopwords.words('english')[ :10]
dfc_.head()

stop_words = set(stopwords.words('english'))

fsw = dfc_['words'].to_list()

fsw

wosw = [] #without stopwords
for w in fsw:
    if w not in stop_words:
        wosw.append(w)

wosw
wosw = pd.DataFrame(wosw)
wosw.columns = ['words']

wosw.head() #1글자인 행, 불용어가 제거된 df

len(wosw)

######################################### 품사 태깅  
posl = wosw['words'].to_list()  ################## 시리즈를 리스트로 
poss = " ".join(posl) #poss = 리스트를 문자열로
poss = poss.lower() #모두 소문자로 변환 
poss

#tnd = tokenized
tnd = pos_tag(word_tokenize(poss)) #품사 태깅 완료(poss사용)
tnd_df = pd.DataFrame(tnd)
tnd_df.head()
tnd_df.columns = ['words','pos']

#개체명 인식하기 
#ne_poss = ne_chunk(tnd)
#type(ne_poss)

tnd_df.head()


###############################################    원형으로 바꾸기 
lm = WordNetLemmatizer()

posl_lemma = [lm.lemmatize(w, pos="v") for w in posl]

#type(posl_lemma) #list 
len(posl_lemma)

posl_lemma_str = " ".join(posl_lemma)

#################### 원형으로 바꾼 문자열에 다시 품사 태깅 
tagged = pos_tag(word_tokenize(posl_lemma_str)) #품사 태깅 완료(poss사용)
tagged

tagged_df = pd.DataFrame(tagged)
tagged_df.columns = ['words','pos']

tf = tagged_df['words'].tolist()

################################################ 빈도 넣기 

counter = Counter(tf)

enfreq = counter.most_common(1000)

enfreq_df = pd.DataFrame(enfreq)
enfreq_df.head()
enfreq_df.columns = ['words','freq']

freq = enfreq_df.groupby('words').sum() #freq = dataframe
freq

freq.to_csv("C:/Users/Master/Eng_freq.csv", encoding='utf-8-sig')




























