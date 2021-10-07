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


cmap = sns.color_palette("Set2", 14)
sns.set(style="white", palette="Set2", color_codes=True)
sns.set_context("notebook", font_scale=aspect['font_scale'])
mpl.rc('font', family='serif', serif='Times New Roman')
mpl.rc('figure', figsize=(aspect['width'], aspect['height']))
mpl.rc('text', usetex=True)
sns.set_style({'font.family': 'serif', 'font.serif': 'Times New Roman'})


def get_args():
    argparser.add_argument('--mixed-effects-file', type=str, required=True)
    argparser.add_argument('--drop-position', action='store_true', default=False)
    argparser.add_argument('--drop-phone', action='store_true', default=False)
    argparser.add_argument('--analysis-type', type=str, default='lognormal')
    return argparser.parse_args()


def plot(df, uid_slope, args, hue=None):
    fig, _ = plt.subplots(figsize=(aspect['width'] / 2.2, aspect['height']))

    ax1 = sns.scatterplot(x='lang', y='slope', data=df, hue='family', style='dataset', markers=['o', 'P'], size='size', linewidth=0, alpha=.9, cmap="mako")
    ax1.set(xticklabels=[])

    if args.analysis_type != 'linear':
        ax1.axhline(1, ls='--', c='C7')
        ax1.axhline(uid_slope, ls='--', c='C1')

        ax1.text(.5, uid_slope, "Average effect", c='C1', ha='left', va='bottom')
        ax1.text(df.shape[0] - 10, 1, "No effect (zero line)", c='C7', ha='right', va='bottom')
        if not args.drop_position:
            plt.ylim([0.995, 1.046])
    else:
        ax1.axhline(0, ls='--', c='C7')
        ax1.axhline(uid_slope, ls='--', c='C1')

        ax1.text(.5, uid_slope, "Average effect", c='C1', ha='left', va='bottom')
        ax1.text(df.shape[0] - 2, 0, "No effect (zero line)", c='C7', ha='right', va='bottom')
        plt.ylim([-2.45, 5.1])

    plt.legend('', frameon=False)
    plt.ylabel('Trade-off Slope (millisecs / bit)')
    plt.xlabel('')

    extra_str = ''
    if args.drop_position and args.drop_phone:
        extra_str = '--drop_both'
    elif args.drop_position:
        extra_str = '--drop_position'
    elif args.drop_phone:
        extra_str = '--drop_phone'

    fname = 'results/plots/monoling-effects_full_%s%s.pdf' % (args.analysis_type, extra_str)
    fig.savefig(fname, bbox_inches='tight')


def clean_data(mdf, args):
    df = mdf.transpose().reset_index()
    df['lang'] = df['index'].apply(lambda x: x.split('--')[0])
    df['is_pvalue'] = df['index'].apply(lambda x: 'pvalue' if 'p_value' in x else 'slope')
    df = df.pivot(index='lang', columns='is_pvalue', values='loss').reset_index()
    df.sort_values('slope', inplace=True, ascending=True)

    if args.analysis_type != 'linear':
        df['slope'] = df['slope'].apply(lambda x: 2**x)

    return df


def plot_surprisal(mdf1, mdf2, args):
    df1 = clean_data(mdf1, args)
    df1['dataset'] = 'unitran'
    df1['size'] = .01
    langs = set(df1.lang.unique())
    df2 = clean_data(mdf2, args)
    df2['dataset'] = 'epitran'
    df2['size'] = 2
    df2 = df2[df2.lang.isin(langs)]
    df = pd.concat([df1, df2], axis=0)

    # uid_slope1 = df1.slope.mean()

    df_info = VoxClamantis.get_languages_info(args.data_path)
    df_info.set_index('bible.is / wilderness code', inplace=True)
    df = pd.merge(df, df_info, left_on='lang', right_on='bible.is / wilderness code')
    # import ipdb; ipdb.set_trace()
    print(df1.slope.mean(), df2.slope.mean())

    plot(df, df.slope.mean(), args)


def main():
    args = get_args()
    mdf1 = pd.read_csv('./results/unitran/mixed_effects_monoling.tsv', sep='\t')
    mdf2 = pd.read_csv('./results/epitran/mixed_effects_monoling.tsv', sep='\t')
    plot_surprisal(mdf1, mdf2, args)


if __name__ == '__main__':
    main()
