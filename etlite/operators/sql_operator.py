""" This class functions as a bridge between RestAPI and Database
    
    TODO:
    1)rename package/files/classes ?
    2)use Constants
    3)tests for different db uris

"""
import  os
import  sys
sys.path = [os.getcwd()] + sys.path

from    etlite.common.base_etl  import  BaseEtl
from    etlite.common   import cfg

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm.session import sessionmaker

class SqlOperator():
    # TODO: support actions such as 'update'...
    def __init__(self, db_name:str, tb_name:str, data_list:list, action="insert"):
        if db_name not in cfg['database']:
            raise ValueError("Please specify database name in the config file ! ")
        
        # TODO: error checking
        self.engine = self._get_engine(db_name)
        self.table = self._get_tb_instance(tb_name)
        self.data_list = [ data[0].split(BaseEtl.DELIMITER) for data in data_list ]
        self.mappings = self._build_mappings()
        self.action = action
        print()
        print(self.mappings)

    def _build_uri(self): pass

    def _get_engine(self, db_name):
        # TODO: 1)try to get uri parameter 
        #       2)if not provided, construct the uri using connection infos(user, pw...)
        uri = cfg['database'][db_name]['uri']

        # TODO: checking db connection
        return create_engine(uri, echo=False)
        
    def _get_tb_instance(self, tb_name):

        metadata = MetaData()
        metadata.reflect( bind= self.engine )
        if tb_name not in metadata.tables:
            raise ValueError(f"Table '{tb_name}' does not exist ! ")
        return metadata.tables[tb_name]
        
    def _build_mappings(self) -> list:
        # TODO: 1)validate the inputs
        columns = [ ( col.name, str(col.type) ) for col in self.table.columns ]
        mappings = []
        for data in self.data_list:
            mapping = {}
            for i, value in enumerate(data):
                # SHOULD check colomn type instead of index
                mapping[columns[i][0]] = int(float(value)) if (i == 3) else value
            mappings.append(mapping)
        return mappings        

    def execute(self):
        if self.action == "insert":
            self.insert()
        elif self.action == "update":
            pass

    def insert(self):
        if not self.mappings or not isinstance(self.mappings, list):
            raise ValueError("Invalid mappings: is null, empty or not a list !")

        result = self.engine.execute(self.table.insert(None), self.mappings)
        print(f"{result.rowcount} rows inserted")
        return result

    def create(self):   pass
    def update(self):   pass
    def delete(self):   pass
 
if __name__ == "__main__": 

    db_name = "postgres"
    tb_name = "weather"
    data_list = [['Beijing\tCN\tclear sky\t268.27'], ['Tokyo\tJP\tfew clouds\t281.51']]

    try:
        so = SqlOperator(db_name, tb_name, data_list)
        so.execute()
    except Exception as ex:
        print(ex)
