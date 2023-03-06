import os
from rdflib import Dataset
import json
import urllib
from rocrateValidator.utils import Result as Result


def rdf_parse_check(crate_root, extension):
    """RO-Crate Metadata file must be valid JSON-LD 1.0, 

    https://www.researchobject.org/ro-crate/1.1/structure.html#ro-crate-metadata-file-ro-crate-metadatajson
    https://www.researchobject.org/ro-crate/1.1/appendix/jsonld.html
    """
    error_message = {
        "JSONError": "Can't parse JSON: {}",
        "ContextError": "Can't retrieve JSON-LD context: {}",
        "ParseError": "Can't parse JSON-LD as RDF: {}",
        "EmptyGraphError": "Parsed JSON-LD is empty"
    }
    NAME = "RDF Parse check"
    d = Dataset()
    try:
        d.parse(os.path.join(crate_root, "ro-crate-metadata.json"), format="application/ld+json")
    except json.JSONDecodeError as e:
        return Result(NAME, code = -1, message = error_message["JSONError"].format(repr(e)))
    except urllib.error.URLError as e:
        return Result(NAME, code = -2, message = error_message["ContextError"].format(repr(e)))
    except Exception as e:
        return Result(NAME, code = -3, message = error_message["ParseError"].format(repr(e)))
    
    if len(d) == 0:
        return Result(NAME, code = -4, message = error_message["EmptyGraphError"])
    
    return Result(NAME)

def shex_check(crate_root, extension):
    NAME = "ShEX check"
    error_message = {
        "ShEXParse": "Broken shex, donkey ate it: {}",
    }
    return Result(NAME, code = -1, message = error_message["ShEXParse"])

