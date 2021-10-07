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
shhh(library(tidyr))


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
    return(data)
}


get_args <- function() {
    args <- commandArgs(trailingOnly = TRUE)
    fname <- args[1]
    outname <- args[2]
    drop_phone <- FALSE
    drop_position <- FALSE

    argsLen <- length(args)
    if (argsLen > 2) {
        if (args[3] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[3] == '--drop-position') {
            drop_position <- TRUE
        }
    }
    if (argsLen > 3) {
        if (args[4] == '--drop-phone') {
            drop_phone <- TRUE
        }
        if (args[4] == '--drop-position') {
            drop_position <- TRUE
        }
    }


    return(c(fname, outname, drop_phone, drop_position))
}


list[fname, outname, drop_phone, drop_position] = get_args()
df <- load_data(fname)

results = c()


if((drop_position == FALSE) & (drop_phone == FALSE)) {
    # print('Here')
    data_avg <- df %>%
        group_by(lang, char, position, position_initial, position_final) %>%
        summarise(loss = mean(loss), duration = mean(duration))
    lm_mod <- gamlss( duration ~ position_initial + position_final + loss * position_initial + re(random =~1|char, method="REML"),
                       data = data_avg)
} else if((drop_position == TRUE) & (drop_phone == FALSE)) {
    # print('Here1')
    data_avg <- df %>%
        group_by(lang, char) %>%
        summarise(loss = mean(loss), duration = mean(duration))
    lm_mod <- gamlss( duration ~ + loss + re(random =~1|char, method="REML"),
                       data = data_avg)
} else if((drop_position == FALSE) & (drop_phone == TRUE)) {
    # print('Here2')
    data_avg <- df %>%
        group_by(lang, position, position_initial, position_final) %>%
        summarise(loss = mean(loss), duration = mean(duration))
    lm_mod <- gamlss( duration ~ position_initial + position_final + loss * position_initial,
                       data = data_avg)
} else if((drop_position == TRUE) & (drop_phone == TRUE)) {
    # print('Here3')
    data_avg <- df %>%
        group_by(lang) %>%
        summarise(loss = mean(loss), duration = mean(duration))
    lm_mod <- gamlss( duration ~ loss,
                       data = data_avg)
}

results <- cbind(results, coef=lm_mod$mu.coefficients)
anova_results <- anova(lm_mod)
results <- cbind(results, pval=anova_results[,4])

write.table(results, outname, quote=FALSE, sep='\t')
