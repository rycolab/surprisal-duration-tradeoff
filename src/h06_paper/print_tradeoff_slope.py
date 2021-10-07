import os
import sys
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

sys.path.append('./src/')
from h01_data.dataset.vox import VoxClamantis
from h02_learn.dataset import load_data, get_alphabet
from util import argparser
from util import util


def get_args():
    argparser.add_argument('--mixed-tradeoff-file', type=str, required=True)
    return argparser.parse_args()


def extract_fixed_effect(mdf, tgt_param, multiplicative=False):
    effect = mdf['coef'][tgt_param]
    if multiplicative:
        effect = 2**effect
    pvalue = mdf['pval'][tgt_param]
    if pvalue < 0.01:
        effect_str = '%.2f$^\\ddagger$' % (effect)
    elif pvalue < 0.05:
        effect_str = '%.2f$^\\dagger$' % (effect)
    else:
        effect_str = '%.2f' % (effect)

    return effect_str


def extract_df(mdf, multiplicative=False):
    uid_slope = extract_fixed_effect(mdf, 'loss', multiplicative=multiplicative)
    return uid_slope


def print_table(mdf_tradeoff):
    effect_tradeoff = extract_df(mdf_tradeoff)
    print('Slope:', effect_tradeoff)


def main():
    args = get_args()

    mdf_tradeoff = pd.read_csv(args.mixed_tradeoff_file, sep='\t')
    print_table(mdf_tradeoff)


if __name__ == '__main__':
    main()
