# surprisal-duration-tradeoff
This repository accompanies the paper "A surprisal--duration trade-off across and within the world's languages" published in EMNLP 2021.

## Install

To install dependencies run:
```bash
$ conda env create -f environment.yml
```

Activate the created conda environment with command:
```bash
$ source activate.sh
```

Finally, install the appropriate version of pytorch:
```bash
$ conda install -y pytorch torchvision cudatoolkit=10.1 -c pytorch
$ # conda install pytorch torchvision cpuonly -c pytorch
$ pip install transformers
```

For the R analysis, you will need to install
```bash
$ sudo apt-get install libnlopt-dev
```

## Get Data

#### VoxClamantis

VoxClamantis data can be obtained at https://voxclamantisproject.github.io.
You can process it with the command:
```bash
$ make LANGUAGE=<language> DATASET=<dataset>
```
with any language in VoxClamantis, e.g. `por`.
There are three alignment methods available in VoxClamantis, called <dataset> here: unitran, epitran, and wikipron.


## Train and evaluate the models

You can train your models using random search with the command
```bash
$ make LANGUAGE=<language> DATASET=<dataset>
```
There are three datasets available in this repository: celex; northeuralex; and wiki.


To train the model in all languages from one of the datasets, run
```bash
$ python src/h02_learn/train_all.py --dataset <dataset> --data-path data/<dataset>/
```



## Extra Information

#### Contact

To ask questions or report problems, please open an [issue](https://github.com/rycolab/surprisal-duration-tradeoff/issues).
