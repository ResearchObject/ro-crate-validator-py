import pytest
import import_ipynb
import os
import sys
from pathlib import Path

# file = Path(os.path.abspath('')).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(os.path.join(str(root), "src"))
import src.semanticCheck as semanticCheck
import src.syntaxCheck as syntaxCheck


testing_path = "test/samples/invalid"
extension = ""
  

class TestGroup:

    NAME = None
    error_message = None
    bool = False

    @pytest.mark.parametrize("NAME, error_message, bool", [("File existence", [], True)])
    def test_file_existece(self, NAME, error_message, bool):
        output = syntaxCheck.existence_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("File size", [], True)])
    def test_file_size(self, NAME, error_message, bool):
        output = syntaxCheck.file_size_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Metadata file existence", [], True)])
    def test_metadataFile(self, NAME, error_message, bool):
        output = syntaxCheck.metadata_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Json check", [], True)])
    def test_json(self, NAME, error_message, bool):
        output = syntaxCheck.string_value_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool


    @pytest.mark.parametrize("NAME, error_message, bool", [("Self descriptor check", [], True)])
    def test_descriptor(self, NAME, error_message, bool):
        output = semanticCheck.self_descriptor_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Direct property check", 'Directory property of RO-Crate is wrong', False)])
    def test_direct_property(self, NAME, error_message, bool):
        output = semanticCheck.direct_property_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Referencing check", 'The referencing math/ is wrong', False)])
    def test_referencing(self, NAME, error_message, bool):
        output = semanticCheck.referencing_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Encoding check", [], True)])
    def test_encoding(self, NAME, error_message, bool):
        output = semanticCheck.encoding_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Scripts and workflow check", [], True)])
    def test_workflow(self, NAME, error_message, bool):
        output = semanticCheck.scripts_and_workflow_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Web-based data entity check", [], True)])
    def test_webbased_entity(self, NAME, error_message, bool):
        output = semanticCheck.webbased_entity_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Person entity check", [], True)])
    def test_person_entity(self, NAME, error_message, bool):
        output = semanticCheck.person_entity_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool

    @pytest.mark.parametrize("NAME, error_message, bool", [("Organization check", [], True)])
    def test_organization_entity(self, NAME, error_message, bool):
        output = semanticCheck.organization_check(testing_path, extension)
        self.NAME = output[0]
        self.error_message = output[1]
        self.bool = output[2]

        assert self.NAME == NAME
        assert self.error_message == error_message
        assert self.bool == bool



