
from mysql import connector
import pymysql
from sqlalchemy import create_engine
from pandas.errors import DatabaseError

import pandas as pd
import os

class Database :
    
    def __init__(self) :
        self.database = 'vision'
        self.host = '52.79.134.175'
        self.port = '57472'
        self.user = 'yangheelee'
        self.password = 'dldidgml'

    def createEngine(self) :
        self.server = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        self.engine = create_engine(self.server)

    def toSql(self,df:pd.DataFrame,tb:str='raw_data') :
        try :
            df.to_sql(name=tb,con=self.engine,if_exists='replace',index=False)
        except ValueError as e :
            print(f'!!!!!!!! Error Occured: {e}')
    
    def openDB(self) :
        self.connector = connector.connect(
            database=self.database
            , host=self.host, port=self.port
            , user=self.user, password=self.password
        )
        self.cursor = self.connector.cursor()

    def closeDB(self) :
        self.cursor.close()
        self.connector.close()

    def select(self,query:str) : pass

    def insert(self,query:str) :
        self.openDB()
        self.cursor.execute(query)
        self.connector.commit()
        self.closeDB()

    def delete(self,query:str) : pass
    def update(self,query:str) : pass

    def create(self,query:str) : 
        self.openDB()
        self.cursor.execute(query)
        self.connector.commit()
        self.closeDB()

    def createRawData(self) : 
        query = 'create table raw_data ('
        query += 'id                        int unsigned primary key auto_increment'
        query += ',unnamed                  int'
        query += ',parent_marital_status    varchar(255)'
        query += ',parent_educ              varchar(255)'
        query += ',is_first_child           varchar(255)'
        query += ',nr_siblings              float'
        query += ',gender                   varchar(255)'
        query += ',ethnic_group             varchar(255)'
        query += ',transport_means          varchar(255)'
        query += ',lunch_type               varchar(255)'
        query += ',practice_sport           varchar(255)'
        query += ',wkly_study_hours         varchar(255)'
        query += ',test_prep                varchar(255)'
        query += ',math_score               int'
        query += ',reading_score            int'
        query += ',writing_score            int'
        query += ',created_datetime         datetime default now()'
        query += ',updated_datetime         datetime on update now()'
        query += ')'
        self.create(query)

    def insertRawData(self,dt:pd.DataFrame) : 
        for idx, row in dt.iterrows() :
            query = 'insert into raw_data ('
            query += 'unnamed,parent_marital_status,parent_educ,is_first_child,nr_siblings,gender,ethnic_group,transport_means,lunch_type,practice_sport,wkly_study_hours,test_prep,math_score,reading_score,writing_score'
            query += ')'
            query += ' values ('
            query += ','.join(['null' if pd.isna(row[col]) else f'"{row[col]}"' for col in dt.columns])
            query += ')'
            self.insert(query)


path = './data/'
file = 'Expanded_data_with_more_features.csv'
path_file = os.path.join(path,file)
data = pd.read_csv(path_file)

columns_ordered = [
    'Unnamed: 0'
    , 'ParentMaritalStatus', 'ParentEduc'
    , 'IsFirstChild', 'NrSiblings'
    , 'Gender', 'EthnicGroup'
    , 'TransportMeans', 'LunchType'
    , 'PracticeSport', 'WklyStudyHours', 'TestPrep'
    , 'MathScore', 'ReadingScore', 'WritingScore'
]
data = data.reindex(columns=columns_ordered)

db = Database()

# db.createEngine()
# db.toSql(data)

db.createRawData()
db.insertRawData(data)