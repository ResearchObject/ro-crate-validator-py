import sys
import requests
import tempfile
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'rocrateValidator'))

from rocrateValidator import validate as validate

def validate_rocrate(source):
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)

        if response.status_code != 200:
            raise Exception(f"Failed to download RO-Crate from URL: {source}")

        with tempfile.NamedTemporaryFile(mode='wb', delete=True, dir='/tmp') as temp_file:
            temp_file.write(response.content)
            temp_file.flush()
            result = validate.validate(temp_file.name)
    else:
        # Handle file path
        result = validate.validate(source)

    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_rocrate.py <path_or_url_to_rocrate>")
        sys.exit(1)

    source = sys.argv[1]
    v = validate_rocrate(source)
    v.validator()
