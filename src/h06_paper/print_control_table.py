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

aspect = {
    'font_scale': 1,
    'ratio': 1.625 * 1.9,
    'width': 6.5 * 1.5,
}
aspect['height'] = aspect['width'] / aspect['ratio']


cmap = sns.color_palette("PRGn", 14)
sns.set(style="white", palette="muted", color_codes=True)
sns.set(style="white", palette="Set2", color_codes=True)
sns.set_context("notebook", font_scale=aspect['font_scale'])
mpl.rc('font', family='serif', serif='Times New Roman')
mpl.rc('figure', figsize=(aspect['width'], aspect['height']))
mpl.rc('text', usetex=True)
sns.set_style({'font.family': 'serif', 'font.serif': 'Times New Roman'})


PARAM_NAMES = {
    '.tsv': 'Phone + Position',
    '--drop_position.tsv': 'Phone',
    '--drop_phone.tsv': 'Position',
    '--drop_both.tsv': 'None',
}


def get_args():
    argparser.add_argument('--mixed-monoling-file', type=str, required=True)
    argparser.add_argument('--mixed-crossling-file', type=str, required=True)
    argparser.add_argument('--mixed-tradeoff-file', type=str, required=True)
    return argparser.parse_args()


def param_to_df(mdf, tgt_param):
    lang_slopes = [(lang, mdf['params'][tgt_param] + lang_effect[tgt_param]) for lang, lang_effect in mdf['random_effects'].items()]
    uid_slope = mdf['params'][tgt_param]

    return pd.DataFrame(lang_slopes, columns=['lang', 'slope']), uid_slope


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


def extract_df(mdfs, multiplicative=False):
    uid_slopes = {}
    for name, mdf in mdfs.items():
        uid_slope = extract_fixed_effect(mdf, 'loss', multiplicative=multiplicative)
        uid_slopes[PARAM_NAMES[name]] = uid_slope

    return uid_slopes


def add_correction(df, column):
    df.sort_values(column, inplace=True)
    df['temp_count'] = range(1, df.shape[0] + 1)
    df['threshold'] = 0.01 * df.temp_count / df.shape[0]
    df['significant'] = df[column] < df.threshold
    max_count = df[df.significant].temp_count.max()
    df.loc[df.temp_count <= max_count, 'significant'] = True

    return df


def extract_df_monoling(mdfs):
    LM_MODELS = {'--drop_phone.tsv', '--drop_both.tsv'}

    uid_slopes, uid_significant = {}, {}
    for name, df in mdfs.items():
        if name in LM_MODELS:
            for column in df.columns:
                if 'p_value' in column:
                    df[column] = df[column].shift(1)

        df = df.transpose()
        df_params = df[df.index.map(lambda x: 'p_value' not in x)]
        df_pvalues = df[df.index.map(lambda x: 'p_value' in x)].copy()
        df_pvalues = add_correction(df_pvalues, 'loss')

        uid_slopes[PARAM_NAMES[name]] = 2**df_params['loss'].mean()
        uid_significant[PARAM_NAMES[name]] = (df_pvalues['significant']).sum()

    return uid_slopes, uid_significant


def print_table(mdfs_monoling, mdfs_crossling, mdfs_tradeoff, args):
    effect_monoling, significant_uid = extract_df_monoling(mdfs_monoling)
    effect_crossling = extract_df(mdfs_crossling, multiplicative=True)
    effect_tradeoff = extract_df(mdfs_tradeoff)

    str_base = '%s & %s & %.2f & %d & %s & %s \\\\'

    for param in effect_crossling.keys():
        if 'Phone' in param:
            drop_phone = '\\cmark'
        else:
            drop_phone = '\\xmark'

        if 'Position' in param:
            drop_position = '\\cmark'
        else:
            drop_position = '\\xmark'

        print(str_base % (drop_phone, drop_position, effect_monoling[param], significant_uid[param], effect_crossling[param], effect_tradeoff[param]))


def main():
    args = get_args()

    mdfs_monoling, mdfs_crossling, mdfs_tradeoff = {}, {}, {}
    for suffix in ['.tsv', '--drop_position.tsv', '--drop_phone.tsv', '--drop_both.tsv']:
        fname = args.mixed_monoling_file.replace('.tsv', suffix)
        mdfs_monoling[suffix] = pd.read_csv(fname, sep='\t')
        fname = args.mixed_crossling_file.replace('.tsv', suffix)
        mdfs_crossling[suffix] = pd.read_csv(fname, sep='\t')
        fname = args.mixed_tradeoff_file.replace('.tsv', suffix)
        mdfs_tradeoff[suffix] = pd.read_csv(fname, sep='\t')

    print_table(mdfs_monoling, mdfs_crossling, mdfs_tradeoff, args)


if __name__ == '__main__':
    main()
