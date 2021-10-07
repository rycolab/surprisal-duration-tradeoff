import numpy as np
import torch
from torch.utils.data import DataLoader

from util import util
from util import constants
from .types import TypeDataset, FullDataset


def get_durations(batch):
    tensor = batch[0][1]
    batch_size = len(batch)
    max_length = max([len(entry[1]) for entry in batch])

    dur = tensor.new_ones(batch_size, max_length) * -1
    for i, item in enumerate(batch):
        durations = item[1]
        sent_len = len(durations)
        dur[i, :sent_len] = durations

    return dur


def get_objects(batch, index):
    # tensor = batch[0][1]
    batch_size = len(batch)
    max_length = max([len(entry[1]) for entry in batch])

    data = np.array([
        [None for _ in range(max_length)]
        for _ in range(batch_size)
    ])
    for i, item in enumerate(batch):
        items = item[index]
        sent_len = len(items)
        data[i, :sent_len] = items

    return data


def generate_batch(batch):
    r"""
    Since the text entries have different lengths, a custom function
    generate_batch() is used to generate data batches and offsets,
    which are compatible with EmbeddingBag. The function is passed
    to 'collate_fn' in torch.utils.data.DataLoader. The input to
    'collate_fn' is a list of tensors with the size of batch_size,
    and the 'collate_fn' function packs them into a mini-batch.[len(entry[0][0]) for entry in batch]
    Pay attention here and make sure that 'collate_fn' is declared
    as a top level def. This ensures that the function is available
    in each worker.
    """

    tensor = batch[0][0]
    batch_size = len(batch)
    max_length = max([len(entry[0]) for entry in batch]) - 1  # Does not need to predict SOS

    x = tensor.new_zeros(batch_size, max_length)
    y = tensor.new_zeros(batch_size, max_length)

    for i, item in enumerate(batch):
        sentence = item[0]
        sent_len = len(sentence) - 1  # Does not need to predict SOS
        x[i, :sent_len] = sentence[:-1]
        y[i, :sent_len] = sentence[1:]

    if len(batch[0]) == 1:
        return x.to(device=constants.device), y.to(device=constants.device)

    dur = get_durations(batch)
    pos = get_objects(batch, index=2)
    words = get_objects(batch, index=3)
    word_ids = get_objects(batch, index=4)
    phone_id = get_objects(batch, index=5)
    return x.to(device=constants.device), \
        (y.to(device=constants.device), dur.to(device=constants.device),
         pos, words, word_ids, phone_id)


def load_data(fname):
    return util.read_data(fname)


def get_alphabet(data):
    alphabet = data[1]
    return alphabet


def get_data(fname):
    data = load_data(fname)
    alphabet = get_alphabet(data)

    return data, alphabet


def get_dataset_cls(dataset_type):
    if dataset_type == 'type':
        dataset_cls = TypeDataset
    elif dataset_type == 'full':
        dataset_cls = FullDataset
    else:
        raise ValueError('Invalid dataset')
    return dataset_cls


def get_data_loader(fname, folds, dataset_cls, batch_size, shuffle):
    trainset = dataset_cls(fname, folds)
    trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=shuffle,
                             collate_fn=generate_batch)
    return trainloader


def get_data_loaders(fname, folds, batch_size, dataset_type='type'):
    data, alphabet = get_data(fname)
    dataset_cls = get_dataset_cls(dataset_type)

    trainloader = get_data_loader(
        data, folds[0], dataset_cls, batch_size=batch_size, shuffle=True)
    devloader = get_data_loader(
        data, folds[1], dataset_cls, batch_size=batch_size, shuffle=False)
    testloader = get_data_loader(
        data, folds[2], dataset_cls, batch_size=batch_size, shuffle=False)
    return trainloader, devloader, testloader, alphabet
