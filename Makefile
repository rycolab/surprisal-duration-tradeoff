LANGUAGE := AZEBSA
DATASET := epitran
MODEL := lstm

DATA_DIR_BASE := ./data
DATA_DIR := $(DATA_DIR_BASE)/$(DATASET)
DATA_DIR_LANG := $(DATA_DIR)/$(LANGUAGE)
CHECKPOINT_DIR_BASE := ./checkpoint
CHECKPOINT_DIR := $(CHECKPOINT_DIR_BASE)/$(DATASET)
CHECKPOINT_DIR_LANG := $(CHECKPOINT_DIR)/$(LANGUAGE)
RESULTS_DIR_BASE := ./results
RESULTS_DIR := $(RESULTS_DIR_BASE)/$(DATASET)

VOX_DIR := $(DATA_DIR_BASE)/vox
VOX_RAW_FILE := $(VOX_DIR)/alignments/$(DATASET)/lab-files/$(LANGUAGE).zip
VOX_TEXT_FILE := $(VOX_DIR)/text/$(LANGUAGE)_transcript_nopunct.txt
VOX_LEX_FILE := $(VOX_DIR)/lexicons/$(DATASET)/$(LANGUAGE)_$(DATASET)_pronunciation.lex
VOX_PUNCT_FILE := $(VOX_DIR)/punct/$(DATASET)/$(LANGUAGE)
VOX_MCD_ZIP := $(VOX_DIR)/mcd.zip
VOX_MCD_PATH := $(VOX_DIR)/mcd
EXTRACTED_DIR := $(VOX_DIR)/extracted/$(DATASET)
VOX_EXTRACTED_FILE := $(EXTRACTED_DIR)/$(LANGUAGE).tsv
MCD_FILE := $(VOX_DIR)/mcd.tsv

PROCESSED_DATA_FILE := $(DATA_DIR)/$(LANGUAGE).pckl

CHECKPOINT_FILE := $(CHECKPOINT_DIR_LANG)/$(MODEL)/model.tch
LOSSES_FILE := $(CHECKPOINT_DIR_LANG)/$(MODEL)/losses.pckl

LOSSES_FULL_RAW := $(RESULTS_DIR)/$(MODEL)_losses-raw.tsv
LOSSES_FULL := $(RESULTS_DIR)/$(MODEL)_losses.tsv
LOSSES_LANGS := $(RESULTS_DIR)/$(MODEL)_langs.tsv
LOSSES_PHONES := $(RESULTS_DIR)/$(MODEL)_phones.tsv

MIXED_EFFECTS_MONOLING := $(RESULTS_DIR)/mixed_effects_monoling.tsv
MIXED_EFFECTS_MONOLING_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_monoling--drop_position.tsv
MIXED_EFFECTS_MONOLING_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_monoling--drop_phone.tsv
MIXED_EFFECTS_MONOLING_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_monoling--drop_both.tsv

MIXED_EFFECTS_MONOLING_LINEAR := $(RESULTS_DIR)/mixed_effects_monoling_linear.tsv
MIXED_EFFECTS_MONOLING_LINEAR_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_monoling_linear--drop_position.tsv
MIXED_EFFECTS_MONOLING_LINEAR_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_monoling_linear--drop_phone.tsv
MIXED_EFFECTS_MONOLING_LINEAR_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_monoling_linear--drop_both.tsv

MIXED_EFFECTS_CROSSLING := $(RESULTS_DIR)/mixed_effects_crossling.tsv
MIXED_EFFECTS_CROSSLING_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_crossling--drop_position.tsv
MIXED_EFFECTS_CROSSLING_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_crossling--drop_phone.tsv
MIXED_EFFECTS_CROSSLING_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_crossling--drop_both.tsv
MIXED_EFFECTS_CROSSLING_RE := $(RESULTS_DIR)/mixed_effects_crossling_re.tsv
MIXED_EFFECTS_CROSSLING_RE_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_crossling_re--drop_position.tsv
MIXED_EFFECTS_CROSSLING_RE_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_crossling_re--drop_phone.tsv
MIXED_EFFECTS_CROSSLING_RE_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_crossling_re--drop_both.tsv

MIXED_EFFECTS_CROSSLING_LINEAR := $(RESULTS_DIR)/mixed_effects_crossling_linear.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_crossling_linear--drop_position.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_crossling_linear--drop_phone.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_crossling_linear--drop_both.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_RE := $(RESULTS_DIR)/mixed_effects_crossling_linear_re.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_RE_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_crossling_linear_re--drop_position.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_RE_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_crossling_linear_re--drop_phone.tsv
MIXED_EFFECTS_CROSSLING_LINEAR_RE_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_crossling_linear_re--drop_both.tsv

MIXED_EFFECTS_TRADEOFF := $(RESULTS_DIR)/mixed_effects_tradeoff.tsv
MIXED_EFFECTS_TRADEOFF_DROP_POSITION := $(RESULTS_DIR)/mixed_effects_tradeoff--drop_position.tsv
MIXED_EFFECTS_TRADEOFF_DROP_PHONE := $(RESULTS_DIR)/mixed_effects_tradeoff--drop_phone.tsv
MIXED_EFFECTS_TRADEOFF_DROP_BOTH := $(RESULTS_DIR)/mixed_effects_tradeoff--drop_both.tsv

MIXED_EFFECTS_REPLICATION := $(RESULTS_DIR)/mixed_effects_replication.pckl

all: get_data train eval

analysis: $(LOSSES_FULL) analysis_monoling_full analysis_tradeoff analysis_crossling_full

plot_paper: plot_monoling_effects plot_crossling_effects plot_monoling_effects_linear plot_crossling_effects_linear \
	plot_monoling_full

plot_monoling_effects: $(MIXED_EFFECTS_MONOLING)
	mkdir -p $(RESULTS_DIR)/plots/
	python src/h06_paper/plot_monoling_slopes.py --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-effects-file $(MIXED_EFFECTS_MONOLING) --results-file $(LOSSES_FULL)

plot_monoling_effects_linear: $(MIXED_EFFECTS_MONOLING_LINEAR)
	mkdir -p $(RESULTS_DIR)/plots/
	python src/h06_paper/plot_monoling_slopes.py  --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-effects-file $(MIXED_EFFECTS_MONOLING_LINEAR) --analysis-type linear \
		 --results-file $(LOSSES_FULL)

plot_crossling_effects: $(MIXED_EFFECTS_CROSSLING)
	mkdir -p $(RESULTS_DIR)/plots/
	python src/h06_paper/plot_crossling_slopes.py --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-effects-file $(MIXED_EFFECTS_CROSSLING) --mixed-effects-file-re $(MIXED_EFFECTS_CROSSLING_RE)

plot_crossling_effects_linear: $(MIXED_EFFECTS_CROSSLING)
	mkdir -p $(RESULTS_DIR)/plots/
	python src/h06_paper/plot_crossling_slopes.py --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-effects-file $(MIXED_EFFECTS_CROSSLING_LINEAR) --mixed-effects-file-re $(MIXED_EFFECTS_CROSSLING_LINEAR_RE) \
		--analysis-type linear

plot_monoling_full: $(MIXED_EFFECTS_MONOLING)
	python src/h06_paper/plot_monoling_full.py --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-effects-file $(MIXED_EFFECTS_MONOLING)


print_controls: analysis_monoling analysis_tradeoff analysis_crossling
	python src/h06_paper/print_control_table.py --dataset $(DATASET) --data-path $(DATA_DIR_BASE) \
		--mixed-crossling-file $(MIXED_EFFECTS_CROSSLING) --mixed-tradeoff-file $(MIXED_EFFECTS_TRADEOFF) \
		--mixed-monoling-file $(MIXED_EFFECTS_MONOLING)



analysis_monoling_full: analysis_monoling analysis_monoling_linear

analysis_monoling:  \
	$(MIXED_EFFECTS_MONOLING) $(MIXED_EFFECTS_MONOLING_DROP_POSITION) \
	$(MIXED_EFFECTS_MONOLING_DROP_PHONE) $(MIXED_EFFECTS_MONOLING_DROP_BOTH)

analysis_monoling_linear: \
	$(MIXED_EFFECTS_MONOLING_LINEAR)

analysis_crossling_full: analysis_crossling analysis_crossling_linear

analysis_crossling: \
	$(MIXED_EFFECTS_CROSSLING) $(MIXED_EFFECTS_CROSSLING_DROP_POSITION) \
	$(MIXED_EFFECTS_CROSSLING_DROP_PHONE) $(MIXED_EFFECTS_CROSSLING_DROP_BOTH)

analysis_crossling_linear: \
	$(MIXED_EFFECTS_CROSSLING_LINEAR)

analysis_tradeoff: \
	$(MIXED_EFFECTS_TRADEOFF) $(MIXED_EFFECTS_TRADEOFF_DROP_POSITION) \
	$(MIXED_EFFECTS_TRADEOFF_DROP_PHONE) $(MIXED_EFFECTS_TRADEOFF_DROP_BOTH)

filter_mcd: $(LOSSES_FULL)

eval: $(LOSSES_FILE)

train: $(CHECKPOINT_FILE)

get_data: $(PROCESSED_DATA_FILE)

extract_vox: $(VOX_EXTRACTED_FILE)

clean:
	rm $(PROCESSED_DATA_FILE)


$(MIXED_EFFECTS_MONOLING): | $(LOSSES_FULL)
	Rscript src/h05_R/monoling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_MONOLING)

$(MIXED_EFFECTS_MONOLING_DROP_POSITION): | $(LOSSES_FULL)
	Rscript src/h05_R/monoling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_MONOLING_DROP_POSITION) --drop-position

$(MIXED_EFFECTS_MONOLING_DROP_PHONE): | $(LOSSES_FULL)
	Rscript src/h05_R/monoling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_MONOLING_DROP_PHONE) --drop-phone

$(MIXED_EFFECTS_MONOLING_DROP_BOTH): | $(LOSSES_FULL)
	Rscript src/h05_R/monoling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_MONOLING_DROP_BOTH) --drop-position --drop-phone

$(MIXED_EFFECTS_CROSSLING): | $(LOSSES_FULL)
	Rscript src/h05_R/crossling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_CROSSLING) $(MIXED_EFFECTS_CROSSLING_RE)

$(MIXED_EFFECTS_CROSSLING_DROP_POSITION): | $(LOSSES_FULL)
	Rscript src/h05_R/crossling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_CROSSLING_DROP_POSITION) $(MIXED_EFFECTS_CROSSLING_RE_DROP_POSITION)  --drop-position

$(MIXED_EFFECTS_CROSSLING_DROP_PHONE): | $(LOSSES_FULL)
	Rscript src/h05_R/crossling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_CROSSLING_DROP_PHONE) $(MIXED_EFFECTS_CROSSLING_RE_DROP_PHONE)  --drop-phone

$(MIXED_EFFECTS_CROSSLING_DROP_BOTH): | $(LOSSES_FULL)
	Rscript src/h05_R/crossling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_CROSSLING_DROP_BOTH) $(MIXED_EFFECTS_CROSSLING_RE_DROP_BOTH)  --drop-position --drop-phone

$(MIXED_EFFECTS_TRADEOFF): | $(LOSSES_FULL)
	Rscript src/h05_R/tradeoff_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_TRADEOFF)

$(MIXED_EFFECTS_TRADEOFF_DROP_POSITION): | $(LOSSES_FULL)
	Rscript src/h05_R/tradeoff_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_TRADEOFF_DROP_POSITION) --drop-position

$(MIXED_EFFECTS_TRADEOFF_DROP_PHONE): | $(LOSSES_FULL)
	Rscript src/h05_R/tradeoff_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_TRADEOFF_DROP_PHONE) --drop-phone

$(MIXED_EFFECTS_TRADEOFF_DROP_BOTH): | $(LOSSES_FULL)
	Rscript src/h05_R/tradeoff_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_TRADEOFF_DROP_BOTH) --drop-position --drop-phone


$(MIXED_EFFECTS_MONOLING_LINEAR): | $(LOSSES_FULL)
	Rscript src/h05_R/monoling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_MONOLING_LINEAR) --linear

$(MIXED_EFFECTS_CROSSLING_LINEAR): | $(LOSSES_FULL)
	Rscript src/h05_R/crossling_analysis.R $(LOSSES_FULL) \
		$(MIXED_EFFECTS_CROSSLING_LINEAR) $(MIXED_EFFECTS_CROSSLING_LINEAR_RE) \
		--linear


$(LOSSES_FULL): | $(MCD_FILE) $(LOSSES_FULL_RAW)
	python src/h04_analysis/filter_mcd.py --results-file-raw $(LOSSES_FULL_RAW) \
		--mcd-file $(MCD_FILE) --results-file $(LOSSES_FULL) --data-path $(EXTRACTED_DIR) \
		--dataset $(DATASET) --raw-data-path $(DATA_DIR_BASE)

$(LOSSES_FULL_RAW):
	mkdir -p $(RESULTS_DIR)/$(DATASET)
	python src/h04_analysis/merge_results.py \
		--data-path $(DATA_DIR_BASE)/$(DATASET) --checkpoints-path $(CHECKPOINT_DIR)/$(DATASET) \
		--results-file $(RESULTS_DIR)/$(DATASET)/$(MODEL)_losses-raw.tsv --model $(MODEL)

$(MCD_FILE): $(VOX_MCD_PATH)/
	python src/h04_analysis/merge_mcd.py --data-path $(VOX_DIR)/extracted/unitran \
		--results-file $(MCD_FILE) --mcd-path $(VOX_MCD_PATH)

# Eval language models
$(LOSSES_FILE): | $(CHECKPOINT_FILE)
	echo "Eval model" $(LOSSES_FILE)
	python src/h03_eval/eval.py --dataset $(DATASET) --data-file $(PROCESSED_DATA_FILE) --checkpoints-path $(CHECKPOINT_DIR_LANG) --model $(MODEL)

# Train Model
$(CHECKPOINT_FILE): | $(PROCESSED_DATA_FILE)
	echo "Train types model" $(CHECKPOINT_FILE)
	mkdir -p $(CHECKPOINT_DIR_LANG)/$(MODEL)
	python src/h02_learn/train.py --data-file $(PROCESSED_DATA_FILE) --checkpoints-path $(CHECKPOINT_DIR_LANG) --model $(MODEL)

# Preprocess Data
$(PROCESSED_DATA_FILE): | $(VOX_EXTRACTED_FILE)
	mkdir -p $(DATA_DIR)
	python src/h01_data/process_data.py --dataset $(DATASET) --src-file $(VOX_EXTRACTED_FILE) --tgt-file $(PROCESSED_DATA_FILE)

$(VOX_EXTRACTED_FILE): $(VOX_RAW_FILE) $(VOX_LEX_FILE)
	mkdir -p $(EXTRACTED_DIR)
	python src/h01_data/extract_vox.py --language $(LANGUAGE) --dataset $(DATASET) \
		--src-file $(VOX_RAW_FILE) --tgt-file $(VOX_EXTRACTED_FILE) \
		--text-file $(VOX_TEXT_FILE) --lex-file $(VOX_LEX_FILE) \
		--punct-file $(VOX_PUNCT_FILE)

$(VOX_PUNCT_FILE):
	unzip $(VOX_DIR)/punct/$(DATASET).zip -d $(VOX_DIR)/punct/

$(VOX_LEX_FILE):
	unzip $(VOX_DIR)/lexicons/$(DATASET).zip -d $(VOX_DIR)/lexicons/