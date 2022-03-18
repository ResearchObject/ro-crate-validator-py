import setuptools 

setuptools.setup(name = 'rocrateValidator',
	version = '0.2.0', 
	description = 'This is python library for ro-crate validator',
	package=["src",
			"src.rocrateValidator",
			"test", 
			"test.integration"
			# "test.samples"
			# "test.samples/invalid", 
			# "test.samples/valid"
			],
	package_data = {"rocrateValidator": ["rocrateValidator/workflow_extension.txt", "rocrateValidator/check_list.txt"]},
  	include_package_data=True,
	packages=setuptools.find_packages(),
	url = "https://github.com/ResearchObject/ro-crate-validator-py",
	zip_safe = False
	)