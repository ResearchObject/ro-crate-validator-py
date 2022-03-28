# Categorising Broken RO-Crate


## 1. Invalid Json Test
**_Test 01 brackets_**

**_Purpose:_** Json objects literals are surrounded by curly braces { }.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/wrong_array_bracket.json

**_Test 02 separators_**

**_Purpose:_** Key and values are separated by a colon : , and each pair of key/value are separated by a comma , .
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_seperatorOf_key_value.json

**_Test 03 key and value format_**

**_Purpose:_** Key must be strings, written with double quotes, and values must be a valid JSON data type except function, time and undefined.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_json_stringValue.json

## 2. Unsupported/Unexpected Json-ld

**_Test 01 Missing type_**

**_Purpose:_** Principles of [Linked Data](https://json-ld.org/spec/latest/json-ld-api-best-practices/#dfn-linked-data) dictate that messages SHOULD be self describing, which includes adding a type to such messages.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/unsupported_jsonld_missingType.json

## 3. Invalid Json-ld Compacted from

**_Test 01 Duplicated keywords_**

**_Purpose:_**  the term must not equal any of the JSON-LD keywords, other than @type
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_compacted_term_duplicatedKeywords.json

**_Test 02 Empty string term_**

**_Purpose:_**  the term must not be empty string (“”) as not all programming languages are able to handle empty JSON keys.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_compacted_term_emptyString.json
  

**_Test 03 term started with @ character_**

**_Purpose:_**  a term should not start with an @ character followed by one or more ALPHA characters to avoid forward-compatibility.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/term_start_with@.json

## 4. Invalid Json-ld

**_Test 01 Duplicated subjects_**

**_Purpose:_**  Each unique subject in the set of triples is represented as a key in the root object. NO key may appear more than once in the root object.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/duplicate_predicated_keys.json

## 5. Wrong schema.org

**_Test 01 wrong schema.org_**

**_Purpose:_**  JSON-LD uses the vocabulary of schema.org to describe what a web page is about
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/wrong_schema.json

## 6.Invalid root data entity

**_Test 01 Invalid root data entity @type value_**

**_Purpose:_** @type must be Dataset
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_rootDataENtity_@typeValue.json

**_Test 02 Invalid id in about property_**

**_Purpose:_**  For each entity in @graph array, if the comformsTo property is a URI that starts with [https://w3id.org/ro/crate/](https://w3id.org/ro/crate/), from this entity’s about object keep the @id URI as variable root
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_is_inAboutObj.json

**_Test 03 Missing about property_**

**_Purpose:_**  The Ro-Crate Metadata file descriptor MUST have an about property referencing the _Root Data Entity_, which SHOULD have an '@id' of './'.
**_Input example:_** https://github.com/ResearchObject/ro-crate-validator-py/blob/main/test/samples/invalid/invalid_is_inAboutObj.jsonß


## Mini-Report 

**Links:** https://docs.google.com/document/d/1fC7_BZYxyM1V9L2g6XnGdbvYiwNOg_YdhRLMPUoFf4M/edit