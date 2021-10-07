from abc import ABC, abstractmethod
import numpy as np

from util import util


class BaseDataProcesser(ABC):
    def __init__(self, fname, alphabet):
        self.fname = fname
        self.alphabet = alphabet

    @abstractmethod
    def process_data(self):
        pass

    @staticmethod
    def get_fold_splits(data, n_folds):
        keys = sorted(list(data.keys()))
        np.random.shuffle(keys)
        splits = np.array_split(keys, n_folds)
        splits = [{key: data[key] for key in fold} for fold in splits]
        return splits

    def write_data(self, tgt_fname, splits):
        data = [list(split.values()) for split in splits]
        util.write_data(tgt_fname, (data, self.alphabet))
