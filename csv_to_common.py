#-------------------------------------------------------------------------------
# Name:        csv_to_common.py
# Purpose:     Takes CSV file and converts to Dojo NLS common.js file format.
# Requires:    Python 3.6.x, codecs module, UTF-8 file encoding.
# Usage:       csv_to_common.py -i <CSV file path> -o <common.js file path>
#
# Author:      Dustin Evans
#
# Created:     18/05/2017
# Copyright:   (c) Omnibond Systems, LLC. 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
import codecs
import sys, getopt
import operator



def main(argv):
    input_file = None
    output_file = "translation.js"

    try:
        opts, args = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError:
        print("csv_to_common.py -i <CSV file path> -o <common.js file path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        elif opt == "-o":
            output_file = arg

    if input_file is not None:
        output_dict = parse_csv_file(input_file)
        write_common_js_file(output_file, output_dict)




def parse_csv_file(file_path):
    output_dict = {}

    with codecs.open(file_path, mode='r', encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            label = row['Label']
            text = str(row['Text'])
            translation = str(row['Translation'])
            if translation == "":
                translation = text
            primary_key = label.split('.')[0]
            secondary_key = label.split('.')[1]
            if primary_key not in output_dict:
                output_dict[primary_key] = {}
            output_dict[primary_key][secondary_key] = translation

    return output_dict


def write_common_js_file(file_path, output_dict):
    with codecs.open(file_path, mode='w', encoding='utf-8') as fp:
        fp.write('define("dojo/nls/<code>/common", {')
        fp.write('\n')
        num_primary_keys = len(output_dict)
        for primary_key in output_dict:
            fp.write('\"' + primary_key + '\":{\n')
            num_secondary_keys = len(output_dict[primary_key])
            for secondary_key in output_dict[primary_key]:
                if num_secondary_keys == 1:
                    fp.write('\"' + secondary_key + '\":\"' + output_dict[primary_key][secondary_key] + '\"\n')
                else:
                    fp.write('\"' + secondary_key + '\":\"' + output_dict[primary_key][secondary_key] + '\",\n')
                num_secondary_keys -= 1
            if num_primary_keys == 1:
                fp.write('}\n')
            else:
                fp.write('},\n')
            num_primary_keys -= 1
        fp.write('});')





if __name__ == '__main__':
    main(sys.argv[1:])
