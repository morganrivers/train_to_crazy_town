
library(tidyverse)
library(rmarkdown)
library(here)
library(quarto)

# SET UP FOR CREATION OF HTML AND PDF FILES
setwd(paste0(here(),"/2_code"))
list.files(pattern = "qmd", full.names = FALSE) %>%
walk(quarto_render)


