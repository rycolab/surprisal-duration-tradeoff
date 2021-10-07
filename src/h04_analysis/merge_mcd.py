import os
import sys
import math
from tqdm import tqdm
import numpy as np
import pandas as pd
from scipy import stats

sys.path.append('./src/')
from h01_data.dataset.vox import VoxClamantis
from h02_learn.dataset import load_data, get_alphabet
from util import argparser
from util import util


def get_args():
    argparser.add_argument('--mcd-path', type=str, required=True)
    argparser.add_argument('--results-file', type=str, required=True)
    return argparser.parse_args()


def get_results(mcd_path, raw_data_path):
    languages = util.get_filenames(mcd_path)
    dfs = []

    for lang_path in tqdm(languages, desc='Reading data'):
        lang = lang_path.split('/')[-1].split('.')[0]
        tqdm.write(lang)

        df = pd.read_csv(lang_path, sep=' ', header=None)
        df.columns = ['file', 'mcd']
        df['lang'] = lang
        assert df.shape[1] == 3
        assert df.file.unique().shape[0] == df.shape[0]

        dfs += [df]

    return pd.concat(dfs, axis=0)


def main():
    args = get_args()
    df = get_results(args.mcd_path, args.data_path)
    df.to_csv(args.results_file, sep='\t', index=False)


if __name__ == '__main__':
    main()
