import os
import pandas as pd

from util import constants
from .base import BaseDataProcesser


class VoxClamantis(BaseDataProcesser):
    # pylint: disable=no-member

    @classmethod
    def get_data(cls, fname):
        df = pd.read_csv(fname, delimiter='\t')
        del df['Unnamed: 0']

        df['phone_id'] = range(df.shape[0])
        df = cls.get_file_id(df)
        df = cls.get_word_id(df)
        df = cls.get_durations(df)

        return df

    def process_data(self):
        df = pd.read_csv(self.fname, delimiter='\t')
        del df['Unnamed: 0']

        df['phone_id'] = range(df.shape[0])
        df = self.get_file_id(df)
        df = self.get_word_id(df)
        df = self.get_durations(df)
        df_file = self.group_sentences(df)

        word_info = {}
        for file_idx, row in df_file.iterrows():
            self.process_row(file_idx, row, word_info, check_times=True)

        return word_info

    @staticmethod
    def get_file_id(df):
        file_id = {x: i for i, x in enumerate(sorted(df.file.unique()))}
        df['file_id'] = df.file.apply(lambda x: file_id[x])
        return df

    @staticmethod
    def get_word_id(df):
        words = [tuple(x) for x in df[['file', 'word_idx']].drop_duplicates().to_numpy()]
        word_id = {x: i for i, x in enumerate(words)}
        df['word_id'] = df.apply(lambda x: word_id[(x['file'], x['word_idx'])], axis=1)
        return df

    @staticmethod
    def get_durations(df):
        df.sort_values(['file', 'position'], inplace=True)
        df['duration'] = df.end_time.diff()
        df.loc[df.position == 0, 'duration'] = df.loc[df.position == 0, 'end_time']
        assert not (df.duration < 0).any()

        return df

    @staticmethod
    def group_sentences(df):
        df_file = df.drop_duplicates(['file', 'lang'])
        df_file = df_file[['file', 'file_id', 'lang']].set_index('file')

        df_file['phones'] = df.groupby('file')['phone'].apply(list)
        df_file['end_times'] = df.groupby('file')['end_time'].apply(list)
        df_file['durations'] = df.groupby('file')['duration'].apply(list)
        df_file['positions'] = df.groupby('file')['position'].apply(list)
        df_file['word_ids'] = df.groupby('file')['word_id'].apply(list)
        df_file['phone_ids'] = df.groupby('file')['phone_id'].apply(list)

        df_file['word_pos'] = df.groupby('file')['word_pos'].apply(list)
        df_file['words'] = df.groupby('file')['word'].apply(list)

        return df_file

    @staticmethod
    def is_sorted(x):
        return all(x[i] <= x[i+1] for i in range(len(x)-1))

    @staticmethod
    def get_durations_from_seq(x):
        return [x[0]] + [x[i+1] - x[i] for i in range(len(x)-1)]

    def process_row(self, file_idx, row, word_info, check_times=False):
        tgt_sentence = tuple(row['phones'])
        tgt_word_ids = tuple(row['word_ids'])
        tgt_positions = tuple(row['positions'])
        tgt_phone_ids = tuple(row['phone_ids'])
        tgt_durations = tuple(row['durations'])
        if check_times:
            tgt_durations2 = tuple(self.get_durations_from_seq(row['end_times']))
            assert tgt_durations == tgt_durations2

        assert self.is_sorted(row['positions'])
        assert self.is_sorted(row['end_times'])
        assert len(row['phones']) == len(row['word_pos'])
        assert len(row['phones']) == len(row['words'])

        self.alphabet.add_word(tgt_sentence)

        word_info[file_idx] = {
            'idx': self.alphabet.word2idx(tgt_sentence),
            'word': tgt_sentence,
            'duration': tgt_durations,
            'word_pos': row['word_pos'],
            'words': row['words'],
            'file_id': row['file_id'],
            'word_id': tgt_word_ids,
            'position': tgt_positions,
            'phone_id': tgt_phone_ids,
        }

    @classmethod
    def get_languages(cls):
        return cls.languages

    @staticmethod
    def get_languages_info(fpath):
        fname = os.path.join(fpath, 'vox', 'languages.tsv')
        return pd.read_csv(fname, sep='\t')


class VoxUnitran(VoxClamantis):
    languages = constants.LANGUAGES_UNITRAN


class VoxEpitran(VoxClamantis):
    languages = constants.LANGUAGES_EPITRAN


class VoxWikipron(VoxClamantis):
    languages = constants.LANGUAGES_WIKIPRON
