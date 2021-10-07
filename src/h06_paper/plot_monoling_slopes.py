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


def get_args():
    argparser.add_argument('--results-file', type=str, required=True)
    argparser.add_argument('--mixed-effects-file', type=str, required=True)
    argparser.add_argument('--drop-position', action='store_true', default=False)
    argparser.add_argument('--drop-phone', action='store_true', default=False)
    argparser.add_argument('--analysis-type', type=str, default='lognormal')
    return argparser.parse_args()


def plot(df, uid_slope, args, hue=None):
    fig, _ = plt.subplots(figsize=(aspect['width'] / 2.2, aspect['height']))
    df['x-axis'] = range(df.shape[0])
    df.sort_values(['family', 'x-axis'], inplace=True)
    ax1 = sns.scatterplot(x='x-axis', y='slope', data=df, hue='family', style='family')
    ax1.set(xticklabels=[])

    if args.analysis_type != 'linear':
        ax1.axhline(1, ls='--', c='C7')
        ax1.axhline(uid_slope, ls='--', c='C1')

        ax1.text(.5, uid_slope, "Average effect", c='C1', ha='left', va='bottom')
        ax1.text(df.shape[0] - 2, 1, "No effect line", c='C7', ha='right', va='bottom')
        if not args.drop_position:
            plt.ylim([0.995, 1.051])
            # plt.ylim([0.995, 1.046])
    else:
        ax1.axhline(0, ls='--', c='C7')
        ax1.axhline(uid_slope, ls='--', c='C1')

        ax1.text(.5, uid_slope, "Average effect", c='C1', ha='left', va='bottom')
        ax1.text(df.shape[0] - 2, 0, "No effect (zero line)", c='C7', ha='right', va='bottom')
        plt.ylim([-2.45, 4.5])

    if args.dataset != 'unitran':
        plt.legend(loc='upper left', ncol=2, frameon=False, handletextpad=0.05, borderpad=0, labelspacing=0.2)
    else:
        plt.legend('', frameon=False)
        # plt.legend()
    plt.ylabel('Trade-off Slope (millisecs / bit)')
    plt.xlabel('')

    extra_str = ''
    if args.drop_position and args.drop_phone:
        extra_str = '--drop_both'
    elif args.drop_position:
        extra_str = '--drop_position'
    elif args.drop_phone:
        extra_str = '--drop_phone'

    fname = 'results/plots/monoling-effects_%s_%s%s.pdf' % (args.dataset, args.analysis_type, extra_str)
    fig.savefig(fname, bbox_inches='tight')


def add_correction(df):
    df.sort_values('pvalue', inplace=True)
    df['temp_count'] = range(1, df.shape[0] + 1)
    df['threshold'] = 0.01 * df.temp_count / df.shape[0]
    df['significant'] = df.pvalue < df.threshold
    max_count = df[df.significant].temp_count.max()
    df.loc[df.temp_count <= max_count, 'significant'] = True

    return df


def plot_surprisal(mdf, args):
    df = mdf.transpose().reset_index()
    df['lang'] = df['index'].apply(lambda x: x.split('--')[0])
    df['is_pvalue'] = df['index'].apply(lambda x: 'pvalue' if 'p_value' in x else 'slope')
    df = df.pivot(index='lang', columns='is_pvalue', values='loss').reset_index()
    df.sort_values('slope', inplace=True, ascending=True)

    if args.analysis_type != 'linear':
        df['slope'] = df['slope'].apply(lambda x: 2**x)

    uid_slope = df.slope.mean()

    df_info = VoxClamantis.get_languages_info(args.data_path)
    df_info.set_index('bible.is / wilderness code', inplace=True)
    df = pd.merge(df, df_info, left_on='lang', right_on='bible.is / wilderness code')
    df = add_correction(df)

    print('Average effect:', df.slope.mean())
    print('Doculects:')
    print('Significantly positive %d, out of %d' % ((df.significant & df.slope > 0).sum(), df.shape[0]))
    print('Significantly negative %d, out of %d' % ((df.significant  & df.slope < 0).sum(), df.shape[0]))
    print()

    df_pvalue = df.groupby('ISO 639-3 code')[['significant']].agg('any')
    print('Languages:')
    print('\tSignificantly positive %d, out of %d' % (df_pvalue.significant.sum(), df_pvalue.shape[0]))

    df_pvalue = df.groupby('family')[['significant']].agg('any')
    print('Family:')
    print('\tSignificantly positive %d, out of %d' % (df_pvalue.significant.sum(), df_pvalue.shape[0]))
    print()

    df.sort_values('slope', inplace=True, ascending=True)
    plot(df, uid_slope, args)


def main():
    args = get_args()
    mdf = pd.read_csv(args.mixed_effects_file, sep='\t')
    plot_surprisal(mdf, args)


if __name__ == '__main__':
    main()
