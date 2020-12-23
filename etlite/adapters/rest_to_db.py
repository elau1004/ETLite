""" This class functions as a bridge between RestAPI and Database
    
"""
#import sqlalchemy as sa
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm.session import sessionmaker

import  os
import  sys
sys.path = [os.getcwd()] + sys.path
from    etlite.common.base_etl  import  BaseEtl

class BaseAdapter():    pass
class DBAdapter(BaseAdapter):
    
    @staticmethod
    def build_mapping(dataLists:list) -> list:
        # TODO: validate the inputs
        # Fix this !
        columns = [ "city","country", "discription", "temp"]
        mappings = []
        for dataList in dataLists:
            tokens = dataList[0].split(BaseEtl.DELIMITER)
            mapping = {}
            for idx, token in enumerate(tokens):
                if idx == len(tokens) - 1:
                    mapping[columns[idx]] = int(float(token))
                else:
                    mapping[columns[idx]] = token
            mappings.append(mapping)
        return mappings

class RestToDB(DBAdapter):
    def __init__(self, mappings:list, tb_name:str):
        if not mappings or not isinstance(mappings, list):
            raise ValueError("Invalid mapping object: is null, empty or not a dictionary !")
        self.mappings = mappings
        # Fix this !
        self.uri = 'postgresql://test:test@localhost/test'
        print("uri:", self.uri)
        self.engine = create_engine(self.uri, echo=False)
        metadata = MetaData()
        metadata.reflect( bind= self.engine )
        # validate tb_name
        self.table = metadata.tables[tb_name]
        
        
    def core_insert(self):
        result = self.engine.execute(self.table.insert(None), self.mappings)
        print(f"{result.rowcount} rows inserted")
        return result

    def run_rawsql(self, query:str):
        pass
 
if __name__ == "__main__": 

    uri = 'postgresql://test:test@localhost/test'
    engine = create_engine(uri, echo=False)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    print(metadata.tables)
    weather = metadata.tables['weather']
    print(type(weather))
    print(weather)
