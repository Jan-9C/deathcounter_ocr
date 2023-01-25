import json
import sys

def merge_json_files(output_file, *files):
    merged_data = []
    for file in files:
        with open(file) as f:
            data = json.load(f)
            merged_data.extend(data)
    with open("completedMasks\\"+output_file, 'w') as f:
        json.dump(merged_data, f, separators=(',', ':'))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage python maskmerger.py <output file name> <input file1> <input file2> <...>")
        print("Error: Please provide the output file name and at least two input files")
    else:
        merge_json_files(sys.argv[1], *sys.argv[2:])