# coding=utf-8

import argparse


def load_lines(file_name):
    with open(file_name, mode='rt') as fp:
        return [x.rstrip() for x in fp.readlines()]


def load_dual_score_to_map(lines):
    score_map = {}
    for line in lines:
        fields = line.split(' ')
        mdl = fields[0]
        seg = fields[1]
        score = float(fields[2])
        if seg in score_map:
            if mdl not in score_map[seg]:
                score_map[seg][mdl] = score
            else:
                print("error: there is two same line")
                exit(-1)
        else:
            value_map = {mdl: score}
            score_map[seg] = value_map
    return score_map


def load_mat_score_to_map(lines):
    score_map = {}
    mdls = lines[0].split('|')[1:]
    for line in lines[1:]:
        fields = line.split('|')
        seg = fields[0]
        scores = fields[1:]
        local_score_map = {}
        for a, b in zip(mdls, scores):
            local_score_map[a] = float(b)
        score_map[seg] = local_score_map
    return score_map


def save_score_map_to_mat(score_map, mat_score_file, mdls=None, segs=None):
    if not segs:
        segs = score_map.keys()

    if not mdls:
        mdls = []
        for seg in segs:
            mdls.extend(score_map[seg].keys())
        mdls = set(mdls)

    with open(mat_score_file, mode='wt') as fp:
        line = 'Label|' + '|'.join(mdls)
        fp.writelines(line + '\n')

        for seg in segs:
            line = seg + '|'
            scores = []
            for mdl in mdls:
                if seg not in score_map.keys() or mdl not in score_map[seg].keys():
                    scores.append('-1000')
                else:
                    scores.append('{:.3f}'.format(score_map[seg][mdl]))
            fp.writelines(line + '|'.join(scores) + '\n')


def save_score_map_to_dual(score_map, dual_score_file):
    with open(dual_score_file, mode='wt') as fp:
        for seg in score_map:
            for mdl in score_map[seg]:
                fp.writelines(mdl + '|' + seg + '|' + str(score_map[seg][mdl]) + '\n')


def parse_arguments():
    desp = "usage: [-imat] input_score(default in dual) [-omat] output_score(default in dual)"
    parser = argparse.ArgumentParser(desp)
    parser.add_argument("--imat", action="store_true", help="input score in mat")
    parser.add_argument("input_score", help="input score")
    parser.add_argument("--omat", action="store_true", help="output score in mat")
    parser.add_argument("output_score", help="output score")
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_arguments()
    lines = load_lines(args.input_score)
    if args.imat:
        score_map = load_mat_score_to_map(lines)
    else:
        score_map = load_dual_score_to_map(lines)

    if args.omat:
        save_score_map_to_mat(score_map, args.output_score)
    else:
        save_score_map_to_dual(score_map, args.output_score)






