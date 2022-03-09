def workflow_extension_update(extension):
    with open ("workflow_extension.txt", "a") as file:
        file.write("\n")
        file.write("%s" % extension)

class Result:
    def __init__(self, NAME = None, code = 0, message = ""):
        self.NAME = NAME
        self.code = code 
        self.message = message