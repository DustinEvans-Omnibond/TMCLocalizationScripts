import json
import sys, getopt
from xlrd import open_workbook

# main ----------------------------
def main(argv):
  excel_file = ""
  output_file = "output_common_new.js"
  
  try:
    opts, args = getopt.getopt(argv, "f:o:")
  except getopt.GetoptError:
    print "ExcelToCommon.py -f <Excel Filepath> -o <Output JS Filepath>"
    sys.exit(2);
	
  for opt, arg in opts:
    if opt == "-f":
      excel_file = arg
    elif opt == "-o":
      output_file = arg

  # check if excel filepath was specified
  if excel_file != "":
    # read in the excel file and turn into dictionary
    excel_dict = read_excel_file(excel_file)
    # write out the new common.js output file
    write_output_file(excel_dict, output_file)
  else:
    print "ERROR: Must specify an Excel file!"

# read_excel_file -------------------------	
def read_excel_file(file_path):
  excel_dict = {}
  
  try:
    book = open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    for row_index in range(sheet.nrows):
      label = sheet.cell(row_index, 0).value.encode("utf-8")
      translation = sheet.cell(row_index, 2).value.encode("utf-8")
      if (label != "" and label.lower() != "label"):
        excel_dict = update_excel_dict(excel_dict, label, translation)  
  except IOError:
    print "ERROR: Couldn't open", file_path
	
  #print json.dumps(excel_dict)
  return excel_dict

# update_excel_dict ---------------------------  
def update_excel_dict(excel_dict, label, translation):
  # Break label up by . notation
  keys = label.split(".")
  temp = excel_dict
  for k in range(len(keys)):
    if k < len(keys)-1:
      if keys[k] in temp:
        temp = temp[keys[k]]
      else:
        temp[keys[k]] = {}
        temp = temp[keys[k]]
    else:
      temp[keys[k]] = translation

  return excel_dict

# read_trans_file ----------------------------
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

# compare_dicts ------------------------------------
def compare_dicts(excel_dict, trans_dict):
  # combine the two dicts, the excel_dict's key:values
  # will overwrite the trans_dict's key:values
  combined_dict = trans_dict
  combined_dict.update(excel_dict)
  
  return combined_dict

# write_output_file --------------------------------
def write_output_file(diff_dict, file_path):
  try:
    fp = open(file_path, "wb")
    fp.write("define(")
    json.dump(diff_dict, fp, ensure_ascii=False, indent=4)
    fp.write(");")
    fp.close()
  except IOError:
    print "ERROR: Could not write out to", file_path

  return {}

main(sys.argv[1:]);