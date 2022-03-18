import os
import zipfile
import json
from rocrateValidator.utils import Result as Result

def existence_check(tar_file, extension):
    
    NAME = "File existence"
    error_message = {
        "FileNotFoundError": "Syntax Error: No such file or directory: {}. Validation Aborted."
    }
    
    if os.path.exists(tar_file) == True:
        return Result(NAME)
    else:
        return Result(NAME, code = -1, message = error_message["FileNotFoundError"].format(tar_file))

def file_size_check(tar_file, extension):
    
    NAME = "File size"
    error_message = {
        "FileSizeError": "Syntax Error: Empty File or Directory. Validation Aborted."
    }
    
    file_size = os.path.getsize(tar_file)
    if file_size == 0:
        return Result(NAME, code = -1, message = error_message["FileSizeError"])
    else:
        return Result(NAME)

def metadata_check(tar_file, extension):
    
    NAME = "Metadata file existence"
    error_message = {
        "FileNotFoundError": "Syntax Error: No metadata file in file/directory: {}. Validation Aborted."
    }
    
    path = os.path.join(os.getcwd(), tar_file)
    metadata_file = "ro-crate-metadata.json"
    if extension == "" and os.path.exists(os.path.join(path, metadata_file)):
        return Result(NAME)
    # elif extension == ".zip":
    #     zf = zipfile.ZipFile(tar_file, 'r')
    #     if metadata_file in zf.namelist():
    #         return Result(NAME)
    return Result(NAME, code = -1, message = error_message["FileNotFoundError"].format(tar_file))


def string_value_check(tar_file, extension):
    
    NAME = "Json check"
    json_string = None
    metadata = "ro-crate-metadata.json"
    if extension == "":
        with open (os.path.join(tar_file, metadata), 'r') as f:
            try:
                json_string = f.read()
                parsed_json = json.loads(json_string)
                json.dumps(parsed_json, indent = 4, sort_keys = True)
            except json.JSONDecodeError as e:
                return Result(NAME, code = -1, message = "Json Syntax Error: %s." %repr(e) + "Validation Aborted.")

    # elif extension == ".zip":
    #     zf = zipfile.ZipFile(tar_file, 'r')
    #     json_string = zf.read(metadata)
    #     try:
    #         parsed_json = json.loads(json_string)
    #         json.dumps(parsed_json, indent = 4, sort_keys = True)
    #     except json.JSONDecodeError as e:
    #         return Result(NAME, code = -1, message = repr(e))
    
    return Result(NAME)

def check_context(tar_file, extension):
    
    NAME = "Json-ld check"
    error_message = {
        "ContextNotFoundError": "Syntax Error: Context is not provided. Validation Aborted."
    }
    metadata = "ro-crate-metadata.json"
    
    if extension == "":
        with open (os.path.join(tar_file, metadata), 'r') as f:
            parsed_jsonld = json.load(f)
            
        context_data = parsed_jsonld.get("@context")
        if context_data == None:
            return Result(NAME, code = -1, message = error_message["ContextNotFoundError"])
        else:
            return Result(NAME)

    # elif extension == ".zip":
    #     zf = zipfile.ZipFile(tar_file, 'r')
    #     json_string = zf.read(metadata)
    #     parsed_jsonld = json.loads(json_string.decode("utf-8"))
    #     context_data = parsed_jsonld.get("@context")

    #     if context_data == None:
    #         return Result(NAME, code = -1, message = error_message["ContextNotFoundError"])
    #     else:
    #         return Result(NAME)

