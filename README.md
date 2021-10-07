# surprisal-duration-tradeoff

[![CircleCI](https://circleci.com/gh/rycolab/surprisal-duration-tradeoff.svg?style=svg&circle-token=581c6fb829d8c4874c9a5a65c7dbc9da7ab3ac82)](https://circleci.com/gh/rycolab/surprisal-duration-tradeoff)


This code accompanies the paper [A surprisal--duration trade-off across and within the world's languages (Pimentel et al., EMNLP 2021)](https://arxiv.org/abs/2109.15000).
It is a study of the trade-off between surprisal and duration resulting from a hypothetical channel capacity in human's language processing capacity.


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

VoxClamantis information can be found at https://voxclamantisproject.github.io. First, download the alignment data for both epitran and unitran in the [OSF repository](https://osf.io/ap4hn/?view_only=ff23dd6bf3324b11b834ea4bd8d7e6c9) and place it in folder `data/vox/alignments/`. Second, download the raw text information from [this drive url](https://drive.google.com/file/d/1hi2ky1c673k7iQLKnwF6Queu5r_YcQSG/view?usp=sharing) and place it in path `data/vox/text/`.
You can now extract the VoxClamantis data with the command:
```bash
$ make extract_vox LANGUAGE=<language> DATASET=<dataset>
```
or directly preprocess it with command:
```bash
$ make get_data LANGUAGE=<language> DATASET=<dataset>
```
with any language in VoxClamantis, e.g. `AZEBSA`.
There are three alignment methods available in VoxClamantis, called `<dataset>`, we use two of them in this project: unitran, and epitran.

To preprocess all languages in one of the analysed datasets run:
```bash
$ source src/h01_data/process_epitran.sh
$ source src/h01_data/process_unitran.sh
```


## Train and evaluate the models

You can train your models on each language with the command
```bash
$ make train LANGUAGE=<language> DATASET=<dataset>
```
Similarly, you can then use your model to get surprisal values on that language by running:
```bash
$ make eval LANGUAGE=<language> DATASET=<dataset>
```
To train the model in all languages from one of the datasets, run
```bash
$ python src/h02_learn/train_all.py --dataset <dataset>
```

## Analysis

After training and evaluating the models in all languages with the commands above. Merge the results and filter them based on MCD scores:
```bash
$ make filter_mcd DATASET=<dataset>
```
With this filtered results, we are now able to run the paper analysis. First, run the individual languages analysis:
```bash
$ make analysis_monoling DATASET=<dataset>
```
Second, the full cross-linguistic analysis:
```bash
$ make analysis_crossling DATASET=<dataset>
```
Finally, run the "pure" cross-linguistic analysis with command:
```bash
$ make analysis_tradeoff DATASET=<dataset>
```

## Paper plots and results

Finally, to get the plots as in the paper run the following commands. For figure 1:
```bash
$ make plot_monoling_full DATASET=unitran
```
For figure 2:
```bash
$ make plot_monoling_effects DATASET=epitran
```
For figure 3:
```bash
$ make plot_crossling_effects DATASET=epitran
```
For the Appendix Table:
```bash
$ make print_controls DATASET=epitran
```

Further, to get the average unitran slope for the individual language analysis run:
```bash
$ make plot_monoling_effects DATASET=unitran
```
And for the cross-linguistic analysis:
```bash
$ make plot_crossling_effects DATASET=unitran
```
This result might not match the paper exactly since the original models were deleted and we had to rerun this cross-linguistic unitran analysis.
Finally, to get the pure cross-linguistic slopes run:
```bash
$ make print_tradeoff DATASET=unitran
```



## Extra Information


#### Citation

If this code or the paper were usefull to you, consider citing it:

```bash
@inproceedings{pimentel-etal-2021-surprisal,
    title = "A surprisal--duration trade-off across and within the world's languages",
    author = "Pimentel, Tiago and
    Meister, Clara and
    Salesky, Elizabeth and
    Teufel, Simone and
    Blasi, Damián and
    Cotterell, Ryan",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year = "2021",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/2109.15000",
}
```


#### Contact

To ask questions or report problems, please open an [issue](https://github.com/rycolab/surprisal-duration-tradeoff/issues).
