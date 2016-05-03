import json
import sys, getopt
import operator
from xlwt import Workbook, easyxf

# main -------------------------------------
def main(argv):
	trans_file = ""
	output_file = "new.xls"
	
	try:
		opts, args = getopt.getopt(argv, "f:o:")
	except getopt.GetoptError:
		print "CommonToExcel.py -f <common.js file path> -o <Output Excel file path>"
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == "-f":
			trans_file = arg
		elif opt == "-o":
			output_file = arg
	
	if trans_file != "":
		trans_dict = read_trans_file(trans_file)
		parsed_dict = parse_trans_dict(trans_dict)
		sorted_list = sort_dict(parsed_dict)
		create_excel_book(sorted_list, output_file)
	else:
		print "ERROR: Must specify a translation JS file!"

# read_trans_file ------------------------------
# just reads in the translation file and returns it as a dictionary
def read_trans_file(file_path):
	trans_dict = {}
	
	try:
		fp = open(file_path, "rb")
		file_content = fp.read()
		valid_content = file_content[file_content.find("{"):file_content.rfind("}")+1]
		trans_dict = json.loads(valid_content)
		fp.close()
	except IOError:
		print "ERROR: Couldn't open", file_path
	except ValueError:
		print "ERROR: No JSON object could be decoded"

	return trans_dict

# parse_trans_dict ----------------------------
# converts the dictionary into something easier to 
# write into an Excel file
def parse_trans_dict(trans_dict):
	parsed_dict = {}
	parsed_dict = recursive_build(trans_dict, parsed_dict, "")
	
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

# sort_dict -----------------------------------
# Sorts the passed in dictionary object and returns a list
def sort_dict(main_dict):
	return sorted(main_dict.items(), key=operator.itemgetter(0))	
	
# create_excel_book ---------------------------
# creates the Excel file and writes data to it
# it required layout for translation purposes
def create_excel_book(main_list, output_file):
	book = Workbook(encoding="utf-8")
	sheet = book.add_sheet("Sheet 1")
	
	# Size the first 3 columns	
	for i in range(3):
		sheet.col(i).width = 20000

	# Create the headers
	header_style = easyxf('font: bold True;' 'alignment: horizontal center;' 'alignment: wrap True;')
	sheet.write(1, 0, "Label", header_style)
	sheet.write(1, 1, "English", header_style)
	sheet.write(1, 2, "Translation", header_style)
	
	# Go through main_list and write per row starting at
	# 3rd row
	wrap_style = easyxf('alignment: wrap True;')
	current_row = 2
	for i in range(len(main_list)):
		sheet.write(current_row, 0, main_list[i][0], wrap_style)
		sheet.write(current_row, 1, main_list[i][1], wrap_style)
		sheet.write(current_row, 2, "")
		#sheet.write(current_row, 2, "(" + str(current_row+1) + ")" + main_list[i][1])
		current_row = current_row + 1
	
	# write the output excel file
	book.save(output_file)

main(sys.argv[1:]);