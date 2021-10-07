import os
import sys
from tqdm import tqdm
import numpy as np
import torch

sys.path.append('./src/')
from h02_learn.dataset import get_data_loaders
from h02_learn.model import get_model_cls
from util import argparser
from util import util
from util import constants


def get_args():
    # Data
    argparser.add_argument('--batch-size', type=int, default=512)
    # Models
    argparser.add_argument('--checkpoints-path', type=str, required=True)

    args = argparser.parse_args()
    args.model_path = os.path.join(args.checkpoints_path, args.model)
    return args


def load_model(fpath, model_name):
    model_cls = get_model_cls(model_name)
    return model_cls.load(fpath).to(device=constants.device)


def merge_tensors(losses, fill=0):
    max_len = max(x.shape[-1] for x in losses)
    n_sentences = sum(x.shape[0] for x in losses)

    full_loss = torch.ones(n_sentences, max_len) * fill

    start, end = 0, 0
    for loss in losses:
        end += loss.shape[0]
        batch_len = loss.shape[-1]
        full_loss[start:end, :batch_len] = loss
        start = end

    return full_loss


def merge_numpy(data, fill=None):
    max_len = max(x.shape[-1] for x in data)
    n_sentences = sum(x.shape[0] for x in data)

    full_data = np.array([
        [fill for _ in range(max_len)]
        for _ in range(n_sentences)
    ])

    start, end = 0, 0
    for item in data:
        end += item.shape[0]
        batch_len = item.shape[-1]
        full_data[start:end, :batch_len] = item
        start = end

    return full_data


def eval_per_char(dataloader, model, pad_idx):
    # pylint: disable=too-many-locals
    model.eval()

    y_values, losses, lengths, durations, words_pos, words, word_ids, phone_ids = \
        [], [], [], [], [], [], [], []
    dev_loss, n_instances = 0, 0
    for x, (y, dur, position, word, word_id,
            phone_id) in tqdm(dataloader, desc='Evaluating per char'):
        y_hat = model(x)
        loss = model.get_loss_full(y_hat, y)

        sent_lengths = (y != pad_idx).sum(-1)
        batch_size = y.shape[0]
        dev_loss += (loss.sum(-1) / sent_lengths).sum()
        n_instances += batch_size
        losses += [loss.cpu()]
        y_values += [y.cpu()]
        durations += [dur.cpu()]
        words_pos += [position]
        words += [word]
        word_ids += [word_id]
        phone_ids += [phone_id]
        lengths += [sent_lengths.cpu()]

    losses = merge_tensors(losses)
    y_values = merge_tensors(y_values, fill=pad_idx)
    durations = merge_tensors(durations, fill=-1)
    words_pos = merge_numpy(words_pos)
    words = merge_numpy(words)
    word_ids = merge_numpy(word_ids)
    phone_ids = merge_numpy(phone_ids)
    lengths = torch.cat(lengths, dim=0)

    results = {
        'losses': losses,
        'y_values': y_values,
        'durations': durations,
        'words_pos': words_pos,
        'words': words,
        'word_ids': word_ids,
        'phone_ids': phone_ids,
        'lengths': lengths,
        'pad_idx': pad_idx,
    }

    return results, (dev_loss / n_instances).item()


def eval_all(model_path, dataloader, model_name):
    # pylint: disable=too-many-locals
    trainloader, devloader, testloader, alphabet = dataloader
    pad_idx = alphabet.char2idx('PAD')

    model = load_model(model_path, model_name)

    train_res, train_loss = eval_per_char(trainloader, model, pad_idx)
    dev_res, dev_loss = eval_per_char(devloader, model, pad_idx)
    test_res, test_loss = eval_per_char(testloader, model, pad_idx)

    print('Training loss: %.4f Dev loss: %.4f Test loss: %.4f' %
          (train_loss, dev_loss, test_loss))

    results = {
        'name': model_name,
        'train': train_res,
        'dev': dev_res,
        'test': test_res,
    }

    return results


def main():
    args = get_args()
    folds = [list(range(8)), [8], [9]]

    dataloader = get_data_loaders(
        args.data_file, folds, args.batch_size, dataset_type='full')

    with torch.no_grad():
        results = eval_all(args.model_path, dataloader, args.model)

    results_file = '%s/losses.pckl' % (args.model_path)
    util.write_data(results_file, results)


if __name__ == '__main__':
    main()
