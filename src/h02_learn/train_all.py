import os
import sys
import subprocess

sys.path.append('./src/')
from h01_data.dataset import get_languages
from util import argparser


def get_args():
    return argparser.parse_args()


def main():
    args = get_args()
    languages = get_languages(args.dataset)
    my_env = os.environ.copy()

    for i, lang in enumerate(languages):
        print()
        print('(%03d/%03d) Training %s on dataset: %s. Language: %s.' % \
              (i + 1, len(languages), args.model, args.dataset, lang))
        cmd = ['make',
               'LANGUAGE=%s' % (lang),
               'DATASET=%s' % (args.dataset),
               'MODEL=%s' % (args.model),]
        print(cmd)
        subprocess.check_call(cmd, env=my_env)
        print()


if __name__ == '__main__':
    main()
