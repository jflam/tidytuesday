# Reproduce this great visualization of TdF stages from this 
# #TidyTuesday tweet: https://twitter.com/delaBJL/status/1247552025560338432

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *

DATA_DIR = "."
stage_data = pd.read_csv(f"{DATA_DIR}/stage_data.csv")
tdf_stages = pd.read_csv(f"{DATA_DIR}/tdf_stages.csv")
tdf_winners = pd.read_csv(f"{DATA_DIR}/tdf_winners.csv")

# The interesting thing here is transforming strings into categories

# This clever bit of data cleaning happens because there are strange
# stages in the data like "11A"

stage_numbers = pd.CategoricalDtype(['1', '2', '3', '4', '5', '6', '7', '8', 
                  '9', '10', '11', '12', '13', '14', '15', 
                  '16', '17', '18', '19', '20', '21', '22', 
                  '23', '24', '25'], 
                  ordered=True)

# In modern pandas, I can index into the "type" column, coerce to string and lowercase
def canonicalize_stages(stage_type):
    if re.search("flat", stage_type):
        return "Flat"
    elif re.search("plain", stage_type):
        return "Flat"
    elif re.search("time trial", stage_type):
        return "Time Trial"
    elif re.search("mountain", stage_type):
        return "Mountain"
    elif re.search("transition", stage_type):
        return "Transition"
    elif re.search("intermediate", stage_type):
        return "Transition"
    elif re.search("half", stage_type):
        return "Transition"
    elif re.search("hilly", stage_type):
        return "Hilly"
    else:
        return stage_type

# Idiomatic pandas method chaining solution
#
# Remember that assign() was *inspired by* dplyr::mutate()
#
# Method chaining involves adding additional columns to a dataframe vs.
# mutating in-place which results in return types that are columns which
# in turn prevents method chaining. The below seems to work quite nicely

def summarize(df):
    return (df.assign(cum_dist = df.Distance.cumsum())
              .assign(start_dist_nas = lambda x: x.cum_dist.shift(1))
              .assign(start_dist = lambda x: x.start_dist_nas.fillna(0))
              .loc[:, ['Year', 'StageNumber', 'StageType', 'Origin', 'Destination', 'Distance', 'cum_dist', 'start_dist']]
)

res = (tdf_stages.assign(StageType   = (tdf_stages.Type.str.lower()
                                                  .apply(canonicalize_stages)),
                         Year        = pd.DatetimeIndex(tdf_stages.Date).year,
                         StageNumber = tdf_stages.Stage.astype(stage_numbers))
                 .query('Year >= 2000')
                 .assign(Distance = lambda x: np.where(x.StageType == 'Transition', 
                                                       0, x.Distance))
                 .sort_values(['Year', 'Stage'])
                 .groupby('Year')
                 .apply(summarize))
res

# Now generate the plot for this which is effectively a stacked horizontal bar chart
# It would be interesting to have it so that it can create 

(ggplot(res, aes(fill = 'StageType'))
    + geom_rect(aes(ymin = 'res.Year - 0.45',
                    ymax = 'res.Year + 0.45',
                    xmin = 'res.start_dist',
                    xmax = 'res.cum_dist'))
    + scale_y_reverse()
    + labs(title = "How has the Tour de France Changed?",
           subtitle = "Section types and distance by year"))

# Earlier expression expanded into sub-expressions

tmp1 = tdf_stages.Type.str.lower()
tmp2 = tmp1.apply(canonicalize_stages)
tmp3 = pd.DatetimeIndex(tdf_stages.Date).year
tmp4 = tdf_stages.Stage.astype(stage_numbers)
tmp5 = tdf_stages.assign(StageType   = tmp1.tmp2,
                         Year        = tmp3,
                         StageNumber = tmp4)
tmp6 = tmp5.query('Year >= 2000')
tmp7 = tmp6.assign(Distance = lambda x: np.where(x.StageType == 'Transition',
                                                 0, x.Distance))
tmp8 = tmp7.sort_values(['Year', 'Stage'])
tmp9 = tmp8.groupby('Year')
tmpa = tmp9.apply(summarize)
