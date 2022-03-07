import pytest
import import_ipynb
import os
import sys
from pathlib import Path

import src.utils as utils
import src.semanticCheck as semanticCheck
import src.syntaxCheck as syntaxCheck


testing_path = "test/samples/invalid"
extension = ""

class TestBase:

    @pytest.fixture
    def existence_example1(self):
        return utils.Result(NAME = "File existence")

    @pytest.fixture
    def fileSize_example1(self):
        return utils.Result(NAME = "File size") 

    @pytest.fixture
    def metadata_example1(self):
        return utils.Result(NAME = "Metadata file existence")

    @pytest.fixture
    def json_example1(self):
        return utils.Result(NAME = "Json check")

    @pytest.fixture
    def descriptor_example1(self):
        return utils.Result(NAME = "File descriptor check")

    @pytest.fixture
    def directProperty_example1(self):
        return utils.Result(NAME = "Direct property check", code = -1, message = "Directory property of RO-Crate is wrong")

    @pytest.fixture
    def referencing_example1(self):
        return utils.Result(NAME = "Referencing check", code = -1, message = "The referencing math/ is wrong")

    @pytest.fixture
    def encoding_example1(self):
        return utils.Result(NAME = "encoding check")

    @pytest.fixture
    def webbasedEntity_example1(self):
        return utils.Result(NAME = "Web-based data entity check")

    @pytest.fixture
    def personEntity_example1(self):
        return utils.Result(NAME = "Person entity check")

    @pytest.fixture
    def organizationEntity_example1(self):
        return utils.Result(NAME = "Organization entity check")

    @pytest.fixture
    def contactInfo_example1(self):
        return utils.Result(NAME = "Contact information check")

    @pytest.fixture
    def citation_example1(self):
        return utils.Result(NAME = "Citation property check")

    @pytest.fixture
    def publisher_example1(self):
        return utils.Result(NAME = "Publisher property check")

    @pytest.fixture
    def funder_example1(self):
        return utils.Result(NAME = "Funder property check")

    @pytest.fixture
    def licensing_example1(self):
        return utils.Result(NAME = "Licensing property check")

    @pytest.fixture
    def places_example1(self):
        return utils.Result(NAME = "Places property check")

    @pytest.fixture
    def time_example1(self):
        return utils.Result(NAME = "Time property check")

    @pytest.fixture
    def thumbnails_example1(self):
        return utils.Result(NAME = "Thumbnails property check")

    @pytest.fixture
    def workflow_example1(self):
        return utils.Result(NAME = "Scripts and workflow check")






class TestGroup(TestBase):

    def check_result(self, result, exp_result):
        if result.NAME == exp_result.NAME and result.code == exp_result.code and result.message == exp_result.message:
            return True
        else:
            return False
   
    def test_file_existence(self, existence_example1):
        result = syntaxCheck.existence_check(testing_path, extension)
        outcome = check_result(result, existence_example1)

        assert outcome == True

    def test_file_size(self, fileSize_example1):
        result = syntaxCheck.file_size_check(testing_path, extension)
        outcome = check_result(result, fileSize_example1)

        assert outcome == True

    def test_metadataFile(self, metadata_example1):
        result = syntaxCheck.metadata_check(testing_path, extension)
        outcome = check_result(result, metadata_example1)

        assert outcome == True

    def test_json(self, json_example1):
        result =syntaxCheck.string_value_check(testing_path, extension)
        outcome = check_result(result, json_example1)

        assert outcome == True

    def test_descriptor(self, descriptor_example1):
        result = semanticCheck.file_descriptor_check(testing_path, extension)
        outcome = check_result(result, descriptor_example1)

        assert outcome == True

    def test_direct_property(self, directProperty_example1):
        result = semanticCheck.direct_property_check(testing_path, extension)
        outcome = check_result(result, directProperty_example1)

        assert outcome == True

    def test_referencing(self, referencing_example1):
        result = semanticCheck.referencing_check(testing_path, extension)
        outcome = check_result(result, referencing_example1)

        assert outcome == True

    def test_encoding(self, encoding_example1):
        result = semanticCheck.encoding_check(testing_path, extension)
        outcome = check_result(result, encoding_example1)

        assert outcome == True

    def test_webbased_entity(self, webbasedEntity_example1):
        result = semanticCheck.webbased_entity_check(testing_path, extension)
        outcome = check_result(result, webbasedEntity_example1)

        assert outcome == True

    def test_person_entity(self, personEntity_example1):
        result = semanticCheck.person_entity_check(testing_path, extension)
        outcome  = check_result(result, personEntity_example1)

        assert outcome == True

    def test_organization_entity(self, organizationEntity_example1):
        result = semanticCheck.organization_check(testing_path, extension)
        outcome  = check_result(result, organizationEntity_example1)

        assert outcome == True

    def test_contactInfo_entity(self, contactInfo_example1):
        result = semanticCheck.contact_info_check(testing_path, extension)
        outcome  = check_result(result, contactInfo_example1)

        assert outcome == True

    def test_citation_entity(self, citation_example1):
        result = semanticCheck.citation_check(testing_path, extension)
        outcome  = check_result(result, citation_example1)

        assert outcome == True

    def test_publisher_entity(self, publisher_example1):
        result = semanticCheck.publisher_check(testing_path, extension)
        outcome  = check_result(result, publisher_example1)

        assert outcome == True

    def test_funder_entity(self, funder_example1):
        result = semanticCheck.funder_check(testing_path, extension)
        outcome  = check_result(result, funder_example1)

        assert outcome == True

    def test_licensing_entity(self, licensing_example1):
        result = semanticCheck.licensing_check(testing_path, extension)
        outcome  = check_result(result, licensing_example1)

        assert outcome == True

    def test_places_entity(self, places_example1):
        result = semanticCheck.places_check(testing_path, extension)
        outcome  = check_result(result, places_example1)

        assert outcome == True

    def test_time_entity(self, time_example1):
        result = semanticCheck.time_check(testing_path, extension)
        outcome  = check_result(result, time_example1)

        assert outcome == True

    def test_workflow(self, workflow_example1):
        result = semanticCheck.scripts_and_workflow_check(testing_path, extension)
        outcome  = check_result(result, workflow_example1)

        assert outcome == True

