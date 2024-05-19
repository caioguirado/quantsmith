# %%
import numpy as np
import pandas as pd
import hiplot as hip
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from statannotations.Annotator import Annotator


f1_laps = pd.read_csv("../../data/f1_laps_train.csv")
f1_laps = f1_laps.assign(
    f1_laps_dt=lambda x: pd.to_datetime(x["date"]),
    year=lambda x: x["f1_laps_dt"].dt.year,
    log_lap_time_ms=lambda x: x["lapTime_ms"].apply(np.log),
)
f1_laps.to_csv("../../data/f1_laps_train_FE.csv")

# %%
columns_to_visualize = [
    # "constructor",
    "avgDriverFinish",
    "avgConstructorFinish",
    "lapNumber",
    "lapPosition",
    "pitStop",
    "pitCount",
    "pitTime_ms",
    "lapTime_ms",
]
hip.Experiment.from_iterable(
    f1_laps[columns_to_visualize].sample(1000).to_dict(orient="records")
).display()

# %%
f1_laps.to_dict(orient="records")

# %%
pit_data = f1_laps.query("pitTime_ms > 0")[
    ["pitTime_ms", "year", "constructor"]
].assign(
    pit_time_seconds=lambda x: x["pitTime_ms"] / 10000.0,
    is_top_tier_constructor=lambda x: x["constructor"]
    .str.lower()
    .isin(["ferrari", "mercedes", "red bull"]),
)

# %%
sns.displot(
    data=pit_data.query("pit_time_seconds < 3"),
    x="pitTime_ms",
    hue="is_top_tier_constructor",
    kind="kde",
)

# %%

x = "is_top_tier_constructor"
y = "pitTime_ms"
box_plot_data = pit_data.query("pit_time_seconds < 3")
ax = sns.boxplot(
    data=box_plot_data,
    y=y,
    x=x,
    showfliers=False,
)

# %%
x_vals = box_plot_data.query("is_top_tier_constructor == True")["pitTime_ms"].values
y_vals = box_plot_data.query("is_top_tier_constructor == False")["pitTime_ms"].values
test_result = mannwhitneyu(x=x_vals, y=y_vals)

# %%
annotator = Annotator(
    ax,
    pairs=[["True"], ["False"]],
    data=box_plot_data,
    x=x,
    y=y,
    order=["False", "True"],
)
annotator.configure(test="Mann-Whitney", text_format="star", loc="outside")
annotator.apply_and_annotate()

# %%
pit_data.describe()

# %%
constructor_filter = ["Ferrari", "Toyota"]
sns.displot(
    data=f1_laps.query("constructor in @constructor_filter"),
    x="log_lap_time_ms",
    hue="constructor",
    kind="kde",
)
plt.show()

# %%
