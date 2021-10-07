import sys
import logging

sys.path.append('./src/')
from h01_data.alphabet import Alphabet
from h01_data.dataset import get_dataset_cls
from util import argparser


def get_args():
    argparser.add_argument("--src-file", type=str,)
    argparser.add_argument("--tgt-file", type=str,)
    argparser.add_argument("--n-folds", type=int, default=10,)

    return argparser.parse_args()


def get_dataset(dataset_name, src_fname, alphabet):
    dataset_cls = get_dataset_cls(dataset_name)
    return dataset_cls(src_fname, alphabet)


def process(src_fname, dataset, tgt_file, n_folds):
    alphabet = Alphabet()

    dataset = get_dataset(dataset, src_fname, alphabet)
    words_info = dataset.process_data()
    splits = dataset.get_fold_splits(words_info, n_folds)

    dataset.write_data(tgt_file, splits)

    print('# unique chars:', len(alphabet))


def main():
    args = get_args()
    logging.info(args)

    process(args.src_file, args.dataset, args.tgt_file, args.n_folds)


if __name__ == '__main__':
    main()
