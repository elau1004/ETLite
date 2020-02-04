"""
    this script loads a class file, instantiates object from the file
    and run methods of the class
    TODO: log all error messages instead raising errors
"""
import os
import sys
import importlib
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/sample.
import sample.create_job_file as cjf
import sample.constants as constants

# TODO: allow arguments to be passed when instantiating the class
def instantiate_class(file_name:str)->object:
    try:
        # saves the current dir so we can move back
        # after class is instainiated
        cwd = os.getcwd() 
        os.chdir(constants.JOBS_DIR) 
        sys.path.append(constants.JOBS_DIR) 
        get_class = None
        if os.path.exists(file_name):
            class_name = file_name[:-3]  # remove .py extension
            mod = importlib.import_module(class_name)
            get_class = getattr(mod, class_name)
        else:
            err_msg = f"{file_name} does not exist in {constants.JOBS_DIR}!"
            raise ValueError(err_msg)
        # restore current dir
        os.chdir(cwd)
        # remove the dynamic import path from sys
        _ = sys.path.pop()

        if get_class:  
            instance = get_class()
            print(f"\nInstance created: {instance}")
            return instance
        else:
            err_msg = f"Unable to get class for {file_name}"
            raise ValueError(err_msg)
    except Exception as ex:
        err_msg = f"\nUnable to instantiate : {file_name}\n{ex}"
        raise ValueError(err_msg)

def check_instance(s:object):
    from etlite.common.base_etl import BaseEtl
    from etlite.common.base_restapi_etl import BaseRestApiEtl
    from sample.base_sample_restapi_etl  import  BaseSampleRestApiEtl

    print(f"Checking instance...")
    if  isinstance( s ,BaseEtl ):
        print( "It is Base ETL")

        if  isinstance( s ,BaseRestApiEtl ):
            print( "It is Base RestApi ETL")

            if  isinstance( s ,BaseSampleRestApiEtl ):
                print( "It is Base Sample RestApi ETL")
    else:
        print( "Bummer!" )

def create_instantiate(protocol:str, job_name:str):
    # for now we use REST API as our default protocol
    file_path = cjf.create_file(protocol, job_name)
    obj = instantiate_class(os.path.basename(file_path))
    check_instance(obj)
    print(f"Calling one of the methods...")
    print(f"obj.get_next_datapage_url()={obj.get_next_datapage_url()}")

def test_instantiate_class(file_name:str):
    assert instantiate_class(file_name) != None 

def main():
    create_instantiate(constants.PROTOCOL_REST_API, "IBM")
    
if __name__ == "__main__":
    main()