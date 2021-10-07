# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import pandas as pd
from tqdm import tqdm

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from util import argparser
from util import constants


def get_args():
    argparser.add_argument("--src-file", type=str)
    argparser.add_argument("--text-file", type=str,)
    argparser.add_argument("--lex-file", type=str)
    argparser.add_argument("--punct-file", type=str)
    argparser.add_argument("--tgt-file", type=str)

    return argparser.parse_args()


def read_text(text_file, lang, dataset):
    files_txt = {}
    with open(text_file, 'r', encoding='utf-8') as f:
        for line in f:
            fname = line.strip().split()[0]

            # Get characters or words which should be ignored or used for splitting the data
            remove_chars = constants.REMOVE_CHARS.get(dataset, [])
            remove_chars += constants.REMOVE_CHARS_LANG \
                .get(dataset, {}).get(lang, [])
            split_chars = constants.SPLIT_CHARS.get(dataset, [])
            remove_words = constants.REMOVE_WORDS.get(dataset, [])
            remove_words += constants.REMOVE_WORDS_LANG \
                .get(dataset, {}).get(lang, [])

            # Remove chars
            for char in remove_chars:
                line = line.replace(char, '')

            # Split sentences
            parsed = line.strip().split()[1:]
            for char in split_chars:
                parsed = [y for x in parsed for y in x.strip().split(char) if y != '']

            # Remove full words
            parsed = [x for x in parsed if x not in remove_words]

            assert fname not in files_txt
            files_txt[fname] = parsed

    return files_txt


def read_lexicon(lex_file, dataset):
    lexicon = {}
    with open(lex_file, 'r') as f:
        for line in f:
            parsed = line.strip().split()

            if dataset != 'wikipron':
                assert (parsed[0] not in lexicon) or (parsed[0] == '<unk>')
            elif parsed[0] in lexicon:
                continue

            lexicon[parsed[0]] = parsed[1:]

    return lexicon


def iter_vox_phones(text, lexicon, dataset):
    for i, word in enumerate(text):
        lexicon_entry = word.lower() if dataset != 'unitran' else word

        if lexicon_entry not in lexicon or not lexicon[lexicon_entry]:
            yield -1, -1, '<oov>', word
            continue

        phones = lexicon[lexicon_entry]
        if i == 0 and phones[0] == '_t':
            phones = phones[1:]

        for j, phone in enumerate(phones):
            if j == 0:
                position = 'initial'
            elif j == len(phones) - 1:
                position = 'final'
            else:
                position = 'mid'
            yield i, position, phone, word


def expand_data(data, text, lexicon, dataset):
    text_iter = iter_vox_phones(text, lexicon, dataset)
    expanded_data = []
    for entry in data:
        phone = entry[2]
        if phone in constants.PAUSE_PHONES and phone != '<oov>':
            word_count, word_pos, word = [-1, -1, '']
        else:
            word_count, word_pos, lex_phone, word = next(text_iter)

            if phone != lex_phone:
                print(phone, lex_phone)
                print(' '.join(text))
                print(word)
                # import ipdb; ipdb.set_trace()

            assert phone == lex_phone
        expanded_data += [entry + [word_count, word_pos, word]]

    return expanded_data


def read_language(in_fname, lang, dataset, files_txt, lexicon):
    archive = zipfile.ZipFile(in_fname, 'r')
    dfs = []
    for file in tqdm(archive.namelist(), desc=f'Iterating lang {lang}'):
        if '.lab' in file:
            fname = file.split('/')[-1].split('.')[0]
            file_txt = files_txt[fname]

            fdata = archive.read(file).decode('utf-8')
            data = [x.split(' ') for x in fdata.split('\n')]
            expanded_data = expand_data(data[1:-1], file_txt, lexicon, dataset)

            assert data[0] == ['#'] or data[0] == ['end', 'sth', 'phone']
            assert data[-1] == ['']

            df = pd.DataFrame(expanded_data, columns=['end_time', 'sth', 'phone',
                                                      'word_idx', 'word_pos', 'word'])

            df['position'] = range(df.shape[0])
            df['file'] = file.split('/')[-1]
            df['lang'] = lang

            assert (df.loc[df.phone.isin(constants.PAUSE_PHONES), 'word_idx'] == -1).all()
            assert (df.loc[~df.phone.isin(constants.PAUSE_PHONES), 'word_idx'] != -1).all()

            dfs += [df]

    return pd.concat(dfs)


def extract_data(lang, dataset, src_file, tgt_file, text_file, lex_file):
    files_txt = read_text(text_file, lang, dataset)
    lexicon = read_lexicon(lex_file, dataset)
    df = read_language(src_file, lang, dataset, files_txt, lexicon)
    print('Lang: %s Sentences: %d' % (lang, df['file'].unique().shape[0]))
    df.to_csv(tgt_file, sep='\t')


def main():
    args = get_args()
    if args.dataset == 'unitran':
        constants.add_punct(args.punct_file)
    extract_data(args.language, args.dataset, args.src_file, args.tgt_file,
                 args.text_file, args.lex_file)


if __name__ == '__main__':
    main()
