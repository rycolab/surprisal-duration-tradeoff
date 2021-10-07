#!/usr/bin/env Rscript
shhh <- suppressPackageStartupMessages # It's a library, so shhh!

shhh(library( mgcv ))
shhh(library(dplyr))
shhh(library(ggplot2))
shhh(library(lme4))
shhh(library( mgcv ))
theme_set(theme_bw())
shhh(library(tidymv))
shhh(library(gamlss))
shhh(library(gsubfn))
shhh(library(lmerTest))


load_data <- function(fname) {
    # Load data and handle slight pre-processing
    data <- read.csv(fname, header=T, sep='\t')
    data$duration <- data$duration * 1000
    data <- data %>% filter(position != -1) %>% droplevels()

    data$log_duration <- log(data$duration, base=2)
    return(data)
}


get_args <- function() {
    args <- commandArgs(trailingOnly = TRUE)
    fname <- args[1]
    outname <- args[2]
    drop_phone <- FALSE
    drop_position <- FALSE
    is_linear <- FALSE

    argsLen <- length(args)
    if (argsLen > 2) {
        if (args[3] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[3] == '--drop-position') {
            drop_position <- TRUE
        }
        if (args[3] == '--linear') {
            is_linear <- TRUE
        }
    }
    if (argsLen > 3) {
        if (args[4] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[4] == '--drop-position') {
            drop_position <- TRUE
        }
        if (args[4] == '--linear') {
            is_linear <- TRUE
        }
    }
    if (argsLen > 4) {
        if (args[5] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[5] == '--drop-position') {
            drop_position <- TRUE
        }
        if (args[5] == '--linear') {
            is_linear <- TRUE
        }
    }


    return(c(fname, outname, drop_phone, drop_position, is_linear))
}


filter_lang <- function(data, language) {
    # print(language)
    data_lang <- data %>% filter(lang == language) %>% droplevels()

    data_lang <- data_lang %>%
        mutate(
            position_initial = as.factor(position == "initial")
        )
    data_lang <- data_lang %>%
        mutate(
            position_final = as.factor(position == "final")
        )

    return(data_lang)
}


list[fname, outname, drop_phone, drop_position, is_linear] = get_args()
df <- load_data(fname)
languages <- unique(df$lang)

results = c()
columns = c()

if (is_linear == TRUE) {
    df$duration_analysis <- df$duration
} else {
    df$duration_analysis <- df$log_duration
}

# print(drop_position)
# print(drop_phone)

file_id = c(2, 4, 3)
for (lang in languages) {
# for (index in file_id) {
#     lang <- languages[index]
    print(lang)
    data_lang <- filter_lang(df, lang)

    if((drop_position == FALSE) & (drop_phone == FALSE)) {
        # print('Here')
        lm_mod <- lmer( duration_analysis ~ position_initial + position_final + loss * position_initial + (1|char),
                           data = data_lang)
        fixedef <- fixef(lm_mod)
        pvalues <- anova(lm_mod)[,6]
    } else if((drop_position == TRUE) & (drop_phone == FALSE)) {
        # print('Here1')
        lm_mod <- lmer( duration_analysis ~ + loss + (1|char),
                           data = data_lang)
        fixedef <- fixef(lm_mod)
        pvalues <- anova(lm_mod)[,6]
    } else if((drop_position == FALSE) & (drop_phone == TRUE)) {
        # print('Here2')
        lm_mod <- lm( duration_analysis ~ position_initial + position_final + loss * position_initial,
                           data = data_lang)
        fixedef <- coef(lm_mod)
        pvalues <- anova(lm_mod)[,5]
    } else if((drop_position == TRUE) & (drop_phone == TRUE)) {
        # print('Here3')
        lm_mod <- lm( duration_analysis ~ loss,
                           data = data_lang)
        fixedef <- coef(lm_mod)
        pvalues <- anova(lm_mod)[,5]
    }

    results <- cbind(results, lang=fixedef)
    # anova_results <- anova(lm_mod)
    lang_pval <- paste(lang, "--p_value", sep='')
    results <- cbind(results, lang_pval=pvalues)

    columns <- cbind(columns, lang)
    columns <- cbind(columns, lang_pval)
}

colnames(results) <- columns
write.table(results, outname, quote=FALSE, sep='\t')
