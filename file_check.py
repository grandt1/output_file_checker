import hashlib
import os
import argparse
import csv


parser = argparse.ArgumentParser(
    description='Compare two directories for similarity.')

parser.add_argument(
    '--dir_1',
    help='Path to first directory',
    metavar='</path/to/run/>',
    dest='dir_1',
    required=True
)

parser.add_argument(
    '--dir_2',
    help='Path to second directory',
    metavar='</path/to/run/>',
    dest='dir_2',
    required=True
)

parser.add_argument(
    '--ignore',
    help='CSV containing files to ignore',
    metavar='</path/to/csv/>',
    dest='ignore_list',
    required=False
)

parser.add_argument(
    '--checksum',
    help='Use checksum, slower but much higher certainty',
    action='store_true'
)

args = parser.parse_args()

# Load list of files to ignore
if args.ignore_list:
    with open(args.ignore_list, 'r') as f:
        ignore_list = set(f.readlines()[0].replace("\n", "").split(','))
else:
    ignore_list = set()

# Function to calculate checksum
# Returns the checksum string


def file_md5_checksum(filename, block_size=2**20):

    # Empty files can cause false errors due to encoding
    if os.path.getsize(filename) == 0:
        return 'd41d8cd98f00b204e9800998ecf8427e'  # Manually set to empty checksum

    with open(filename, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()

# Iterate over each directory, defaults to comparing filesize


def compare_dirs(dir_1, dir_2, method=os.path.getsize):

    files_checked = 0  # Initialise counter

    results = dict()

    for root, _, files in os.walk(dir_1):
        for name in files:
            # Results are stored in form {commonpath: [dir1_result, dir2_result]}
            # Empty string as placeholder for second dir
            if name not in ignore_list:
                relpath = os.path.relpath(os.path.join(root, name), dir_1)
                results[relpath] = [method(os.path.join(root, name)), '']
                files_checked += 1  # File counter because I'm impatient
                print(f'Files checked: {files_checked}', end='\r', flush=True)

    print(f"Files in Dir_1 = {files_checked}")

    files_checked = 0

    for root, _, files in os.walk(dir_2):
        for name in files:
            relpath = os.path.relpath(os.path.join(root, name), dir_2)

            # If file in dir1 add result
            if name not in ignore_list:
                if results[relpath]:
                    results[relpath][1] = (method(os.path.join(root, name)))
                    files_checked += 1
                    print(f'Files checked: {files_checked}',
                          end='\r', flush=True)

                # Else add to dict and add empty string for dir1_result
                else:
                    results[relpath] = ['', method(os.path.join(root, name))]
                    files_checked += 1
                    print(f'Files checked: {files_checked}',
                          end='\r', flush=True)
    print(f"Files in Dir_2 = {files_checked}")
    output = []
    verified = 0

    # write results dictionary to csv
    with open('/home/grandt/results.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(['File Name', 'File Check 1', 'File Check 2'])
        for key, value in results.items():
            writer.writerow([key, value[0], value[1]])

    # Iterate over results, printing mismatches and reasons
    for key, value in results.items():
        if not value[0]:
            output.append(f'{key} is not in truth directory')
            continue
        if not value[1]:
            output.append(f'{key} is not in test directory')
            continue
        check = value[0] == value[1]
        if check:
            verified += 1
        else:
            output.append(f'{key} failed check')

    output = "\n".join(
        output + [f'{verified}/{len(results)} succesfully verified']
        )

    return output


if __name__ == "__main__":

    # Use checksum if flag used
    if args.checksum:
        print("\n", compare_dirs(args.dir_1, args.dir_2, method=file_md5_checksum))
    else:
        print("\n", compare_dirs(args.dir_1, args.dir_2))
