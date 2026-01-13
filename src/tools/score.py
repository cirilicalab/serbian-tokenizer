import argparse
import os
import sys
import glob
import Levenshtein

WORD_SEP = ' '

def parse_args():
    parser = argparse.ArgumentParser(description='Computes tokenized text recall.')
    parser.add_argument('-e', '--expected', help='Expected tokenized text file.', required=False)
    parser.add_argument('-a', '--actual', help='Actual tokenization output file.', required=False)
    parser.add_argument('-ed', '--expected-dir', help='Directory with expected files', required=False)
    parser.add_argument('-ad', '--actual-dir', help='Directory with actual tokenization output files', required=False)
    parser.add_argument('-pfr', '--per-file-results', help='Per file results output file', required=False)

    return parser.parse_args()


def read_word_tokens(path):
    words = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            words.extend(line.split())
    return words


def count_equal(opcodes):
    eq_count = 0
    for opcode in opcodes:
        if opcode[0] == 'equal':
            assert opcode[2] - opcode[1] == opcode[4] - opcode[3]
            eq_count += opcode[2] - opcode[1]
    return eq_count


def process_file_pair(expected_path, actual_path):
    expected_words = read_word_tokens(expected_path)
    actual_words = read_word_tokens(actual_path)

    opcodes = Levenshtein.opcodes(actual_words, expected_words)

    tp = count_equal(opcodes)
    total = len(expected_words)

    return total, tp


def get_filelist(dir):
    pattern = os.path.join(dir, "**", "*")
    file_list = glob.glob(pattern, recursive=True)
    for i in range(0, len(file_list)):
        file_list[i] = os.path.relpath(file_list[i], dir)
    return file_list


def process_directory_pair(actual_dir, expected_dir):
    actual_files = set(get_filelist(actual_dir))
    expected_files = set(get_filelist(expected_dir))

    common_files = expected_files.intersection(actual_files)
    expected_only = expected_files.difference(common_files)
    actual_only = actual_files.difference(common_files)

    # first report warnings
    for path in sorted(expected_only):
        sys.stderr.write("Expected only file: %s\n" % os.path.join(expected_dir, path))
    for path in sorted(actual_only):
        sys.stderr.write("Actual only file: %s" % os.path.join(actual_dir, path))
    
    # process files
    file2result = {}
    for path in common_files:
        expected_path = os.path.join(expected_dir, path)
        actual_path = os.path.join(actual_dir, path)
        file2result[path] = process_file_pair(expected_path, actual_path)
    
    return file2result


def sum_results(results):
    total = 0
    tp = 0
    for i_total, i_tp in results:
        total += i_total
        tp += i_tp
    return total, tp


def report_overall_result(total, tp):
    recall = (100.0 * tp) / total
    print("recall\t%f\ttp\t%d\ttokens\t%d" % (recall, tp, total))


def report_per_file_results(file2result, out_path):
    with open(out_path, 'w', encoding='utf-8') as out_file:
        out_file.write("%s\t%s\t%s\t%s\n" % ("FILE", "RECALL", "TOTAL", "TP"))
        for file, result in sorted(file2result.items()):
            total, tp = result
            recall = (100.0 * tp) / total
            out_file.write("%s\t%f\t%d\t%d\n" % (file, recall, total, tp))



if __name__ == "__main__":
    args = parse_args()


    if args.expected:
        assert args.actual, "Option --actual must be used with --expected."
        assert not args.expected_dir, "Option --expected-dir shouldn't be used with --expected"
        assert not args.actual_dir, "Option --actual-dir shouldn't be used with --expected"
        assert not args.per_file_results, "Option --per-file-results shouldn't be used with --expected"
        total, tp = process_file_pair(args.expected, args.actual)
        report_overall_result(total, tp)

    elif args.expected_dir:
        assert args.actual_dir, "Option --actual-dir must be used with --expected-dir."
        assert not args.expected, "Option --expected shouldn't be used with --expected-dir"
        assert not args.actual, "Option --actual shouldn't be used with --expected-dir"

        file2result = process_directory_pair(args.actual_dir, args.expected_dir)
        total, tp = sum_results(file2result.values())
        report_overall_result(total, tp)
        if args.per_file_results:
            report_per_file_results(file2result, args.per_file_results)

    else:
        assert False, "Either --expected or --expected-dir is required."
