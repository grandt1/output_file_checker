import hashlib
import os
import argparse
import csv


parser = argparse.ArgumentParser(description='Compare two directories for similarity.')

parser.add_argument(
    '--dir_1',
    help = 'Path to first directory',
    metavar = '</path/to/run/>',
    dest = 'dir_1',
    required = True
)

parser.add_argument(
    '--dir_2',
    help = 'Path to second directory',
    metavar = '</path/to/run/>',
    dest = 'dir_2',
    required = True
)
parser.add_argument(
        '--checksum',
        help = 'Use checksum, slower but much higher certainty',
        action='store_true'
    )

args = parser.parse_args()

# Function to calculate checksum
# Returns the checksum string
def file_md5_checksum(filename, block_size=2**20):
    if os.path.getsize(filename) == 0: # Empty files can cause false errors due to encoding
        return 'd41d8cd98f00b204e9800998ecf8427e' #Manually set to empty checksum
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
    files_checked = 0
    results = dict()
    for root, dirs, files in os.walk(dir_1):
        for name in files:
            # Results are stored in form {path: [dir1_result, dir2_result]}
            # Empty string as placeholder for second dir
            results[name] = [method(os.path.join(root, name)), '']
            files_checked += 1 # File counter because I'm impatient
            print(f'Files checked: {files_checked}', end='\r', flush=True)

    for root, _, files in os.walk(dir_2):
        for name in files:
            # If file in dir1 add result
            if results[name]:
                results[name][1] = (method(os.path.join(root, name)))
                files_checked += 1
                print(f'Files checked: {files_checked}', end='\r', flush=True)
            # Else add to dict and add empty string for dir1_result
            else:
                results[name] = ['', method(os.path.join(root, name))]
                files_checked += 1
                print(f'Files checked: {files_checked}', end='\r', flush=True)
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
    output = "\n".join([f'{verified}/{len(results)} verified'] + output)
    return output


if __name__ == "__main__":
    # Use checksum if flag used
    if args.checksum:
        print(compare_dirs(args.dir_1, args.dir_2, method = file_md5_checksum), sep="\n")
    else:
        print(compare_dirs(args.dir_1, args.dir_2), sep="\n")