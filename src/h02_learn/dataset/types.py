import torch
import numpy as np

from torch.utils.data import Dataset


class TypeDataset(Dataset):
    def __init__(self, data, folds):
        self.data = data
        self.folds = folds
        self.process_train(data)

    def process_train(self, data):
        folds_data = data[0]
        self.alphabet = data[1]

        folds_words = [
            instance['word']
            for fold in self.folds for instance in folds_data[fold]
        ]

        self.words = [torch.LongTensor(self.get_word_idx(word)) for word in folds_words]
        self.n_instances = len(self.words)

    def get_word_idx(self, word):
        return [self.alphabet.char2idx('SOS')] + \
            self.alphabet.word2idx(word) + \
            [self.alphabet.char2idx('EOS')]

    def __len__(self):
        return self.n_instances

    def __getitem__(self, index):
        return (self.words[index],)


class FullDataset(TypeDataset):

    def process_train(self, data):
        super().process_train(data)
        folds_data = data[0]

        folds_duration = [
            instance['duration']
            for fold in self.folds for instance in folds_data[fold]
        ]
        folds_positions = [
            instance['word_pos']
            for fold in self.folds for instance in folds_data[fold]
        ]
        folds_words = [
            instance['words']
            for fold in self.folds for instance in folds_data[fold]
        ]
        folds_word_ids = [
            instance['word_id']
            for fold in self.folds for instance in folds_data[fold]
        ]
        folds_phone_ids = [
            instance['phone_id']
            for fold in self.folds for instance in folds_data[fold]
        ]

        self.durations = [torch.FloatTensor(item) for item in folds_duration]
        self.word_pos = [np.array(item) for item in folds_positions]
        self.word_forms = [np.array(item) for item in folds_words]
        self.word_ids = [np.array(item) for item in folds_word_ids]
        self.phone_ids = [np.array(item) for item in folds_phone_ids]

    def __getitem__(self, index):
        return (self.words[index], self.durations[index], self.word_pos[index], \
                self.word_forms[index], self.word_ids[index], self.phone_ids[index])
