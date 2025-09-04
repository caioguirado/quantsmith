# %%
import pickle
import pandas as pd

with open("../../../player_values.pickle", "rb") as f:
    player_value_dev_curves = pickle.load(f)

# %%
player_values = pd.DataFrame(player_value_dev_curves)
# %%
player_values_transformed = (
    player_values.explode("values")
    .reset_index(drop=True)
    .assign(
        x=lambda x: x["values"].apply(lambda x: x.get("x")),
        y=lambda x: x["values"].apply(lambda x: x.get("y")),
    )
    .drop(columns=["values"])
)

# %%
player_values_transformed.to_parquet("../../../player_values_transformed.parquet")

# %%
