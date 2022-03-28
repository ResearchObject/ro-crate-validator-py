import os
import json
from collections import defaultdict
import rocrateValidator.syntaxCheck as sync
import rocrateValidator.semanticCheck as smtc
import rocrateValidator.check_list as ck


class validate:
    
    def __init__(self, tar_file):
        self.tar_file = tar_file
        self.extension = os.path.splitext(self.tar_file)[1]
        
        ### define a dictionary storing the checking name with related function
        dictionary = {
            "File existence": sync.existence_check,
            "File size": sync.file_size_check, 
            "Metadata file existence":sync.metadata_check,
            "Json check": sync.string_value_check,
            "Json-ld check": sync.check_context,
            "File descriptor check": smtc.file_descriptor_check, 
            "Direct property check": smtc.direct_property_check,
            "Referencing check":smtc.referencing_check, 
            "Encoding check":smtc.encoding_check,
            "Web-based data entity check": smtc.webbased_entity_check,
            "Person entity check": smtc.person_entity_check,
            "Organization entity check": smtc.organization_check,
            "Contact information check": smtc.contact_info_check,
            "Citation property check": smtc.citation_check,
            "Publisher property check": smtc.publisher_check,
            "Funder property check": smtc.funder_check,
            "Licensing property check": smtc.licensing_check,
            "Places property check": smtc.places_check,
            "Time property check": smtc.time_check,
            # "Thumbnails check":smtc.thumbnails_check,
            "Scripts and workflow check":smtc.scripts_and_workflow_check
        }
        
        ### initialize the check result and function set as empty lists to store the checking function
        self.functions = []
        self.final_result = defaultdict(list)
        
        ### define the output of validator
        self.ptOutput = {
            "Valid": "This is a VALID RO-Crate",
            "WARNING": "This is a VALID RO-Crate but with Warning",
            "Invalid": "This is an INVALID RO-Crate"
        }
        
        check_list = list(ck.get_check_list())
        # with open ("check_list.txt") as file: 
        #     check_list = list(map(lambda s: s.strip(), file.readlines()))
        
        ### store the functions in a dictionary
        for x in check_list:
            if x in dictionary:
                self.functions.append(dictionary[x])
        
        for i in range(len(self.functions)):
            self.final_result[list(dictionary.keys())[i].rstrip("\n")].append(None)
            
        
    def update_output(self, NAME, code, message):
        if code == -1:
            self.final_result[NAME][0] = False
            self.final_result[NAME].append(message)
        elif code == 0:
            self.final_result[NAME][0] = True
        else:
            self.final_result[NAME][0] = message
    
    def printing_output(self, final_result, ptOutput):    
        temp_output = ptOutput["Valid"] 
        for values in final_result.values():
            if "WARNING" in str(values):
                temp_output = ptOutput["WARNING"]
            elif values[0] == False:
                return ptOutput["Invalid"]
    
        return temp_output
        
               
    def get_final_result(self):
        return self.final_result

    def validator(self):
        for methods in self.functions: 
            result = methods(self.tar_file, self.extension)
            if (result.NAME == "File existence" or result.NAME == "File_size" or result.NAME == "Metadata file existence" or result.NAME == "Json check" or result.NAME == "Json-ld check") and result.code == -1:
                self.update_output(result.NAME, result.code, result.message)
                break
            self.update_output(result.NAME, result.code, result.message)
        
        output = json.dumps(self.final_result, indent = 4, separators=(',', ': '), sort_keys = False)
        
        with open('result.json', 'w') as file:
            file.write(json.dumps(self.final_result, indent = 4, separators=(',', ': '),sort_keys = False))
        
        print(self.printing_output(self.final_result, self.ptOutput))
        print(output)