import pytest
import import_ipynb
import os
import sys
from pathlib import Path

from rocrateValidator import semanticCheck as semanticCheck
from rocrateValidator import syntaxCheck as syntaxCheck
from rocrateValidator import utils as utils
from rocrateValidator import validate as validate

testing_path = "test/samples/valid"
testing_path0 = "test/samples/invalid/brroken_example"
testing_path1 = "test/samples/invalid/referencing_missing"
testing_path2 = "test/samples/invalid/context_missing"
testing_path3 = "test/samples/invalid/invalid_json"
testing_path4 = "test/samples/invalid/metadataFile_missing"
testing_path5 = "test/samples/invalid/invalid_descriptorType"
testing_path6 = "test/samples/invalid/empty_metadataFile"
testing_path7 = "test/samples/invalid/invalid_encodingType1"
testing_path8 = "test/samples/invalid/invalid_directProp_id"
testing_path9 = "test/samples/invalid/invalid_personEntity_type"
testing_path10 = "test/samples/invalid/invalid_directProp_type"
testing_path11 = "test/samples/invalid/invalid_licenseType"
testing_path12 = "test/samples/invalid/invalid_directProp_dateFormat"
testing_path13 = "test/samples/invalid/invalid_encodingType2"
testing_path14 = "test/samples/invalid/webBasedEntity_publishedDateMissing"
testing_path15 = "test/samples/invalid/invalid_webBasedEntity_type"
testing_path16 = "test/samples/invalid/invalid_webBasedEntity_id"
testing_path17 = "test/samples/invalid/invalid_contactInfo_type"
testing_path18 = "test/samples/invalid/citation_referencingMissing"
testing_path19 = "test/samples/invalid/invalid_organizationType"
testing_path20 = "test/samples/invalid/invalid_citationId"
testing_path21 = "test/samples/invalid/publisher_referencingMissing"
testing_path22 = "test/samples/invalid/invalid_funderType"
testing_path23 = "test/samples/invalid/invalid_licenseId"
testing_path24 = "test/samples/invalid/placeEntity_missingGeoName"
testing_path25 = "test/samples/invalid/invalid_workflowType"
testing_path26 = "test/samples/invalid/unrecognised_workflow"
extension = ""

class DataBase:

    @pytest.fixture
    def existence_true(self):
        return utils.Result(NAME = "File existence")

    @pytest.fixture
    def existence_false_1(self):
        return utils.Result(NAME = "File existence", code = -1, message = "Syntax Error: No such file or directory: test/samples/invalid/brroken_example. Validation Aborted.")

    @pytest.fixture
    def fileSize_true(self):
        return utils.Result(NAME = "File size")

    @pytest.fixture
    def metadata_true(self):
        return utils.Result(NAME = "Metadata file existence")

    @pytest.fixture
    def metadata_false_1(self):
        return utils.Result(NAME = "Metadata file existence", code = -1, message = "Syntax Error: No metadata file in file/directory: test/samples/invalid/metadataFile_missing. Validation Aborted.")

    @pytest.fixture
    def json_true(self):
        return utils.Result(NAME = "Json check")

    @pytest.fixture
    def json_false_1(self):
        return utils.Result(NAME = "Json check", code = -1, message = "Json Syntax Error: JSONDecodeError('Invalid control character at: line 9 column 37 (char 221)').Validation Aborted.")

    @pytest.fixture
    def context_true(self):
        return utils.Result(NAME = "Json-ld check")

    @pytest.fixture
    def context_false(self):
        return utils.Result(NAME = "Json-ld check", code = -1, message = "Syntax Error: Context is not provided. Validation Aborted.")

    @pytest.fixture
    def descriptor_true(self):
        return utils.Result(NAME = "File descriptor check")

    @pytest.fixture
    def descriptor_false(self):
        return utils.Result(NAME = "File descriptor check", code = -1, message = "Semantic Error: Invalid file descritor.")

    @pytest.fixture
    def directProperty_true(self):
        return utils.Result(NAME = "Direct property check")

    @pytest.fixture
    def directProperty_idError(self):
        return utils.Result(NAME = "Direct property check", code = -1, message = "Semantic Error: Invalid Direct Property ID. It MUST end with / and SHOULD be ./")

    @pytest.fixture
    def directProperty_typeError(self):
        return utils.Result(NAME = "Direct property check", code = -1, message = "Semantic Error: Invalid Type Value at Direct Property ./")

    @pytest.fixture
    def directProperty_dateError(self):
        return utils.Result(NAME = "Direct property check", code = -1, message = "Semantic Error: datePublished of Direct Property ./ is not in ISO 8601 date format or not Provided")

    @pytest.fixture
    def referencing_true(self):
        return utils.Result(NAME = "Referencing check")

    @pytest.fixture
    def referencing_referencingError_1(self):
        return utils.Result(NAME = "Referencing check", code = -1, message = "Semantic Error: The referencing math/ is wrong.")

    @pytest.fixture
    def encoding_true(self):
        return utils.Result(NAME = "Encoding check")

    @pytest.fixture
    def encoding_encodingError_1(self):
        return utils.Result(NAME = "Encoding check", code = -1, message = "Semantic Error: Encoding in {} is wrong")

    @pytest.fixture
    def encoding_typeError_1(self):
        return utils.Result(NAME = "Encoding check", code = -1, message = "Semantic Error: The value of @type of some_extension.md entity is incorrect.")

    @pytest.fixture
    def encoding_typeError_2(self):
        return utils.Result(NAME = "Encoding check", code = -1, message = "Semantic Error: The value of @type of https://www.nationalarchives.gov.uk/PRONOM/fmt/19 entity is incorrect.")

    @pytest.fixture
    def webbasedEntity_true(self):
        return utils.Result(NAME = "Web-based data entity check")

    @pytest.fixture
    def webbasedEntity_urlError(self):
        return utils.Result(NAME = "Web-based data entity check", code = -1, message = "Semantic Error: Invalid ID at https://www.researchobject.org/ro-crate/1.1/data-entities.html#web-based-data-entities. It should be a downloadable url")

    @pytest.fixture
    def webbasedEntity_dateError(self):
        return utils.Result(NAME = "Web-based data entity check", code = -1, message = "Semantic Error: Invalid sdDatePublished https://zenodo.org/record/3541888/files/ro-crate-1.0.0.pdf or Not Provided")

    @pytest.fixture
    def webbasedEntity_typeError(self):
        return utils.Result(NAME = "Web-based data entity check", code = -1, message = "Semantic Error: Invalid @type value of http://example.com/downloads/2020/lots_of_little_files.zip.")

    @pytest.fixture
    def personEntity_true(self):
        return utils.Result(NAME = "Person entity check")

    @pytest.fixture
    def personEntity_personError(self):
        return utils.Result(NAME = "Person entity check", code = -1, message = "")

    @pytest.fixture
    def personEntity_typeError(self):
        return utils.Result(NAME = "Person entity check", code = -1, message = "Semantic Error: Invalid @type value of https://orcid.org/0000-0002-8367-6908")

    @pytest.fixture
    def organizationEntity_true(self):
        return utils.Result(NAME = "Organization entity check")

    @pytest.fixture
    def organizationEntity_typeError(self):
        return utils.Result(NAME = "Organization entity check", code = -1, message = "Semantic Error: Invalid Organization contextual entity https://ror.org/03f0f6041")

    @pytest.fixture
    def contactInfo_true(self):
        return utils.Result(NAME = "Contact information check")

    @pytest.fixture
    def contactInfo_typeError(self):
        return utils.Result(NAME = "Contact information check", code = -1, message = "Semantic Error: Invlaid Type Value at mailto:tim.luckett@uts.edu.au")

    @pytest.fixture
    def citation_true(self):
        return utils.Result(NAME = "Citation property check")

    @pytest.fixture
    def citation_typeError(self):
        return utils.Result(NAME = "Citation property check", code = -1, message = "Semantic Error: Invalid Type Value at https://doi.org/10.1109/TCYB.2014.2386282")

    @pytest.fixture
    def citation_idError(self):
        return utils.Result(NAME = "Citation property check", code = -1, message = "Semantic Error: Invalid ID Value at 10.1109/TCYB.2014.2386282")

    @pytest.fixture
    def citation_referencingError(self):
        return utils.Result(NAME = "Citation property check", code = -1, message = "Semantic Error: Invalid Referencing https://doi.org/10.1109/TCYB.2014.2386282 or Not Provided")

    @pytest.fixture
    def publisher_true(self):
        return utils.Result(NAME = "Publisher property check")

    @pytest.fixture
    def publisher_typeError(self):
        return utils.Result(NAME = "Publisher property check", code = -1, message = "")

    @pytest.fixture
    def publisher_referencingError(self):
        return utils.Result(NAME = "Publisher property check", code = -1, message = "Semantic Error: Invalid Referencing https://ror.org/03f0f6041 or Not Provided")

    @pytest.fixture
    def funder_true(self):
        return utils.Result(NAME = "Funder property check")

    @pytest.fixture
    def funder_typeError(self):
        return utils.Result(NAME = "Funder property check", code = -1, message = "Semantic Error: Invalid Type Vlaue at https://eresearch.uts.edu.au/projects/provisioner")

    @pytest.fixture
    def funder_referencingError(self):
        return utils.Result(NAME = "Funder property check", code = -1, message = "")

    @pytest.fixture
    def licensing_true(self):
        return utils.Result(NAME = "Licensing property check")

    @pytest.fixture
    def licensing_typeError(self):
        return utils.Result(NAME = "Licensing property check", code = -1, message = "Semantic Error: Invalid Type Value at https://spdx.org/licenses/CC-BY-NC-SA-4.0 or not provided.")

    @pytest.fixture
    def licensing_idError(self):
        return utils.Result(NAME = "Licensing property check", code = -1, message =  "Semantic Error: Invalid ID Value at licenses/CC-BY-NC-SA-4.0. It must be an URL.")

    @pytest.fixture
    def licensing_referencingError(self):
        return utils.Result(NAME = "Licensing property check", code = -1, message = "Semantic Error: Invalid Referencing or NOT Provided")

    @pytest.fixture
    def places_true(self):
        return utils.Result(NAME = "Places property check")

    @pytest.fixture
    def places_nameError(self):
        return utils.Result(NAME = "Places property check", code = -1, message = "Semantic Error: Invalid Place Entity #b4168a98-8534-4c6d-a568-64a55157b656. The Place has geo property SHOULD have a name.")

    @pytest.fixture
    def time_true(self):
        return utils.Result(NAME = "Time property check")

    @pytest.fixture
    def time_typeError(self):
        return utils.Result(NAME = "Time property check", code = -1, message = "")

    @pytest.fixture
    def thumbnails_true(self):
        return utils.Result(NAME = "Thumbnails property check")

    @pytest.fixture
    def workflow_true(self):
        return utils.Result(NAME = "Scripts and workflow check")

    @pytest.fixture
    def workflow_WorkflowError(self):
        return utils.Result(NAME = "Scripts and workflow check", code = -1, message = "Scripts and Workflow is Wrong")

    @pytest.fixture
    def workflow_typeError(self):
        return utils.Result(NAME = "Scripts and workflow check", code = -1, message = "Semantic Error: Invalid @type value for workflow file workflow/retropath.knime. It must have File, SoftwareSourceCode and ComputationalWorkflow as value.")

    @pytest.fixture
    def workflow_warning(self):
        return utils.Result(NAME = "Scripts and workflow check", code = 1, message = "WARNING: .md is not a recognised workflow extension. Please raise an issue at GitHub: <https://github.com/ResearchObject/ro-crate-validator-py/issues>.")






class TestGroup(DataBase):

    def check_result(self, result, exp_result):
        if result.NAME == exp_result.NAME and result.code == exp_result.code and result.message == exp_result.message:
            return True
        else:
            return False
    def aborted_result(self, result):
        if result == [None]:
            return True
        else:
            return False
   
    def test_file_existence(self, existence_true):
        result = syntaxCheck.existence_check(testing_path1, extension)
        outcome = self.check_result(result, existence_true)

        assert outcome == True

    def test_file_existence_1(self, existence_false_1):
        result = syntaxCheck.existence_check(testing_path0, extension)
        outcome = self.check_result(result, existence_false_1)

        assert outcome == True

    def test_file_size_0(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()["File size"]
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_file_size(self, fileSize_true):
        result = syntaxCheck.file_size_check(testing_path1, extension)
        outcome = self.check_result(result, fileSize_true)

        assert outcome == True

    # def test_file_size_1(self, fileSize_false):
    #     result = syntaxCheck.file_size_check(testing_path12, extension)
    #     outcome = self.check_result(result, fileSize_false)

    #     assert outcome == True

    def test_metadataFile(self, metadata_true):
        result = syntaxCheck.metadata_check(testing_path1, extension)
        outcome = self.check_result(result, metadata_true)

        assert outcome == True

    def test_metadataFile_1(self, metadata_false_1):
        result = syntaxCheck.metadata_check(testing_path4, extension)
        outcome = self.check_result(result, metadata_false_1)

        assert outcome == True

    def test_metadataFile_2(self, metadata_true):
        result = syntaxCheck.metadata_check(testing_path2, extension)
        outcome = self.check_result(result, metadata_true)

        assert outcome == True

    def test_metadataFile_3(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Metadata file existence']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_json(self, json_true):
        result =syntaxCheck.string_value_check(testing_path1, extension)
        outcome = self.check_result(result, json_true)

        assert outcome == True

    def test_json_1(self, json_true):
        result =syntaxCheck.string_value_check(testing_path2, extension)
        outcome = self.check_result(result, json_true)

        assert outcome == True

    def test_json_2(self, json_false_1):
        result =syntaxCheck.string_value_check(testing_path3, extension)
        outcome = self.check_result(result, json_false_1)

        assert outcome == True

    def test_json_3(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Json check']
        outcome = self.aborted_result(result)

        assert outcome == True
    
    def test_jsonld(self, context_true):
        result = syntaxCheck.check_context(testing_path1, extension)
        outcome = self.check_result(result, context_true)

        assert outcome == True

    def test_jsonld_1(self, context_false):
        result = syntaxCheck.check_context(testing_path2, extension)
        outcome = self.check_result(result, context_false)

        assert outcome == True

    def test_jsonld_2(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Json-ld check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_descriptor(self, descriptor_true):
        result = semanticCheck.file_descriptor_check(testing_path1, extension)
        outcome = self.check_result(result, descriptor_true)

        assert outcome == True

    def test_descriptor_1(self, descriptor_false):
        result = semanticCheck.file_descriptor_check(testing_path5, extension)
        outcome = self.check_result(result, descriptor_false)

        assert outcome == True

    def test_descriptor_2(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['File descriptor check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_direct_property(self, directProperty_true):
        result = semanticCheck.direct_property_check(testing_path1, extension)
        outcome = self.check_result(result, directProperty_true)

        assert outcome == True

    # def test_direct_property_1(self, directProperty_idError):
    #     result = semanticCheck.direct_property_check(testing_path8, extension)
    #     outcome = self.check_result(result, directProperty_idError)

    #     assert outcome == True

    def test_direct_property_2(self, directProperty_typeError):
        result = semanticCheck.direct_property_check(testing_path10, extension)
        outcome = self.check_result(result, directProperty_typeError)

        assert outcome == True

    def test_direct_property_3(self, directProperty_dateError):
        result = semanticCheck.direct_property_check(testing_path12, extension)
        outcome = self.check_result(result, directProperty_dateError)

        assert outcome == True

    def test_direct_property_4(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Direct property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_referencing(self, referencing_referencingError_1):
        result = semanticCheck.referencing_check(testing_path1, extension)
        outcome = self.check_result(result, referencing_referencingError_1)

        assert outcome == True

    def test_referencing_1(self, referencing_true):
        result = semanticCheck.referencing_check(testing_path, extension)
        outcome = self.check_result(result, referencing_true)

        assert outcome == True

    def test_referencing_2(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Referencing check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_referencing_3(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Referencing check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_encoding(self, encoding_true):
        result = semanticCheck.encoding_check(testing_path1, extension)
        outcome = self.check_result(result, encoding_true)

        assert outcome == True

    def test_encoding_1(self, encoding_typeError_1):
        result = semanticCheck.encoding_check(testing_path7, extension)
        outcome = self.check_result(result, encoding_typeError_1)

        assert outcome == True

    def test_encoding_2(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Encoding check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_encoding_3(self, encoding_typeError_2):
        result = semanticCheck.encoding_check(testing_path13, extension)
        outcome = self.check_result(result, encoding_typeError_2)

        assert outcome == True

    def test_webbased_entity(self, webbasedEntity_true):
        result = semanticCheck.webbased_entity_check(testing_path1, extension)
        outcome = self.check_result(result, webbasedEntity_true)

        assert outcome == True

    def test_webbased_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Web-based data entity check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_webbased_entity_2(self, webbasedEntity_dateError):
        result = semanticCheck.webbased_entity_check(testing_path14, extension)
        outcome = self.check_result(result, webbasedEntity_dateError)

        assert outcome == True

    def test_webbased_entity_3(self, webbasedEntity_typeError):
        result = semanticCheck.webbased_entity_check(testing_path15, extension)
        outcome = self.check_result(result, webbasedEntity_typeError)

        assert outcome == True

    def test_webbased_entity_4(self, webbasedEntity_urlError):
        result = semanticCheck.webbased_entity_check(testing_path16, extension)
        outcome = self.check_result(result, webbasedEntity_urlError)

        assert outcome == True

    def test_person_entity(self, personEntity_true):
        result = semanticCheck.person_entity_check(testing_path1, extension)
        outcome  = self.check_result(result, personEntity_true)

        assert outcome == True

    def test_person_entity_1(self, personEntity_typeError):
        result = semanticCheck.person_entity_check(testing_path9, extension)
        outcome  = self.check_result(result, personEntity_typeError)

        assert outcome == True

    def test_person_entity_2(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Person entity check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_organization_entity(self, organizationEntity_true):
        result = semanticCheck.organization_check(testing_path1, extension)
        outcome  = self.check_result(result, organizationEntity_true)

        assert outcome == True

    def test_organization_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Organization entity check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_organization_entity(self, organizationEntity_typeError):
        result = semanticCheck.organization_check(testing_path19, extension)
        outcome  = self.check_result(result, organizationEntity_typeError)

        assert outcome == True

    def test_contactInfo_entity(self, contactInfo_true):
        result = semanticCheck.contact_info_check(testing_path1, extension)
        outcome  = self.check_result(result, contactInfo_true)

        assert outcome == True

    def test_contactInfo_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Contact information check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_contactInfo_entity_2(self, contactInfo_typeError):
        result = semanticCheck.contact_info_check(testing_path17, extension)
        outcome  = self.check_result(result, contactInfo_typeError)

        assert outcome == True

    def test_citation_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Citation property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_citation_entity_2(self, citation_referencingError):
        result = semanticCheck.citation_check(testing_path18, extension)
        outcome  = self.check_result(result, citation_referencingError)

        assert outcome == True

    def test_citation_entity_3(self, citation_idError):
        result = semanticCheck.citation_check(testing_path20, extension)
        outcome  = self.check_result(result, citation_idError)

        assert outcome == True  

    def test_publisher_entity(self, publisher_true):
        result = semanticCheck.publisher_check(testing_path1, extension)
        outcome  = self.check_result(result, publisher_true)

        assert outcome == True

    def test_publisher_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Publisher property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_publisher_entity_2(self, publisher_referencingError):
        result = semanticCheck.publisher_check(testing_path21, extension)
        outcome  = self.check_result(result, publisher_referencingError)

        assert outcome == True

    def test_funder_entity(self, funder_true):
        result = semanticCheck.funder_check(testing_path1, extension)
        outcome  = self.check_result(result, funder_true)

        assert outcome == True

    def test_funder_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Funder property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_funder_entity_2(self, funder_typeError):
        result = semanticCheck.funder_check(testing_path22, extension)
        outcome  = self.check_result(result, funder_typeError)

        assert outcome == True

    def test_licensing_entity(self, licensing_referencingError):
        result = semanticCheck.licensing_check(testing_path1, extension)
        outcome  = self.check_result(result, licensing_referencingError)

        assert outcome == True

    def test_licensing_entity_1(self, licensing_true):
        result = semanticCheck.licensing_check(testing_path, extension)
        outcome  = self.check_result(result, licensing_true)

        assert outcome == True

    def test_licensing_entity_2(self, licensing_typeError):
        result = semanticCheck.licensing_check(testing_path11, extension)
        outcome  = self.check_result(result, licensing_typeError)

        assert outcome == True

    def test_licensing_entity_3(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Licensing property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_licensing_entity_4(self, licensing_idError):
        result = semanticCheck.licensing_check(testing_path23, extension)
        outcome  = self.check_result(result, licensing_idError)

        assert outcome == True

    def test_places_entity(self, places_true):
        result = semanticCheck.places_check(testing_path1, extension)
        outcome  = self.check_result(result, places_true)

        assert outcome == True

    def test_places_entity_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Places property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_places_entity_2(self, places_nameError):
        result = semanticCheck.places_check(testing_path24, extension)
        outcome  = self.check_result(result, places_nameError)

        assert outcome == True

    def test_time_entity(self, time_true):
        result = semanticCheck.time_check(testing_path1, extension)
        outcome  = self.check_result(result, time_true)

        assert outcome == True

    def test_time_entity(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Time property check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_workflow(self, workflow_true):
        result = semanticCheck.scripts_and_workflow_check(testing_path1, extension)
        outcome  = self.check_result(result, workflow_true)

        assert outcome == True

    def test_workflow_1(self):
        v = validate.validate(testing_path0)
        result = v.get_final_result()['Scripts and workflow check']
        outcome = self.aborted_result(result)

        assert outcome == True

    def test_workflow_2(self, workflow_typeError):
        result = semanticCheck.scripts_and_workflow_check(testing_path25, extension)
        outcome  = self.check_result(result, workflow_typeError)

        assert outcome == True

    def test_workflow_3(self, workflow_warning):
        result = semanticCheck.scripts_and_workflow_check(testing_path26, extension)
        outcome  = self.check_result(result, workflow_warning)

        assert outcome == True

