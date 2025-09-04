# %%
import pandas as pd

player_values_transformed = pd.read_parquet(
    "../../../player_values_transformed.parquet"
)

# %%
(
    player_values_transformed.assign(
        timestamp=lambda x: pd.to_datetime(x["x"], unit="ms")
    )
    # .set_index()
    .query('name == "Jude Bellingham"').plot(x="timestamp", y="y")
)

# %%
(
    player_values_transformed.assign(
        timestamp=lambda x: pd.to_datetime(x["x"], unit="ms")
    )
    .set_index("timestamp")
    .groupby("name")
    .resample("6M")
    .mean()
    .query('name == "Jude Bellingham"')
    .reset_index()
    # .plot(x="timestamp", y="y")
    .assign(
        rank=lambda x: x.groupby("name")["timestamp"].rank(method="first").astype(str)
    )
    .rename(columns={"y": "value"})
)

# %%
pivot_df = (
    player_values_transformed.assign(
        timestamp=lambda x: pd.to_datetime(x["x"], unit="ms")
    )
    .set_index("timestamp")
    .groupby("name")
    .resample("6M")
    .mean()
    # .query('name == "Jude Bellingham"')
    .reset_index()
    .assign(
        rank=lambda x: x.groupby("name")["timestamp"]
        .rank(method="first")
        .astype(int)
        .astype(str)
    )
    .sort_values(by=["name", "rank"])
    .pivot(index="name", columns="rank", values="y")
    .fillna(method="ffill", axis=1)
    .fillna(method="bfill", axis=1)
    .pipe(
        lambda x: x.set_axis(
            [
                "_".join(col).strip() if isinstance(col, tuple) else col
                for col in x.columns
            ],
            axis=1,
        )
    )
)
pivot_df

# %%
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans
from tslearn.metrics import dtw
from sklearn.preprocessing import StandardScaler

X = pivot_df.values
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

n_clusters = 3
model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
clusters = model.fit_predict(X_normalized)

pivot_df["Cluster"] = clusters

# %%
for cluster in range(n_clusters):
    plt.figure()
    for i, ts in enumerate(X_normalized[clusters == cluster]):
        plt.plot(ts, label=f"{pivot_df[clusters == cluster].iloc[i].name}")
    plt.title(f"Cluster {cluster}")
    plt.legend()
    plt.show()

print(pivot_df[["Cluster"]])

# %%
import altair as alt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_normalized)
pivot_df["PCA1"] = pca_result[:, 0]
pivot_df["PCA2"] = pca_result[:, 1]

# %%
brush = alt.selection_interval()
cluster_selection = alt.selection_multi(
    fields=["Cluster"],
    bind=alt.binding_select(
        options=df_pivot_ri["Cluster"].unique().tolist(), name="Select Cluster: "
    ),
)


df_pivot_ri = pivot_df.copy().reset_index()
scatter = (
    alt.Chart(df_pivot_ri)
    .mark_circle(size=60)
    .encode(
        x="PCA1",
        y="PCA2",
        color="Cluster:N",
        tooltip=["name", "Cluster"],
    )
    .add_selection(brush)
    .transform_filter(cluster_selection)
    .properties(title="PCA Scatter Plot")
)

df_melted = df_pivot_ri.melt(
    id_vars=["name", "Cluster", "PCA1", "PCA2"],
    var_name="Timestep",
    value_name="Market Value",
)
df_melted["Timestep"] = df_melted["Timestep"].astype(int)

lines = (
    alt.Chart(df_melted)
    .mark_line()
    .encode(
        x="Timestep:O",
        y="Market Value:Q",
        color="name:N",
        tooltip=["name", "Market Value", "Timestep"],
    )
    .transform_filter(brush)
    .transform_filter(cluster_selection)
    .properties(title="Market Value Over Time")
)

# Concatenating both charts side by side
# Create a dropdown control chart
dropdown = (
    alt.Chart(df_pivot_ri)
    .mark_text()
    .encode(text=alt.value("Select Cluster:"))
    .properties(height=30)  # Adjust height for spacing
)

# Combine the dropdown and scatter plot, then concatenate with the line plot
chart = (
    alt.vconcat(dropdown, scatter)
    .add_selection(cluster_selection)
    .resolve_scale(y="independent")
    & lines
)

chart.show()
# %%
