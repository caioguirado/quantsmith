# %%
import pandas as pd

items_sales = pd.read_csv('../../data/sales_train_validation.csv')
items_sales.head()

# %%
DATE_COLUMNS = [col for col in items_sales if col.startswith('d_')]
def get_item_time_series(item_id: str):
    filtered_item = items_sales.query(f"id == '{item_id}'")[DATE_COLUMNS]
    return filtered_item.values.reshape(-1)

# %%
import matplotlib.pyplot as plt

random_item_series = get_item_time_series('HOBBIES_1_001_CA_1_validation')
plt.plot(random_item_series[-500:])

# %%
import antropy as ant
print(ant.spectral_entropy(random_item_series, 
                            sf=100, 
                            method='welch', 
                            normalize=True))

# %%
def resample_time_series(df_raw: pd.DataFrame, freq: str):
    dates = pd.date_range(start="2011-01-01", periods=df_raw.shape[1], freq='D')
    time_indexed_df = pd.DataFrame(df_raw.T, index=dates)
    return time_indexed_df.resample(freq).sum().T.values

N_SAMPLES=200
sampled_items = items_sales.sample(n=N_SAMPLES)[DATE_COLUMNS].values
print(sampled_items.shape)
sampled_items = resample_time_series(df_raw=sampled_items, freq='1M')
print(f"Resampled df shape: {sampled_items.shape}")


# %%
import numpy as np
from tqdm import tqdm

time_series_metrics = []
for i in tqdm(range(N_SAMPLES)):
    time_series_metrics.append(
        {
            "PermEnt": ant.perm_entropy(sampled_items[i], order=3, normalize=True),
            "SVDEnt": ant.svd_entropy(sampled_items[i], order=3, normalize=True),
            "SpecEnt": ant.spectral_entropy(sampled_items[i], sf=10, 
                                            normalize=True, method="welch", nperseg=50),
            "AppEnt": ant.app_entropy(sampled_items[i], order=2),
            "SampleEnt": ant.sample_entropy(sampled_items[i], order=2),
            "PetrosianFD": ant.petrosian_fd(sampled_items[i]),
            "KatzFD": ant.katz_fd(sampled_items[i]),
            "HiguchiFD": ant.higuchi_fd(sampled_items[i]),
            "DFA": ant.detrended_fluctuation(sampled_items[i]),
        },
    )

time_series_metrics = pd.DataFrame(time_series_metrics).replace([np.inf, -np.inf], np.nan).fillna(0)
time_series_metrics.head().round(3)

# %%
import umap

mapper = umap.UMAP(n_components=2, random_state=42)
embeddings = mapper.fit_transform(time_series_metrics)

plt.scatter(embeddings[:, 0], embeddings[:, 1])

# %%
import numpy as np
import altair as alt

def get_interactive_chart(series, embeddings):
    ids = np.arange(len(series))
    embed_df = pd.DataFrame({'id': ids.astype(str), 
                                'x': embeddings[:, 0], 'y': embeddings[:, 1]})
    ts_df = (
        pd.DataFrame(series, index=ids.astype(str))
            .reset_index()
            .melt(id_vars='index', var_name='t', value_name='value')
            .rename(columns={'index': 'id'})
    )

    # Merge x,y so the brush (on x,y) can filter the time-series rows
    ts_df = ts_df.merge(embed_df[['id', 'x', 'y']], on='id', how='left')
    alt.data_transformers.disable_max_rows() 

    brush = alt.selection_interval(encodings=['x', 'y'], name='brush')

    scatter = (
        alt.Chart(embed_df)
        .mark_circle(size=48, opacity=0.85)
        .encode(
            x=alt.X('x:Q', title='Dim 1'),
            y=alt.Y('y:Q', title='Dim 2'),
            color=alt.condition(brush, alt.value('steelblue'), alt.value('#d3d3d3')),
            tooltip=['id', 'cluster:O']
        )
        .add_params(brush)
        .properties(height=320, width=700, title='Embeddings — drag to select')
    )

    lines = (
        alt.Chart(ts_df)
        .transform_filter(brush)
        .mark_line(opacity=0.45)
        .encode(
            x=alt.X('t:Q', title='Time index'),
            y=alt.Y('value:Q', title='Value'),
            detail='id:N',
            tooltip=['id:N', 't:Q', 'value:Q']
        )
        .properties(height=260, width=700)
    )

    mean_line = (
        alt.Chart(ts_df)
        .transform_filter(brush)
        .transform_aggregate(mean_value='mean(value)', groupby=['t'])
        .mark_line(strokeWidth=3)
        .encode(
            x='t:Q',
            y='mean_value:Q',
            tooltip=[alt.Tooltip('mean_value:Q', title='mean(selection)'), 't:Q']
        )
    )

    chart = alt.vconcat(
        scatter,
        (lines + mean_line).resolve_scale(y='independent').properties(
            title='Time series of selected points (with mean)'
        )
    ).configure_title(anchor='start')

    return chart

# %%
embeddings_interactive_chart = get_interactive_chart(series=sampled_items, embeddings=embeddings)
embeddings_interactive_chart

# %%
