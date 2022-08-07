import os
import argparse

#TODO: Feed files and dirs via cmd, if file create a .sorted.xxx file if dir create a sorted dir with .sorted.xxx files
#TODO: support dir so to do a bunch of files
#TODO: Capitals before lowercase
#TODO: Read x amount of lines

def load_into_memory(path: str):
    file = open(path, 'r')
    data = file.read()
    file.close()
    return data

def separate_words(string: str, unique: bool):
    words = string.split()
    if unique:
        words = list(dict.fromkeys(words))
    return words

def sort_alphabetically(container: list):
    print("Sorting alphabetically")
    sorted = []
    for w1 in container:
        if len(sorted) == 0:
            sorted.append(w1)
            continue

        prev = 0
        break_out = False
        for w2 in sorted:
            i = 0
            while i != len(w2):
                if i == len(w1):
                    break_out = True
                    break
                c1 = ord(w1[i].upper())
                c2 = ord(w2[i].upper())
                if c2 < c1:
                    break
                elif c2 > c1:
                    break_out = True
                    break
                i += 1
            if break_out:
                break
            prev += 1

        sorted.insert(prev, w1)
    return sorted

def sort_by_length(container: list):
    print("Sorting by length")
    sorted = []
    for w1 in container:
        if len(sorted) == 0:
            sorted.append(w1)
            continue

        prev = 0
        for w2 in sorted:
            if len(w2) > len(w1):
                break
            prev += 1
        sorted.insert(prev, w1)
    return sorted

def write_to_file(path: str, data: list, overwrite: bool):
    new_path: str
    if overwrite:
        new_path = path
    else:
        name, ext = path.split(os.extsep, 1)
        new_path = name + ".sorted." + ext

    print("Writing to", new_path, "...")
    out = open(new_path, 'w+')
    for i, word in enumerate(data):
        out.write(word + '\n' if len(data) - 1 != i else word)
    out.close()

    print("Success!")

p = argparse.ArgumentParser(description='Sorts file contents', prefix_chars='-')
p.add_argument('path', type= str, action='store', help='Directory or file')
p.add_argument('-a', '--alphabetically', action='store_true', help='Sort alphabetically')
p.add_argument('-l', '--lengthwise', action='store_true', help='Sort lengthwise')
p.add_argument('-o', '--overwrite', action='store_true', help='Overwrite source files')
p.add_argument('-r', '--reverse', action='store_true', help='Reverse sorting priority')
p.add_argument('-u', '--unique', action='store_true', help='Remove duplicate items')
args = p.parse_args()

print("Loading", args.path)
data = load_into_memory(args.path)
words = separate_words(data, args.unique)

if not args.alphabetically and not args.lengthwise:
    args.alphabetically = True

if args.alphabetically: words = sort_alphabetically(words)
if args.lengthwise:     words = sort_by_length(words)
if args.reverse:        words.reverse()

write_to_file(args.path, words, args.overwrite)