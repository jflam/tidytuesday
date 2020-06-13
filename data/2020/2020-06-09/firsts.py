# I like this plot in R
# https://github.com/ml4-scf/tidytuesday

import pandas as pd
import numpy as np
from plotnine import *

DATA_DIR = "."

firsts = pd.read_csv(f"{DATA_DIR}/firsts.csv")

data = (firsts.assign(category = pd.Categorical(firsts.category),
                      decade = firsts.year - firsts.year % 10))
data

plot = (ggplot(data, aes(x = data.decade, fill = data.category)) +
  geom_bar(colour = "floralwhite", width=8.0) +
 labs(
    x = "",
    y = "",
    title = "African-American firsts",
    subtitle = "Number of first achievements by African-Americans by category and decade",
    caption = "Source: https://en.wikipedia.org/wiki/List_of_African-American_firsts"
  ) +
  theme_minimal() +
  scale_x_continuous(breaks = range(1730, 2015, 10)) +
  theme(
    text = element_text(colour = "floralwhite"),
    line = element_line(colour = "floralwhite"),
    axis_text = element_text(colour = "floralwhite"),
    axis_text_y = element_blank(),
    axis_text_x = element_text(angle = 90, vjust = 0.5),
    axis_line_x = element_line(colour = "floralwhite"),
    axis_ticks = element_line(),
    axis_ticks_major_x = element_blank(),
    axis_ticks_minor_x = element_blank(),
    axis_line_y = element_blank(),
    axis_ticks_major_y = element_blank(),
    axis_ticks_minor_y = element_blank(),
    legend_key_width = 19.8,
    legend_key_height = 2.8,
    legend_position = (0.25, 0.75),
    legend_text = element_text(size = 8),
    legend_title = element_blank(),
    legend_spacing = 8.5, 
    panel_grid = element_blank(),
    plot_background = element_rect(fill = "slategray", colour = "floralwhite"),
    plot_title = element_text(ha = "right", weight="heavy")
  ))

plot

