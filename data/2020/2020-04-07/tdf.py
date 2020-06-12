# Cleaning and presenting TdF data
# David Robinson [Tidy Tuesday](https://www.youtube.com/watch?v=vT-DElIaKtE) video
# Tour de France [dataset](https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-04-07/readme.md)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = "."
stage_data = pd.read_csv(f"{DATA_DIR}/stage_data.csv")
tdf_stages = pd.read_csv(f"{DATA_DIR}/tdf_stages.csv")
tdf_winners = pd.read_csv(f"{DATA_DIR}/tdf_winners.csv")

# NOTENOTE: there are missing time_overall for some winners in the old days
# is this a parse error or something else?
tdf_winners = tdf_winners.assign(
                year = pd.DatetimeIndex(tdf_winners["start_date"]).year,
                speed = pd.Float64Index(tdf_winners["distance"]) / 
                        pd.Float64Index(tdf_winners["time_overall"]))

# This is done in dplyr using a pipe operator
# In pandas, I think I can chain using "." since functions like assign()
# will return a dataframe as the return value.
# TODO: what would it look like to write a function to clean column names
# that also returns the input dataframe so that we can cleanly compose?

tdf_stages.columns = tdf_stages.columns.str.strip().str.lower().str.replace(' ', '_')
tdf_stages = tdf_stages.assign(
                year = pd.DatetimeIndex(tdf_stages["date"]).year)

# Count the number of winners of the TdF based on birth_country
tdf_winners["birth_country"].value_counts()

# Note that value_counts() returns a Series object
country_winners = tdf_winners["birth_country"].value_counts()
# The row labels are returned by axes
country_winners.axes
# The values are returned by values
country_winners.values

# Now let's make it horizontal
country_winners.plot.barh()

# I want the longest bar on the top
country_winners.plot.barh()
plt.gca().invert_yaxis()
plt.title("What countries were the most Tour de France winners born in?")

# Now how do I rewrite the above plot using objects explicitly?
ax = country_winners.plot.barh()
ax.invert_yaxis()
ax.set_title("What countries were the most Tour de France winners born in?")

# Completely explicit version, starting by creating the plot
fig, ax = plt.subplots()
ax.barh(country_winners.index, country_winners.values)
ax.invert_yaxis()
ax.set_title("What countries were the most Tour de France winners born in?")

# How does winner attributes change over time?
# Original R code:
#
# by_decade <- tdf_winners %>% 
#     group_by(decade = 10 * (year %/% 10)) %>% 
#     summarize(winner_age = mean(age),
#               winner_height = mean(height, na.rm = TRUE),
#               winner_weight = mean(weight, na.rm = TRUE),
#               winner_margin = mean(time_margin, na.rm = TRUE),
#               winner_speed = mean(speed, na.rm = TRUE)) 
#
# Idiomatic pandas code that uses method chaining idiom:
by_decade = (tdf_winners.assign(decade = tdf_winners["year"] - tdf_winners["year"] % 10)
            .groupby("decade")
            .agg(
                # Promote groupby into its own column
                decade = pd.NamedAgg(column='decade', aggfunc='first'),
                winner_age = pd.NamedAgg(column='age', aggfunc='mean'), 
                winner_height = pd.NamedAgg(column='height', aggfunc='mean'),
                winner_weight = pd.NamedAgg(column='weight', aggfunc='mean'),
                winner_margin = pd.NamedAgg(column='time_margin', aggfunc='mean'),
                winner_speed = pd.NamedAgg(column='speed', aggfunc='mean')
            ))

by_decade

# Visualize decade average margin of victory in the TdF over time
#
# Original R code: 
# by_decade %>% 
#     filter(decade >= 1910) %>% 
#     ggplot(aes(decade, winner_margin * 60)) +
#     geom_line() +
#     expand_limits(y = 0) +
#   labs(x = "Decade",
#        y = "Average victory margin (minutes)",
#        title = "Tour de France margin of victory has been getting smaller")

# NOTENOTE: the code below doesn't chain well - for example if I wanted to set 
# the y axis label via set_ylabel() it returns a text object which doesn't let
# me chain the subsequent set_title() call (or vice-versa)
#
# There is an interesting library called plotnine that lets me do a bunch of 
# interesting things that are ggplot inspired: https://github.com/has2k1/plotnine

(by_decade.query('decade >= 1910')
          .plot
          .line(y='winner_margin')
          .set_title('TdF margin of victory has been getting smaller')
)

from plotnine import *

newer = (by_decade.query('decade >= 1910')
                  .assign(winner_margin_min = by_decade['winner_margin'] * 60))

# There is a nice convenience expression in ggplot/R where I can simply
# multiply a column by 60 within the aes() expression itself.

(ggplot(newer, aes('decade', 'winner_margin_min'))
        + geom_line()
        + expand_limits(y = 0)
        + labs(x = "Decade",
                y = "Average victory margin (min)",
                title = "Tour de France margin of victory has been getting smaller"
        )
)
