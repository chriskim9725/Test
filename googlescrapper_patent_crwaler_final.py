# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 19:43:46 2022

@author: 김근수
"""
from googlepatentscraper.document import Document
from tqdm import tqdm
import time
import pandas as pd
import numpy as np





#%%crawling function
def patent_crawling(df):
    data = pd.DataFrame(df["id"],columns=["id"])
    data["id"] = data["id"].replace("-","",regex=True)
    data["dic"] = ""
    data["patent_citations"] = ""
    for i, data_id in enumerate(tqdm(data["id"])): # googlepatentscraper 적용 후 저장
        try:
           patent = Document(data_id)
           data["dic"].loc[i] = patent.data
           data["patent_citations"].loc[i] = patent.data["backward_citations"]
        except:
            print("error")
            data["dic"].loc[i] = None
            data["patent_citations"].loc[i] = None
            pass
    return data

def patent_make_table(patent,patent_final_temp,attribution_want):
    patent_temp = []
    for i in patent.index:
        try:
            patent_temp=(patent["dic"][i][attribution_want])
            patent_temp_df = patent_temp.to_frame()
            patent_temp_df = patent_temp_df.transpose()
            patent_final_temp = patent_final_temp.append(patent_temp_df)
            patent_final_temp = patent_final_temp.reset_index(drop=True)
        except:
            print("error2")
            patent_final_temp.loc[i] = None
            pass
    return patent_final_temp


def get_cited_patent(patent):
    
    cited_num = patent["patent_citations"] # object -> dict 형 변환
    cited_num_list = []

    for cited_dic in cited_num:
        #print(cited_dic)
        for cited_dic_number in cited_dic:
            #print(cited_dic_number)
            if "US" in cited_dic_number["publiationNumber"]: # US 특허만 사용
                cited_num_list.append(cited_dic_number["publiationNumber"]) 
                
    cited_nums = list(set(cited_num_list)) # 특허 중복제거 42858 -> 19327
    
    return cited_nums

#%%patent number를 가지고 크롤링하기 
pat_num = pd.read_excel('D:/Practice_python/2_patenCrawling/Data/0.HEV/googlepatent_HEV_1990-2021_grantdate.xlsx',sheet_name = '1990-2021') # patent number리스트 파일 불러오기
patent = patent_crawling(pat_num)
pat_nums = list(patent["id"])


attribution_sample = patent["dic"][0] # 가지고 있는 특허 정보리스트
attribution_want = ["title","abstract","cpcs"] #추출하고 싶은 특허 정보리스트
patent_final_temp = pd.DataFrame(columns=attribution_want) #attribution_want를 column으로 가진 빈 DF

patent_final = patent_make_table(patent, patent_final_temp, attribution_want)
patent_final.insert(0, "id" ,patent["id"]) #id값 맨 앞으로 추가해주기

patent_final.to_excel('D:/Practice_python/2_patenCrawling/Data/0.HEV/Output/Result_1990-2021_HEV.xlsx', index=False) #원하는 경로와 파일명을 적어주세요


#%% cited 관계 특허 추출 후 전체 특허의 정보 추출 
#pat_num = pd.read_excel('D:/Practice_python/2_patenCrawling/Data/0.HEV/Output/Result_1990-2021_HEV.xlsx',header=1)
#pat_nums = list(pat_num["id"])
cited_nums = get_cited_patent(patent)
print("load_citation Patent")

total_pat_num = pd.DataFrame(pat_nums + cited_nums, columns = ["id"])

#%% 기존의 특허정보 + cited관계 특허 정보 
patent = patent_crawling(total_pat_num)
attribution_sample = patent["dic"][0] # 가지고 있는 특허 정보리스트
attribution_want = ["title","abstract","cpcs"] #추출하고 싶은 특허 정보리스트
patent_final_temp_citation = pd.DataFrame(columns=attribution_want) #attribution_want를 column으로 가진 빈 DF

patent_final_with_citations = patent_make_table(patent, patent_final_temp_citation, attribution_want)
patent_final_with_citations.insert(0, "id" ,patent["id"]) #id값 맨 앞으로 추가해주기

patent_final_with_citations.to_excel('D:/Practice_python/2_patenCrawling/Data/0.HEV/Output/Result_1990-2021_HEV_citation.xlsx', index=False) # 원하는 경로와 파일명을 적어주세요







#%% Garbage
#patent_final["id"] = patent["id"]


#[patent_final[list(patent_final)[1]] 
'''
patent_temp =[]
for i in patent.index:
    for attrs in attribution_want:
        patent_temp[0].append(patent["dic"][i][attrs])
    
patent_final[list(patent_final)[0]] =pd.DataFrame(patent_temp)   
'''
#patent["dic"][0].index





#list(patent["dic"][0].index)
#"title","cpcs" in list(patent["dic"][0].index)





'''
a = patent["dic"][0][attribution_want] 

b = a.to_frame()
c= b.transpose()



patent_temp_df.values[1]=patent_temp_df.values
pat_num.loc[3] = pat_num.values[0]

patent_final = patent_final.append(patent_temp_df)
'''