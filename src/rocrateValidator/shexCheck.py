from rocrateValidator.utils import Result as Result

def rdf_parse_check(tar_file, extension):
    """RO-Crate Metadata file must be valid JSON-LD 1.0, 

    https://www.researchobject.org/ro-crate/1.1/structure.html#ro-crate-metadata-file-ro-crate-metadatajson
    https://www.researchobject.org/ro-crate/1.1/appendix/jsonld.html
    """
    NAME = "RDF Parse check"
    
    return Result(NAME)

def shex_check(tar_file, extension):
    NAME = "ShEX check"
    error_message = {
        "ShEXParse": "Broken shex, donkey ate it: {}",
    }
    return Result(NAME, code = -1, message = error_message["ShEXParse"])

