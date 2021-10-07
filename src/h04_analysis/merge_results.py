import os
import sys
from tqdm import tqdm
import pandas as pd

sys.path.append('./src/')
from h02_learn.dataset import load_data, get_alphabet
from util import argparser
from util import util


def get_args():
    argparser.add_argument('--checkpoints-path', type=str, required=True)
    argparser.add_argument('--results-file', type=str, required=True)
    return argparser.parse_args()


def load_alphabet(data_path, lang):
    fname = os.path.join(data_path, '%s.pckl' % lang)
    data = load_data(fname)
    return get_alphabet(data)


def load_losses(fname):
    results = util.read_data(fname)

    losses = results['test']['losses'].cpu().numpy()
    y_values = results['test']['y_values'].cpu().numpy()
    durations = results['test']['durations'].cpu().numpy()
    durations[durations == -1] = 0
    word_pos = results['test']['words_pos']
    words = results['test']['words']
    word_ids = results['test']['word_ids']
    phone_ids = results['test']['phone_ids']

    return losses, y_values, durations, word_pos, words, word_ids, phone_ids


def get_results(checkpoints_path, data_path, model):
    # pylint: disable=too-many-locals

    languages = util.get_dirs(checkpoints_path)
    losses, phones, durations, y_values = {}, {}, {}, {}
    positions, words, word_ids, phone_ids = {}, {}, {}, {}

    for lang_path in tqdm(languages, desc='Reading data'):
        lang = lang_path.split('/')[-1]

        try:
            fname = os.path.join(lang_path, model, 'losses.pckl')
            loss, y_value, duration, word_pos, word, word_id, phone_id = load_losses(fname)
        except FileNotFoundError:
            tqdm.write('Warning: Skipping language %s' % lang)
            continue

        alphabet = load_alphabet(data_path, lang)
        phone = [alphabet.idx2word(y, drop_pad=True) for y in y_value]

        losses[lang] = loss
        y_values[lang] = y_value
        phones[lang] = phone
        durations[lang] = duration
        positions[lang] = word_pos
        words[lang] = word
        word_ids[lang] = word_id
        phone_ids[lang] = phone_id

    return (losses, phones, durations, y_values, positions, words, word_ids, phone_ids)


def main():
    # pylint: disable=too-many-locals

    args = get_args()
    losses, phones, durations, y_values, positions, words, word_ids, phone_ids = \
        get_results(args.checkpoints_path, args.data_path, args.model)

    results = []

    for (lang, loss), (lang2, dur), (lang3, y), (lang4, phone), \
            (lang5, position), (lang6, word), (lang7, word_id), (lang8, phone_id) in \
            tqdm(zip(losses.items(), durations.items(), y_values.items(),
                     phones.items(), positions.items(), words.items(),
                     word_ids.items(), phone_ids.items()), desc='Creating DataFrame'):
        assert lang == lang2
        assert lang == lang3
        assert lang == lang4
        assert lang == lang5
        assert lang == lang6
        assert lang == lang7
        assert lang == lang8

        # Remove eos loss
        loss[range(loss.shape[0]), (y != 0).sum(-1) - 1] = 0
        y[range(y.shape[0]), (y != 0).sum(-1) - 1] = 0

        loss_array = loss[y != 0]
        dur_array = dur[y[:, :-1] != 0]
        words_array = word[y[:, :-1] != 0]
        word_ids_array = word_id[y[:, :-1] != 0]
        phone_id_array = phone_id[y[:, :-1] != 0]
        positions_array = position[y[:, :-1] != 0]

        phone_array = [x for phon in phone for x in phon[:-1]]
        sentence_array = [i for i, phon in enumerate(phone) for _ in phon[:-1]]

        assert loss_array.shape == dur_array.shape
        assert loss_array.shape == words_array.shape
        assert loss_array.shape == word_ids_array.shape
        assert loss_array.shape == positions_array.shape
        assert loss_array.shape[0] == len(phone_array)

        results += [
            (lang, sentence, phone, loss, dur, position, word, word_id, phone_id)
            for loss, dur, phone, sentence, position, word, word_id, phone_id in
            zip(loss_array, dur_array, phone_array, sentence_array, positions_array,
                words_array, word_ids_array, phone_id_array)
        ]

    df = pd.DataFrame(results, columns=['lang', 'sentence', 'char', 'loss', 'duration',
                                        'position', 'word', 'word_id', 'phone_id'])
    df.to_csv(args.results_file, sep='\t', index=False)


if __name__ == '__main__':
    main()
