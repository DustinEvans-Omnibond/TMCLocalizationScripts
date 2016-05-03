import json
import operator
import sys, getopt
from xlwt import Workbook, easyxf

def main(argv):
	old_root_file = ""
	new_root_file = ""
	lang_file = ""
	excel_file = "common.xls"
	
	try:
		opts, args = getopt.getopt(argv, "n:o:f:x:")
	except getopt.GetoptError:
		print "CompareCommon.py -o <old common.js> -n <new common.js> -f <foreign language common.js> -x <output excel file>"
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == "-o":
			old_root_file = arg
		elif opt == "-n":
			new_root_file = arg
		elif opt == "-f":
			lang_file = arg
		elif opt == "-x":
			excel_file = arg
	
	# check if required files are given
	if old_root_file != "" and new_root_file != "" and lang_file != "":
		# first read the js files in can make them dictionaries
		old_root_dict = read_js_file(old_root_file)
		new_root_dict = read_js_file(new_root_file)
		lang_dict = read_js_file(lang_file)
		# convert the dictionaries to something easier to compare and read
		converted_old = convert_dict(old_root_dict)
		converted_new = convert_dict(new_root_dict)
		converted_lang = convert_dict(lang_dict)
		# compare the dictionaries
		output_list = compare_converted_dicts(converted_old, converted_new, converted_lang)
		# create and write data to excel file
		create_excel_book(output_list, excel_file)
	else:
		print "ERROR: Must have an old/new root and language file!"

		
def read_js_file(file_path):
	ret_dict = {}
	
	try:
		fp = open(file_path, "rb")
		file_content = fp.read()
		valid_content = file_content[file_content.find("{"):file_content.rfind("}")+1]
		ret_dict = json.loads(valid_content)
		fp.close()
		# Check to see if a "root" key is in the ret_dict,
		if "root" in ret_dict:
			ret_dict = ret_dict["root"]
	except IOError:
		print "ERROR: Couldn't open ", file_path
	except ValueError:
		print "ERROR: No JSON object could be decoded"
	
	return ret_dict

def convert_dict(main_dict):
	parsed_dict = {}
	parsed_dict = recursive_build(main_dict, parsed_dict, "")
	
	return parsed_dict

def recursive_build(main_dict, output_dict, prev_key):
	if isinstance(main_dict, basestring):
		return {prev_key: main_dict}
	else:
		for key in main_dict.iterkeys():
			if len(prev_key) > 0:				
				output_dict.update(recursive_build(main_dict[key], output_dict, prev_key + "." + key))
			else:
				output_dict.update(recursive_build(main_dict[key], output_dict, key))
		
	return output_dict
	
def compare_converted_dicts(old_dict, new_dict, lang_dict):
	# go through the new_dict and compare it to old_dict
	# to get a diff_dict
	diff_dict = lang_dict.copy()
	for key in new_dict.iterkeys():
		if key in old_dict:
			# compare values and add to diff_dict if different
			if new_dict[key] != old_dict[key]:
				diff_dict.update({key: new_dict[key]})
		else:
			# add to diff_dict
			diff_dict.update({key: new_dict[key]})
	
	# sort and go through and compare new_dict to diff_dict
	# and create a list of tuples containing the
	# key, English, and translation
	new_lang_dict = {}
	for key in new_dict.iterkeys():
		if key in diff_dict:
			new_lang_dict.update({key: diff_dict[key]})
	
	sorted_new_dict = sorted(new_dict.items(), key=operator.itemgetter(0))
	sorted_new_lang = sorted(new_lang_dict.items(), key=operator.itemgetter(0))
	
	output_list = []
	for i in range(len(sorted_new_dict)):
		output_list.append([sorted_new_dict[i][0], sorted_new_dict[i][1], sorted_new_lang[i][1]])

	return output_list

	
# create_excel_book ---------------------------
# creates the Excel file and writes data to it
# it required layout for translation purposes
def create_excel_book(output_list, output_file):
	book = Workbook(encoding="utf-8")
	sheet = book.add_sheet("Sheet 1")
	
	# Size the first 3 columns
	for i in range(3):
		sheet.col(i).width = 20000

	# Create the headers
	header_style = easyxf('font: bold true;' 'alignment: horizontal center;' 'alignment: wrap True;')
	sheet.write(1, 0, "Label", header_style)
	sheet.write(1, 1, "English", header_style)
	sheet.write(1, 2, "Translation", header_style)

	# Go through output_list and write per row starting at
	# 3rd row
	wrap_style = easyxf('alignment: wrap true;')
	current_row = 2
	for i in range(len(output_list)):
		sheet.write(current_row, 0, output_list[i][0], wrap_style)
		sheet.write(current_row, 1, output_list[i][1], wrap_style)
		sheet.write(current_row, 2, output_list[i][2])
		current_row = current_row + 1
	
	# write the output excel file
	book.save(output_file)
	
# Call main
main(sys.argv[1:]);