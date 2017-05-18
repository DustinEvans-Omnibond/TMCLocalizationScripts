#-------------------------------------------------------------------------------
# Name:        common_to_csv.py
# Purpose:     Takes a Dojo NLS common.js file and outputs it to CSV.
# Requires:    Python 3.6.x, codecs module, UTF-8 file encoding.
# Usage:       common_to_csv.py -i <common.js file path> -o <output CSV file path>
#
# Author:      Dustin Evans
#
# Created:     15/05/2017
# Copyright:   (c) Omnibond Systems, LLC. 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import csv
import codecs
import sys, getopt
import operator

def main(argv):
    input_file = None
    output_file = "translation.csv"

    try:
        opts, args = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError:
        print("common_to_csv.py -i <common.js file path> -o <output file path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        elif opt == "-o":
            output_file = arg

    if input_file is not None:
        common_dict = parse_common_file(input_file)
        csv_list = convert_to_list(common_dict)
        with codecs.open(output_file, mode='w', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, ['Label', 'Text', 'Translation'])
            writer.writeheader()
            for item in csv_list:
                writer.writerow({'Label': item['Label'], 'Text': item['Text'], 'Translation': item['Translation']})




def parse_common_file(file_path):
    common_dict = {}

    try:
        with codecs.open(file_path, mode='r', encoding='utf-8') as fp:
            file_content = fp.read()
            valid_content = file_content[file_content.find("{"):file_content.rfind("}")+1]
            common_dict = json.loads(valid_content)
            if 'root' in common_dict:
                common_dict = common_dict['root']
    except IOError:
        print("ERROR: Couldn't open", file_path)
    except ValueError:
        print("ERROR: No JSON object could be decoded")

    return common_dict




def convert_to_list(input_dict):
    output_list = []

    for primary_key in input_dict:
        inner_dict = input_dict[primary_key]
        for secondary_key in inner_dict:
            label = primary_key + "." + secondary_key
            text = str(inner_dict[secondary_key])
            output_list.append({'Label': label, 'Text': text, 'Translation': ""})

    return output_list



if __name__ == '__main__':
    main(sys.argv[1:])
