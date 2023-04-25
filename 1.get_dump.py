
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
db.createEngine()
db.toSql(data)