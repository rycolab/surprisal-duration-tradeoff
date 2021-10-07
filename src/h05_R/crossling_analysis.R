#!/usr/bin/env Rscript
shhh <- suppressPackageStartupMessages # It's a library, so shhh!

shhh(library( mgcv ))
shhh(library(dplyr))
shhh(library(ggplot2))
shhh(library(lme4))
shhh(library( mgcv ))
theme_set(theme_bw())
shhh(library(tidymv))
shhh(library(gsubfn))
shhh(library(tidyr))
shhh(library(lmerTest))


load_data <- function(fname) {
    # Load data and handle slight pre-processing
    data <- read.csv(fname, header=T, sep='\t')
    data$duration <- data$duration * 1000
    data <- data %>% filter(position != -1) %>% droplevels()

    data <- data %>%
        mutate(
            position_initial = as.factor(position == "initial")
        )
    data <- data %>%
        mutate(
            position_final = as.factor(position == "final")
        )
    data$log_duration <- log(data$duration, base=2)
    return(data)
}


get_args <- function() {
    args <- commandArgs(trailingOnly = TRUE)
    fname <- args[1]
    outname <- args[2]
    outname_re <- args[3]
    drop_phone <- FALSE
    drop_position <- FALSE
    is_linear <- FALSE

    argsLen <- length(args)
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
    if (argsLen > 5) {
        if (args[6] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[6] == '--drop-position') {
            drop_position <- TRUE
        }
        if (args[6] == '--linear') {
            is_linear <- TRUE
        }
    }


    return(c(fname, outname, outname_re, drop_phone, drop_position, is_linear))
}


list[fname, outname, outname_re, drop_phone, drop_position, is_linear] = get_args()
data_full <- load_data(fname)

if (is_linear == TRUE) {
    data_full$duration_analysis <- data_full$duration
} else {
    data_full$duration_analysis <- data_full$log_duration
}

results = c()


if((drop_position == FALSE) & (drop_phone == FALSE)) {
    lm_mod <- lmer( duration_analysis ~ position_initial + position_final + loss * position_initial +
                       (1+loss*position_initial|lang) + (1|lang/char),
                       data = data_full)
} else if((drop_position == TRUE) & (drop_phone == FALSE)) {
    lm_mod <- lmer( duration_analysis ~ loss +
                       (1+loss|lang) + (1|lang/char),
                       data = data_full)
} else if((drop_position == FALSE) & (drop_phone == TRUE)) {
    lm_mod <- lmer( duration_analysis ~ position_initial + position_final + loss * position_initial +
                       (1+loss*position_initial|lang),
                       data = data_full)
} else if((drop_position == TRUE) & (drop_phone == TRUE)) {
    lm_mod <- lmer( duration_analysis ~ loss +
                       (1+loss|lang),
                       data = data_full)
}

results <- cbind(results, coef=fixef(lm_mod))
results <- cbind(results, pval=anova(lm_mod)[,6])
write.table(results, outname, quote=FALSE, sep='\t')

random_effects <- coef(lm_mod)$lang
write.table(random_effects, outname_re, quote=FALSE, sep='\t')
