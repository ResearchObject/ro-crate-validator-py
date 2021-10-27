import os
import os.path
import zipfile
# from src.existence_check import existence as E
import pytest
import sys

def existence_check(target_file_name):

	cur_dir = os.getcwd()
	tar_dir = os.path.dirname(os.path.join(cur_dir, 'samples/'))
	os.chdir(tar_dir)

	if os.path.exists(target_file_name) == True:
		if os.path.splitext(target_file_name)[1] == '':
			return 'directory'
		elif os.path.splitext(target_file_name)[1] == '.txt':
			return 'BagIt file'
		elif os.path.splitext(target_file_name)[1] == '.zip':
			return 'zipfile'
		elif os.path.splitext(target_file_name)[1] == '.tar':
			return 'tarfile'
		elif os.path.splitext(target_file_name)[1] == '.gz':
			return 'gzfile'
	else:
		print("There is no file or directory called %s" % target_file_name)
		print("The file existence check - FAIL")
		sys.exit()

	
def file_size_check(target_file_name):

	file_size = os.path.getsize(target_file_name)
	if file_size == 0:
		print("The file size is 0 byte.")
		print("The file size check - FAIL")
		sys.exit()
	else: 
		return True

def 

def main():

	# file_set = [f for f in os.listdir(parent_dir)]
	target_file_name = sys.argv[1]
	check_result = existence_check(target_file_name)
	
	if check_result != False:
		print("The file existence check - PASS")
		print("The %s" %check_result, target_file_name + " exists")

	if file_size_check(target_file_name) == True:
		print("The file size check - PASS")


	
		





if __name__ == "__main__":
	main()



	

