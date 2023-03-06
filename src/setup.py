import setuptools 

setuptools.setup(name = 'rocrateValidator',
	version = '0.2.15', 
	description = 'This is python library for ro-crate validator',
	package=["src",
			"src.rocrateValidator"
			],
	package_data = {"rocrateValidator": ["rocrateValidator/workflow_extension.txt", "rocrateValidator/check_list.txt"]},
  	include_package_data=True,
	install_requires=["requests>=2", "rocrate>=0.7", "PyShEx>=0.7"],
	packages=setuptools.find_packages(),
	url = "https://github.com/ResearchObject/ro-crate-validator-py",
	zip_safe = False
	)