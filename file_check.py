# import hashlib
import os
import argparse

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

args = parser.parse_args()


# def filemd5(filename, block_size=2**20):
#     with open(filename, 'rb') as f:
#         md5 = hashlib.md5()
#         while True:
#             data = f.read(block_size)
#             if not data:
#                 break
#             md5.update(data)
#     return md5.digest()


def compare_dirs(dir_1, dir_2):
    results = dict()
    for root, dirs, files in os.walk(dir_1):
        for name in files:
            results[name] = [os.path.getsize(os.path.join(root, name)), '']

    for root, dirs, files in os.walk(dir_2):
        for name in files:
            if results[name]:
                results[name][1] = (os.path.getsize(os.path.join(root, name)))
            else:
                results[name] = ['', os.path.getsize(os.path.join(root, name))]

    output = []
    verified = 0
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
    print(compare_dirs(args.dir_1, args.dir_2), sep="\n")
