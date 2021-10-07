import os
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append('./src/')
from h01_data.dataset.vox import VoxClamantis
from util import argparser


MCD_MAXIMUM = 6.5

def get_args():
    argparser.add_argument('--results-file-raw', type=str, required=True)
    argparser.add_argument('--results-file', type=str, required=True)
    argparser.add_argument('--mcd-file', type=str, required=True)
    argparser.add_argument('--raw-data-path', type=str, required=True)
    return argparser.parse_args()


def add_language_families(df, data_path):
    df_info = VoxClamantis.get_languages_info(data_path)
    df_info.set_index('bible.is / wilderness code', inplace=True)
    df_info = df_info[['family']]
    df = pd.merge(df, df_info, left_on='lang', right_on='bible.is / wilderness code')

    return df


def main():
    args = get_args()


    df = pd.read_csv(args.results_file_raw, delimiter='\t')
    df = add_language_families(df, args.raw_data_path)
    if args.dataset == 'epitran':
        df['ratio'] = 1
        df['mcd'] = None
        df.to_csv(args.results_file, sep='\t', index=False)
        return

    dfs_filtered = []
    df_mcd = pd.read_csv(args.mcd_file, delimiter='\t')

    for lang in tqdm(df.lang.unique(), desc='Filtering languages'):
        df_mcd_lang = df_mcd[df_mcd.lang == lang]
        df_lang = df[df.lang == lang].copy()
        df_lang['mcd'] = df_mcd_lang.mcd.mean()

        assert df_mcd_lang.file.unique().shape[0] == df_mcd_lang.shape[0]

        files = set(df_mcd_lang[df_mcd_lang.mcd < MCD_MAXIMUM].file)
        if len(files) == df_mcd_lang.shape[0]:
            df_lang['ratio'] = 1
            dfs_filtered += [df_lang]
            continue

        fname = os.path.join(args.data_path, '%s.tsv' % lang)
        df_data = VoxClamantis.get_data(fname)
        df_data['file'] = df_data['file'].apply(lambda x: x.replace('.lab', ''))
        phone_ids = set(df_data[df_data.file.isin(files)].phone_id)

        df_lang = df_lang[df_lang.phone_id.isin(phone_ids)]
        df_lang['ratio'] = df_lang.shape[0] / df[df.lang == lang].shape[0]

        ratio = df_lang.shape[0] / df[df.lang == lang].shape[0]
        tqdm.write('Language: %s. Ratio: %.2f. MCD: %.2f' % (lang, ratio, df_mcd_lang.mcd.mean()))

        dfs_filtered += [df_lang]

    df_filtered = pd.concat(dfs_filtered)
    df_filtered.to_csv(args.results_file, sep='\t', index=False)


if __name__ == '__main__':
    main()
