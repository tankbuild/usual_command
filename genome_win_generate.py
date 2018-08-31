import argparse
import sys
import os
from collections import defaultdict
import time
import datetime


# How to use it
# python[3] genome_win_generate.py -i path_to_depth_file -l path_to_chr_length_file
# -w window_size(default 500) -s step(default 250)

parser = argparse.ArgumentParser(
    description='Generates a sliding window depth file without overlap',
    usage='''python[3] genome_win_generate.py -i path_to_depth_file
          -l path_to_chr_length_file [-w window_size] [-s step] [-o output_file]

Options:  -i\t--input-file\tPath to a file containing the iutput of depth
\t  -l\t--chr_length\tPath to a file containing the iutput of chromosomes length
\t  -w\t--window_size\tPath to window_size: default 500
\t  -s\t--step\tPath to step: default 250
\t  -o\t--output-file\tPath to output file (default: male_femele_win500.tsv)
''')
parser.add_argument('--input-file', '-i',
                    help='Path to a file containing the iutput of depth')
parser.add_argument('--chr-length', '-l',
                    help='Path to a file containing the iutput of chromosomes length')
parser.add_argument('--window-size', '-w', nargs='?',
                    help='Path to a integer --win to use',
                    default=500)
parser.add_argument('--step', '-s', nargs='?',
                    help='Path to a integer --step to use',
                    default=250)
parser.add_argument('--output-file', '-o',
                    help='Path to output file', nargs='?',
                    default='male_femele_win500.tsv')

args = parser.parse_args(sys.argv[1:])

if not args.input_file or not os.path.isfile(args.input_file):
    print('\nError: no valid input file specified\n')
    parser.print_usage()
    print()
    exit(1)

if not args.chr_length or not os.path.isfile(args.chr_length):
    print('\nError: no valid input file specified\n')
    parser.print_usage()
    print()
    exit(1)

if args.window_size <= args.step:
    print('\nError: window size should be more than step')
    parser.print_usage()
    print()
    exit(1)


def analysis(input_file_path='',
             chr_length_path='',
             window_size=500,
             step=250,
             output_file_path='male_femele_win500.tsv'):
    # Generate a library to store raw data of contig_name, pos, male_depth, and female_depth
    depth_data = defaultdict(lambda: defaultdict(list))
    depth_file = open(input_file_path, 'r')
    t1 = time.time()
    for line in depth_file:
        line_split = line[:-1].split('\t')
        contig_name = line_split[0]
        pos = line_split[1]
        male_depth = line_split[2]
        female_depth = line_split[3]
        depth_data[contig_name][pos].append(male_depth)
        depth_data[contig_name][pos].append(female_depth)
    t2 = time.time()
    # Print('library built in {} seconds.'.format(round(t2 - t1, 4)))
    print('Depth library was built in {} seconds.'.format(str(datetime.timedelta(seconds=t2 - t1))))
    # Generate a library to store chr_length raw data of contig_name and length
    len_data = defaultdict(int)
    len_file = open(chr_length_path, 'r')
    t3 = time.time()
    for line in len_file:
        line_split = line[:-1].split('\t')
        contig_name = line_split[0]
        length = line_split[1]
        len_data[contig_name] = length
    t4 = time.time()
    print('Length library was built in {} seconds.'.format(str(datetime.timedelta(seconds=t4 - t3))))
    # Generate a library for window with step
    win_data = defaultdict(list)
    for name in len_data:
        start = list(range(1, int(len_data[name]) - step, step))
        end = [window_size + a for a in start]
        win_step = [(a, b) for a, b in zip(start, end)]
        win_data[name] = win_step
    # Finally deal with data
    output_data = defaultdict(dict)
    for contig in depth_data:
        temp_dict = defaultdict(list)
        for win in win_data[contig]:
            s = int(win[0])
            e = int(win[1])
            win_male_depth = 0
            win_female_depth = 0
            num = 0
            for pos in range(s, e + 1):
                pos = str(pos)
                if pos in depth_data[contig].keys():
                    win_male_depth += int(depth_data[contig][pos][0])
                    win_female_depth += int(depth_data[contig][pos][1])
                    num += 1
                else:
                    pass
            if num != 0:
                mean_win_male_depth = str(win_male_depth // num)
                mean_win_female_depth = str(win_female_depth // num)
                position = str(e // 2)
                temp_dict[position].append(mean_win_male_depth)
                temp_dict[position].append(mean_win_female_depth)
        output_data[contig] = temp_dict
    # Writing data to output file
    output_file = open(output_file_path, 'w')
    for contig in output_data:
        print(output_data[contig])
        for position in output_data[contig]:
            output_file.write(contig + '\t' + position + '\t' + output_data[contig][position][0] + '\t' + output_data[contig][position][1] + '\n')


analysis(input_file_path=args.input_file,
         chr_length_path=args.chr_length,
         window_size=args.window_size,
         step=args.step,
         output_file_path=args.output_file)
