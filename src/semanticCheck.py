import os 
import json
import datetime
import import_ipynb
import zipfile
import rocrate.utils as utils
import rocrate.rocrate as rocrate
from datetime import datetime
import pytest
from utils import Result as Result

def entity_type(type, exp_type):
    return True if type == exp_type else False

def entity_id(id, *exp_id):
    return True if id in exp_id else False

def entity_about(about, exp_about):
    return True if about == exp_about else False

def entity_conformsTo(cfmsTo):
    return True if cfmsTo.startswith("https://w3id.org/ro/crate/") else False

def entity_property(entity, type):
    if entity_type(type, ['CreativeWork']):
        try:
            id = utils.get_norm_value(entity, "@id")[0]
            about = utils.get_norm_value(entity, "about")[0]
            cfm = utils.get_norm_value(entity, "conformsTo")[0]
        except IndexError:
            return False
        if entity_id(id, 'ro-crate-metadata.json', 'ro-crate-metadata.jsonld') and entity_about(about, './') and entity_conformsTo(cfm):
            return True
    return False
            
    
def file_descriptor_check(tar_file, extension):
    """\
    Check the Metadata file descriptor in RO-Crate
    Please check the requirements details in: 
    <https://www.researchobject.org/ro-crate/1.1/root-data-entity.html>
    """
    NAME = "File descriptor check"
    error_message = {
        "DescriptorError": "entity property of self descriptor is incorrect"
    }
    
    with open (os.path.join(tar_file, "ro-crate-metadata.json"), 'r') as file:
        metadata = json.load(file)
        graph = metadata['@graph']
    
    for entity in graph:
        type = utils.get_norm_value(entity, "@type")
        if entity_property(entity, type):
            return Result(NAME) 

    return Result(NAME, code = -1, message = error_message["DescriptorError"])


def datetime_valid(dt_str):
    try: 
        datetime.fromisoformat(dt_str)
    except: 
        return False
    return True

def dataset_property(entity, type):
    try:
        id = utils.get_norm_value(entity, '@id')[0]
    except IndexError:
        return False
    if type[0] == ['Dataset'] and id.endswith('/'):
        return True
    return False
            
def direct_property_check(tar_file, extension):
    """\
    A valid RO-Crate MUST meets the direct property requirements
    Please check the requirements details in: 
    <https://www.researchobject.org/ro-crate/1.1/root-data-entity.html>
    """
    NAME = "Direct property check"
    error_message = {
        "DateError": "datePublished at {} is not in ISO 8601 date format",
        "DirectPropError": "Directory property of RO-Crate is wrong"
    }
    
    with open (os.path.join(tar_file, "ro-crate-metadata.json"), 'r') as file:
        metadata = json.load(file)
        graph = metadata['@graph']
    
    ### check each entity in @graph of metadata, each type must be Dataset and datePublished has to be in ISO format
    for entity in graph: 
        type = utils.get_norm_value(entity, '@type')
        if dataset_property(entity, type):
            for _ in utils.get_norm_value(entity, 'datePublished'):
                if datetime_valid(_) == True:
                    return Result(NAME)
                else:
                    return Result(NAME, code = -1, message = error_message["DateError"].format(_) )
                
    return Result(NAME, code = -1, message = error_message["DirectPropError"])


### the value of type must either be string of expected type or a list with expected type in elements. 
def metadata_contains(metadata, id_, exp_ct):
    if metadata["%s" % id_[0]]["@type"] == exp_ct or (isinstance(metadata["%s" % id_[0]]["@type"], list) and exp_ct in metadata["%s" % id_[0]]["@type"]):
        return True
    return False

### referencing result record the metadata name as key and check result as value. 
def update_rfeResult(id_, referencing_result, metadata, error_message, exp_ct):
    if metadata_contains(metadata, id_, exp_ct):
        referencing_result[id_[0]] = True
    else:
        referencing_result[id_[0]] = [False, error_message["ReferError"].format(id_[0])]
                         
def referencing_check(tar_file, extension):
    """/
    Where file or folder are represented as Data Entity in RO-Crate JSON-LD
    There MUST be linked to, directly or indirectly, hasPart in Root Data Entity.
    For more information, please check : 
    <https://www.researchobject.org/ro-crate/1.1/data-entities.html#referencing-files-and-folders-from-the-root-data-entity>
    """
    
    NAME = "Referencing check"
    error_message = {
        "ReferError": "The referencing {} is wrong."
    }
    
    ### Create a dictionary to store the referencing check result
    referencing_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    
    for entity in metadata.values(): 
        hasPart = utils.get_norm_value(entity, "hasPart")
        creator = utils.get_norm_value(entity, "creator")
        if len(hasPart) != 0: 
            break
    
    for parts in hasPart: 
        id_ = utils.get_norm_value(metadata[parts], "@id")
        extensions = os.path.splitext(id_[0])[1]
        
        if extension == "" and id_[0].endswith('/'):
            update_rfeResult(id_, referencing_result, metadata, error_message, "Dataset")
        elif extension != "":
            update_rfeResult(id_, referencing_result, metadata, error_message, "File")
    
    ### loop through referencign result, if there is a list in the vlaue of dictionary, the function will return False
    for values in referencing_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
    
    return Result(NAME)


### for the value of encoding is url, the type must have website in the element within the list
def update_ecdResult(type, encoding, encoding_result, error_message):
    type = "WebSite" if "Website" in type else None
    if utils.is_url(encoding[1]) and type != None:
        encoding_result[encoding[1]] = True
    else:
        encoding_result[encoding[1]] = [False, error_message["TypeError"].format(encoding[1])]
        
def ext_based_updEcd(extension, encoding, encoding_result, type, error_message):
    if extension == "" and encoding[1].endswith("/") and "Dataset" in type:
        encoding_result[encoding[1]] = True
    elif extension != "" and "File" in type:
        encoding_result[encoding[1]] = True
    else:
        encoding_result[encoding[1]] = [False, error_message["TypeError"].format(encoding[1])]

def encoding_check(tar_file, extension): 
    
    """
    The details of encoding should meet the requirments
    Please check more information at:
    <https://www.researchobject.org/ro-crate/1.1/data-entities.html#adding-detailed-descriptions-of-encodings>
    """
    
    NAME = "Encoding check"
    error_message = {
        "EncodingError" : "Encoding in {} is wrong",
        "TypeError": "The value of @type of {} entity is incorrect."
    }
    
    ### Create a dictionary to store the encoding check result
    encoding_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    
    for entity in metadata.values(): 
        encoding = utils.get_norm_value(entity, "encodingFormat")
        if len(encoding) >= 2:
            type = utils.get_norm_value(metadata[encoding[1]], "@type")
            if utils.is_url(encoding[1]):
                update_ecdResult(type, encoding, encoding_result, error_message)
            else:
                extension = os.path.splitext(encoding[1])[1]
                ext_based_updEcd(extension, encoding, encoding_result, type, error_message)
                    
    ### If any of the value in the dictionary are false which should be a list, then return false
    for values in encoding_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = error_message["EncodingError"].format(list(encoding_result.keys())[list(encoding_result.values()).index([values[0], values[1]])]))
    
    return Result(NAME)


def is_downloadable(url):
    """
    Does the url contain a downloadable resourses
    """
    r = requests.get(url,stream=True)
    content_type = r.headers.get('content-type')
    if "text" in content_type.lower(): 
        return False
    if 'html' in content_type.lower(): 
        return False
    return True

def urlFile_updRlt(id_, entity, webbased_result, error_message):
    if is_downloadable(id_):
        try:
            sdDatePublished = utils.get_norm_value(entity, "sdDatePublished")[0]
            if datetime_valid(sdDatePublished):
                webbased_result[id_] = True
            else:
                webbased_result[id_] = [False, error_message["DateError"].format(id_)]
        except IndexError:
            webbased_result[id_] = [False, error_message["DateError"].format(id_)]
    else:
        webbased_result[id_] = [False, error_message["UrlError"].format(id_)]

def dirOnWeb_updRlt(entity, metadata, webbased_result, error_message):
    distribution = utils.get_norm_value(entity, "distribution")
    if distribution != []:
        dis_type = utils.get_norm_value(metadata[distribution[0]], "@type")
        if dis_type[0] !="DataDownload":
            webbased_result[distribution[0]] = [False, error_message["TypeError"].format(distribution[0])]
        else:
            webbased_result[distribution[0]] = True

def webbased_entity_check(tar_file, extension):
    """
    Please check RO-Crate website for more information about web-based data entity.
    <https://www.researchobject.org/ro-crate/1.1/data-entities.html#web-based-data-entities>
    """
    
    NAME = "Web-based data entity check"
    error_message = {
        "UrlError": "Web-based data entity {} should be a downloadable url",
        "DateError": "sdDatePublished of web based data entity {} is not provided or incorrect",
        "TypeError": "the value of @type of {} has to be DataDownload"
    }
    webbased_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    
    for entity in metadata.values():
        type = utils.get_norm_value(entity, "@type")[0]
        id_ = utils.get_norm_value(entity, "@id")[0]
        
        ### update result
        if type == "File" and utils.is_url(id_):
            urlFile_updRlt(id_, entity, webbased_result, error_message)
        elif type == "Dataset":
            dirOnWeb_updRlt(entity, metadata, webbased_result, error_message)
    
    for values in webbased_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
    
    return Result(NAME)

def check_author_type(author, metadata, person_result, error_message):
    if author != []:
        author = author[0]
        if utils.is_url(author):
            type = utils.get_norm_value(metadata[author], "@type")
            try:
                if type[0] == "Person":
                    person_result[author] = True
                elif type[0] == "Organization":
                    person_result[author] = warning_message['OrganizationAuthor'].format(author)
                else:
                    person_result[author] = [False, error_message["TypeError"].format(author)]
            except IndexError:
                person_result[author] = [False, error_message["PersonError"].format(author)]


def person_entity_check(tar_file, extension):
    
    """
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#people>
    """
    
    NAME = "Person entity check"
    error_message = {
        "PersonError": "Person entity {} is incorrect",
        "TypeError": "The value of @type of {} is incorrect"
    }
    warning_message = {
        "OrganizationAuthor" : "WARNING: The Author {} is an Organization"
    }
    
    person_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        author = utils.get_norm_value(entity, "author")
        check_author_type(author, metadata, person_result, error_message)
    
    for values in person_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
    
    return Result(NAME)

def publisher_affiliation_correctness(entity, ck_item, metadata, organization_result, error_message):
    item = utils.get_norm_value(entity, "%s" %ck_item)
    if item != []:
        item = item[0]
        if utils.get_norm_value(metadata[item], "@type") == ["Organization"]:
            organization_result[utils.get_norm_value(entity, "@id")[0]] = True
        else:
            organization_result[utils.get_norm_value(entity, "@id")[0]] = [False, error_message["OrganizationError"].format(item)]
        
def organization_check(tar_file, extension):
    
    """
    An Organization SHOULD be the value for the publisher property of a Dataset or ScholarlyArticle 
    or affiliation property of a Person.
    Please see more information and examples at RO-Crate Website
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#organizations-as-values>
    """
    
    NAME = "Organization entity check"
    error_message = {
        "OrganizationError": "Organization contextual entity {} is incorrect"
    }
    
    ### dictionary to store the checking result
    organization_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        type = utils.get_norm_value(entity, "@type")[0]
        
        ### check the value of publisher for each dataset and scholarly article entity
        if type =="Dataset" or type == "ScholarlyArticle":
            publisher_affiliation_correctness(entity, "publisher", metadata, organization_result, error_message)
            
        ### check the vlaue of affiliation for each file entity
        elif type == "File":
            publisher_affiliation_correctness(entity, "affiliation", metadata, organization_result, error_message)
    
    for values in organization_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
      
    return Result(NAME)


def upd_contactInfoType_rlt(metadata, parent_entity, contact_result, error_message):
    publisher_entity = metadata[parent_entity[0]]
    contact_point = utils.get_norm_value(publisher_entity, "contactPoint")
    if contact_point != []:
        contactPoint_entity = metadata[contact_point[0]]
        type = utils.get_norm_value(contactPoint_entity, "@type")
        if type[0] == "ContactPoint":
            contact_result[contact_point[0]] = True
        else:
            contact_result[contact_point[0]] = [False, error_message["TypeError"].format(contact_point)]
            
def contact_info_check(tar_file, extension):
    
    """
    A RO-Crate SHOULD have contact information, using a contextual entity of type ContactPoint.
    For more informaiton, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#contact-information>
    """
    
    NAME = "Contact information check"
    error_message = {
        "TypeError": "Invlaid Type Value at {}"
    }
    
    ###dictionary to store the checking result
    contact_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        if utils.get_norm_value(entity, "@type")[0] == "Dataset":
            author = utils.get_norm_value(entity, "author")
            publisher = utils.get_norm_value(entity, "publisher")
            
            ### check contact information property of both author and publisher
            if author != []:
                upd_contactInfoType_rlt(metadata, author, contact_result, error_message)
            if publisher != []:
                upd_contactInfoType_rlt(metadata, publisher, contact_result, error_message)
    
    for values in contact_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
    
    return Result(NAME)


def upd_citationRlt(citation, metadata, citation_result, error_message):
    if utils.is_url(citation):
        citation_entity = metadata[citation[0]]
        type = utils.get_norm_value(citation_entity, "@type")
        try:
            type = type[0]
        except IndexError:
            citation_result[citation[0]] = [False, "No Type Provided"]
        if type == "ScholarlyArticle" or type == "CreativeWork":
            citation_result[citation[0]] = True
        else:
            citation_result[citation[0]] = [False, error_message["TypeError"].format(citation)]
    else:
        citation_result[citation[0]] = [False, error_message["IDError"].format(citation)]
def get_citation(entity, metadata, citation_result, error_message):
    citation = utils.get_norm_value(entity, "citation")
    try: 
        citation = citation[0]
        upd_citationRlt(citation, metadata, citation_result, error_message)
    except IndexError:
        pass
    
def citation_check(tar_file, extension):
    
    """
    RO-Crate JSON-LD MUST include a URL (for example a DOI URL) as the @id of a publication using the citation property
    For more information and examples, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#publications-via-citation-property>
    """
    
    NAME = "Citation property check"
    error_message = {
        "TypeError": "Invalid Type Value at {}",
        "IDError": "Invalid ID Value at {}"
    }
    
    ### Dict to store the checking result
    citation_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        type = utils.get_norm_value(entity, "@type")[0]
        if type == "Dataset" or type == "File":
            get_citation(entity, metadata, citation_result, error_message)

    for values in citation_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])

    return Result(NAME)


def upd_publisherRlt(publisher, metadata, publisher_result, error_message):
    try:
        publisher_entity = metadata[publisher[0]]
        type = utils.get_norm_value(publisher_entity, "@type")
        try:
            type = type[0]
        except IndexError:
            publisher_result[publisher[0]] = [False, "NO Type Provided"]
        if type == "Organization" or type == "Person":
            publisher_result[publisher[0]] = True
        else:
            publisher_result[publisher[0]] = [False, error_message["TypeError"].format(publisher[0])]
    except KeyError:
        publisher_result[publisher[0]] = [False, error_message["ReferencingError"].format(publisher[0])]


def get_publisher(entity, metadata, publisher_result, error_message):
    publisher = utils.get_norm_value(entity, "publisher")
    if publisher != []:
        if utils.is_url(publisher[0]):
            upd_publisherRlt(publisher, metadata, publisher_result, error_message)
                
def publisher_check(tar_file, extension):
    
    """
    The Root Data Entity SHOULD have a publisher property.
    For more information and examples, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#publisher>
    """
    
    NAME = "Publisher property check"
    error_message = {
        "TypeError": "Invalid Type Value at {}",
        "ReferencingError": "Invalid Referencing {} or Not Provided"
    }
    
    publisher_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        publisher = utils.get_norm_value(entity, "publisher")          
        ### publisher SHOULD be an Organization though it MAY be a Person.
        get_publisher(entity, metadata, publisher_result, error_message)
    
    for values in publisher_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
    
    return Result(NAME)


def upd_funderRlt(funders, metadata, funder_result, error_message):
    for funder in funders:
        try:
            funder_entity = metadata[funder]
            type = utils.get_norm_value(funder_entity, "@type")
            if type[0] == "Organization" or type[0] == "Person":
                funder_result = True
                get_funder(funder_entity, metadata, funder_result, error_message)
            else:
                funder_result[funder] = [False, error_message["TypeError"].format(funder)]
        except KeyError:
            funder_result[funder] = [False, error_message["ReferencingError"].format(funder)]

def get_funder(depth, entity, metadata, funder_result, error_message):
    depth += 1
    funders = utils.get_norm_value(entity, "funder")
    if depth <= 2:
        if funders != []:
            upd_funderRlt(funders, metadata, funder_result, error_message)
    else:
        funder_result["Warning"] = "There are too many unecessary funders."

def funder_check(tar_file, extension):
    """
    The RO-Crate JSON-LD SHOULD contain an entity for the project using type Organization, referenced by a funder property
    For more information, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#funding-and-grants>
    """
    
    NAME = "Funder property check"
    error_message = {
        "TypeError": "Invalid Type Vlaue at {}",
        "ReferencingError": "Reference Entity {} Missing"
    }
    
    funder_result = {}
    depth = 0
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    
    for entity in metadata.values():
        if utils.get_norm_value(entity, "@type")[0] == "Dataset":
            get_funder(depth, entity, metadata, funder_result, error_message)
            
    for values in funder_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
        if isinstance(values, str):
        	return Reuslt(NAME, code = 1, message = values)
    
    return Result(NAME)


def upd_copyrightRlt(copyright, metadata, licensing_result, error_message):
    try:
        copyright_entity = metadata[copyright[0]]
    except KeyError:
        licensing_result[copyright[0]] = [False, error_message["ReferencingError"]]
    type = utils.get_norm_value(metadata[copyright[0]], "@type")
    if type == "Person" or type == "Organization":
        licensing_result[copyright[0]] = True
    else:
        licensing_result[copyright[0]] = [False, error_message["TypeError"].format(copyright[0])]

def upd_licenseRlt(entity, license, metadata, licensing_result, error_message):
    if utils.is_url(license[0]) and utils.get_norm_value(entity, "@id")[0] != "./" and utils.get_norm_value(entity, "@id"[0] != "ro-crate-metadata.json"):
        try:
            license_entity = metadata[license[0]]
        except KeyError:
            licensing_result[license[0]] = [False, error_message["ReferencingError"]]
        type = utils.get_norm_value(license_entity, "@type")
        if type == "CreativeWork":
            licensing_result[license[0]] = True
        else:
            licensing_result[license[0]] = [False, error_message["TypeError"].format(license[0])]
    else:
        licensing_result[license[0]] = [False, error_message["IDError"].format(license[0])]

def licensing_check(tar_file, extension):

    """
    The data entity SHOULD have a license property referencing 
    a Contextual Entity with a type CreativeWork to describe the license.
    For more details and examples, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#licensing-access-control-and-copyright> 
    """
    
    NAME = "Licensing property check"
    error_message = {
        "TypeError":"Invalid Type Value at {}", 
        "IDError" : "Invalid ID Value at {}. It must be an URL.", 
        "ReferencingError": "Invalid Referencing or NOT Provided"
    }
    
    licensing_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        copyright = utils.get_norm_value(entity, "copyrightHolder")
        license = utils.get_norm_value(entity, "license")
        if license != []:
            upd_licenseRlt(entity, license, metadata, licensing_result, error_message)
        if copyright != []:
            upd_copyrightRlt(copyright, metadata, licensing_result, error_message)
    
    for values in licensing_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
        
    return Result(NAME)

def geo_correctness(entity, metadata, geo_result, error_message):
    geo = utils.get_norm_value(entity, "geo")
    if geo != []:
        try:
            geo_entity = metadata[geo[0]]
            geo_entity_type = utils.get_norm_value(geo_entity, "@type")
            if geo_entity_type == "GeoCoordinates" and utils.get_norm_value(entity, "name") != []:
                geo_result[geo[0]] = True
            else:
                geo_result[geo[0]] = [False, error_message["TypeError"].format(geo[0])]
        except KeyError:
            geo_result[geo[0]] = [False, error_message["ReferencingError"]]

def type_correctnessWithGeo(id_, entity, metadata, geo_result, error_message):
    place_type = utils.get_norm_value(entity, "@type")
    if place_type[0] == "Place":
        geo_correctness(entity, metadata, geo_result, error_message)
    else:
        geo_result[id_] = [False, error_message["TypeError"].format(id_)]

def places_check(tar_file, extension):
    
    """
    Data Entity with a Contextual Entity representing a geographical location or region
    SHOULD have a property of contentLocation with a value of type Place.
    For more information, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#places>
    """
    
    NAME = "Places property check"
    error_message = {
        "TypeError":"Invalid Type Value at {}",
        "ReferencingError": "Invalid Refernencing or Not Provided"
    }
    
    geo_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        id_ = utils.get_norm_value(entity, "@id")[0]
        entity_type = utils.get_norm_value(entity, "@type")
        if entity_type[0] == "Place":
            geo_correctness(entity, metadata, geo_result, error_message)
        if id_.startswith("http://sws.geonames.org/") or id_.startswith("https://www.geonames.org/"):
            type_correctnessWithGeo(id_, entity, metadat, geo_result, error_message)
    
    for values in geo_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, messge = values[1])
    
    return Result(NAME)


def upd_timeRlt(entity, error_message, time_result):
    time = utils.get_norm_value(entity, "temporalCoverage")
    if time != []:
        if isinstance(time[0], str) or utils.is_url(time[0]) or isinstance(time[0], datetime):
            time_result[time[0]] = True
        else:
            time_result[time[0]] = [False, error_message["TypeError"].format]

def time_check(tar_file, extension):
    
    """
    To describe the time period which a RO-Crate Data Entity 
    (or the root data entity) is about, use temporalCoverage
    For more information, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#time>
    """
    
    NAME = "Time property check"
    error_message = {
        "TypeError": "Invalid Type Value at {}"
    }
    
    time_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))

    for entity in metadata.values():
        upd_timeRlt(entity, error_message, time_result)
    
    for values in time_result.values():
        if isinstance(values, list):
            return Result(NAME, code=-1, message = values[1])
        elif isinstance(values, str):
            return Result(NAME, code = 1, message = values)
    
    return Result(NAME)


def thumbnails_check(tar_file, extension):
    
    """
    Multiple file in same property(via hasFile) with one of thumbnails. 
    The thumbnails SHOULD be included in the RO-Crate
    For more information and exaples, please check:
    <https://www.researchobject.org/ro-crate/1.1/contextual-entities.html#thumbnails>
    """
    
    NAME = "Thumbnails property check"
    error_message = {
        
    }
    
    thumbnails_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    for entity in metadata.values():
        thumbnail = utils.get_norm_value(entity, "thumbnail")
        hasFile = utils.get_norm_value(entity, "hasFile")
        if thumbnail != []:
            if thumbnails[0] in hasFile:
                thumbnails_result = True
            else:
                thumbnails_result = [False, error_message[""]]


def recognisedWkf_upd(extension_set, entity, workflow_result, id_, error_message):
    extension = os.path.splitext(id_)[1]
    if extension in extension_set:
        type = utils.get_norm_value(entity, "@type")
        name = utils.get_norm_value(entity, "name")
        if "File" in type and "SoftwareSourceCode" in type and "ComputationalWorkflow" in type and name != []:
            workflow_result[id_] = True
        else:
            workflow_result[id_] = [False, error_message["TypeError"].format(id_)]

def unrecognisedWfk_upd(type, extension_set, entity, workflow_result, warning_message):
    extension = os.path.splitext(utils.get_norm_value(entity,"@id")[0])[1]
    if extension not in extension_set:
        if "File" in type and "SoftwareSourceCode" in type:
            workflow_result[utils.get_norm_value(entity, "@id")[0]] = True
        else:
            workflow_result[utils.get_norm_value(entity, "@id")[0]] = warning_message["UnrecognizedWkf"].format(extension)

def scripts_and_workflow_check(tar_file, extension):
    
    """
    For workflow RO-Crate, if there is an unrecognised workflow file, the function will return an warning message.
    Please check more details at RO-Crate website:
    <https://www.researchobject.org/ro-crate/1.1/workflow-and-scripts.html>
    """

    NAME = "Scripts and workflow check"
    wkfext_path = '/Users/xuanqili/Desktop/ro-crate-validator-py/src/workflow_extension.txt'

    error_message = {
        "WorkflowError":"Scripts and Workflow is Wrong",
        "TypeError": " @type for workflow file {} must have File, SoftwareSourceCode and ComputationalWorkflow as value."
    }
    warning_message = {
        "UnrecognizedWkf" : "WARNING: {} is not a recognised workflow extension. Please raise an issue at GitHub: <https://github.com/ResearchObject/ro-crate-validator-py/issues>."
    }
    
    ### dictionary to store checking result
    workflow_result = {}
    
    context, metadata = rocrate.read_metadata(os.path.join(tar_file, "ro-crate-metadata.json"))
    
    ### check if recognised workflow file meets the requirments
    for entity in metadata.values():
        id_ = utils.get_norm_value(entity, "@id")[0]
        with open (wkfext_path, "r") as file:
            extension_set = file.read().splitlines()
        recognisedWkf_upd(extension_set, entity, workflow_result, id_, error_message)
    
    ### check unrecognised workflow file with ComputaionalWorkflow in its @type
    for entity in metadata.values():
        type = utils.get_norm_value(entity, "@type")
        if "ComputationalWorkflow" in type:
            unrecognisedWfk_upd(type, extension_set, entity, workflow_result, warning_message)

    ### fucntion will return True only when the all of the recognised workflow file are correct      
    for values in workflow_result.values():
        if isinstance(values, list):
            return Result(NAME, code = -1, message = values[1])
        elif isinstance(values, str):
            return Result(NAME, code = 1, message = values)
        else:
            return Result(NAME)
    
    return Result(NAME, code = -1, message = error_message["WorkflowError"])
                