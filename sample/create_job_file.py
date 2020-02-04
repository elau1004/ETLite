"""
    This script does 3 things:
    1)finds the template file by its protocol
    2)once the file is retrieved, a copy is made 
      to the job files directory
    3)change the class name to the job name ie, IBM
      rename the file to job name
    TODO: recursive file system search if needed
    TODO: log all error messages instead raising errors
"""
import os
import sys
import shutil
import importlib
sys.path = [os.getcwd()] + sys.path # VS Code debugger needs it because it default cwd to {workspace}/sample.
import sample.constants as constants

# helper function rewrites the file and rename the file name
def change_class_name(input_path:str, job_name:str)->str:
    try:
        output_path = f"{constants.JOBS_DIR}{os.sep}{job_name}.py"
        old_name = os.path.basename(input_path)
        with open(input_path) as handle1:
            with open(output_path, "w") as handle2:
                for line in handle1:
                    if line.startswith("class"):
                        idx = line.index("(")
                        part1 = line[:idx]
                        old_name = part1.split()[1]
                        part1 = part1.replace(old_name, job_name)
                        part2 = line[idx:]
                        line = part1 + part2
                    elif old_name in line:
                        line = line.replace(old_name, job_name)
                    handle2.write(line)
        os.remove(input_path)
        return output_path
    except Exception as ex:
        err_msg = f"\nError creating file for job: {job_name}\n{ex}"
        raise ValueError(err_msg)

# this function performs the following tasks:
# 1)find the template file base on the protocol 
# based on protocol provided, ie REST API
# 2)copy the file to the directory for job files
# 3)rewrite the file and rename the file 
#   based on job name ie IBM.py 
# return: abs path of the job file
def create_file(protocol:str, job_name:str)->str:
    try:
        # we can always do a recursive search if needed
        files = os.listdir(constants.TEMPLATE_DIR)
        found = False
        for file_name in files:
            if protocol.lower() in file_name.lower():
                found = True
                src_path = f"{constants.TEMPLATE_DIR}{os.sep}{file_name}"
                # leave the template file alone
                dst_path = f"{constants.JOBS_DIR}{os.sep}CopyOf{file_name}"
                shutil.copy(src_path, dst_path)
                job_file = change_class_name(dst_path, job_name)
                print(f"\nJob file created: {job_file}")
                return job_file
        if not found:
            err_msg = f"\nThere is no matching template file for protocol: {protocol}"
            raise ValueError(err_msg)
    except Exception as ex:
        err_msg = f"\nError in finding templates and copying for protocol: {protocol}\n{ex}"
        raise ValueError(err_msg)

def test_create_file(protocol:str, job_name:str):
    assert create_file(protocol, job_name) != None

def main():
    create_file(constants.PROTOCOL_REST_API, "IBM")
    #test_create_file(constants.PROTOCOL_REST_API, "IBM")
    
if __name__ == "__main__":
    main()