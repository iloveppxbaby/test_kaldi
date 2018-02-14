import argparse
import pandas as pd

def load_key(fn):
    key = pd.read_csv(fn, sep=' ', header=None, names=['mdl', 'seg'], dtype=str).set_index('seg')
    return key

def load_score(fn):
    score = pd.read_csv(fn, sep='|', dtype=str).set_index('Label')
    return score


def eval_topn_precision(key, score):
    key_seg_num = key.shape[0]
    score_seg_num = score.shape[0]
    print('mdl num: {0}'.format(score.shape[1])) 
    print('key_seg_num: {0}, score_seg_num: {1}'.format(key_seg_num, score_seg_num))
  
    key = key[key.mdl.isin(score.columns)]
    valid_score = score[score.index.isin(key.index)]
    valid_seg_num = valid_score.shape[0]
    correct_num_top1 = 0
    correct_num_top2 = 0
    correct_num_top3 = 0
    correct_num_top5 = 0

    output = valid_score.copy()
    output['result'] = None
    for seg in output.index:
        output.loc[seg, ['result']] = str(valid_score.loc[seg, :].astype(float).sort_values(ascending=False).index[0:5].tolist())
    output[['result']].to_csv('output_result', '\t')

    for seg in valid_score.index:
        if key.loc[seg, 'mdl'] in valid_score.loc[seg, :].astype(float).sort_values(ascending=False).index[0:1]:
            correct_num_top1 += 1
        if key.loc[seg, 'mdl'] in valid_score.loc[seg, :].astype(float).sort_values(ascending=False).index[0:2]:
            correct_num_top2 += 1
        if key.loc[seg, 'mdl'] in valid_score.loc[seg, :].astype(float).sort_values(ascending=False).index[0:3]:
            correct_num_top3 += 1
        if key.loc[seg, 'mdl'] in valid_score.loc[seg, :].astype(float).sort_values(ascending=False).index[0:5]:
            correct_num_top5 += 1
            
    
    precision_top1 = correct_num_top1/float(valid_seg_num)
    precision_top2 = correct_num_top2/float(valid_seg_num)
    precision_top3 = correct_num_top3/float(valid_seg_num)
    precision_top5 = correct_num_top5/float(valid_seg_num)
    
    print('valid_seg_num: {0}, top1: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top1, precision_top1))
    print('valid_seg_num: {0}, top2: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top2, precision_top2))
    print('valid_seg_num: {0}, top3: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top3, precision_top3))
    print('valid_seg_num: {0}, top5: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top5, precision_top5))

def eval_topn_precision_v2(key, score):
    key_seg_num = key.shape[0]
    score_seg_num = score.shape[0]

    key = key[key.mdl.isin(score.columns)]
    correct_num_top1 = 0
    correct_num_top2 = 0
    correct_num_top3 = 0
    correct_num_top5 = 0

    for mdl in score.columns:
        if score[mdl].astype(float).sort_values(ascending=False).index[0] in key[key['mdl'] == mdl].index:
            correct_num_top1 += 1
            correct_num_top2 += 1
            correct_num_top3 += 1
            correct_num_top5 += 1
        if score[mdl].astype(float).sort_values(ascending=False).index[1] in key[key['mdl'] == mdl].index:
            correct_num_top2 += 1
            correct_num_top3 += 1
            correct_num_top5 += 1    
        if score[mdl].astype(float).sort_values(ascending=False).index[2] in key[key['mdl'] == mdl].index:
            correct_num_top3 += 1
            correct_num_top5 += 1 
        if score[mdl].astype(float).sort_values(ascending=False).index[3] in key[key['mdl'] == mdl].index:
            correct_num_top5 += 1   
        if score[mdl].astype(float).sort_values(ascending=False).index[4] in key[key['mdl'] == mdl].index:
            correct_num_top5 += 1

    

    valid_seg_num = key.shape[0]

    precision_top1 = correct_num_top1/valid_seg_num
    precision_top2 = correct_num_top2/valid_seg_num
    precision_top3 = correct_num_top3/valid_seg_num
    precision_top5 = correct_num_top5/valid_seg_num

    print('valid_seg_num: {0}, top1: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top1, precision_top1))
    print('valid_seg_num: {0}, top2: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top2, precision_top2))
    print('valid_seg_num: {0}, top3: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top3, precision_top3))
    print('valid_seg_num: {0}, top5: correct_num: {1},  precison: {2:.3f}'.format(valid_seg_num, correct_num_top5, precision_top5))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('fn_key', help='format: mdl|seg')
    parser.add_argument('fn_score', help='format: matrix')
    args = parser.parse_args()
    

    key = load_key(args.fn_key)
    score = load_score(args.fn_score)
    eval_topn_precision(key, score)
    #eval_topn_precision_v2(key, score)
