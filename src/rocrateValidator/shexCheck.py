import os
from rdflib import Dataset
import json
from rocrateValidator.utils import Result as Result

def rdf_parse_check(crate_root, extension):
    """RO-Crate Metadata file must be valid JSON-LD 1.0, 

    https://www.researchobject.org/ro-crate/1.1/structure.html#ro-crate-metadata-file-ro-crate-metadatajson
    https://www.researchobject.org/ro-crate/1.1/appendix/jsonld.html
    """
    error_message = {
        "JSONError": "Can't parse JSON: {}",
    }
    NAME = "RDF Parse check"
    d = Dataset()
    try:
        d.parse(os.path.join(crate_root, "ro-crate-metadata.json"), format="json-ld")
    except json.JSONDecodeError as e:
        return Result(NAME, code = -1, message = error_message["JSONError"].format(repr(e)))
    except:
        pass

    return Result(NAME)

def shex_check(crate_root, extension):
    NAME = "ShEX check"
    error_message = {
        "ShEXParse": "Broken shex, donkey ate it: {}",
    }
    return Result(NAME, code = -1, message = error_message["ShEXParse"])

