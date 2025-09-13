"""
PCA on synthetic futures returns (demo inspired by Rob Carver's blog post).

What this script does:
1) Generate synthetic daily returns for a small futures universe.
2) Vol-normalize each series using a rolling volatility.
3) Run a rolling 1Y PCA (latest window) with n_components = min(max(2, N//2), 6).
4) Show explained variance, loadings (top/bottom), and PC cumulative sums.
5) Risk-management example: compute portfolio exposures and hedge PC1 & PC2.
6) Optional "labelling" step: correlate PCs with simple benchmark baskets.

Usage:
- Run directly with Python 3.9+ with numpy/pandas/scikit-learn/matplotlib installed.
- Outputs figures and CSVs under ./pca_demo_outputs/

Notes:
- PC series here are *projections*, not investable PnL. Use cumulative sums to visualise.
- Signs of PCs are arbitrary; we anchor by ensuring SP500 loading on PC1 is positive.
"""

# %%
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["figure.figsize"] = (10, 6)

# %%
def make_synthetic_data(seed=7):
    np.random.seed(seed)
    assets = [
        "EQ_US_SP500", "EQ_EU_EuroStoxx",
        "BOND_US_10Y", "BOND_DE_Bund",
        "ENERGY_WTI", "ENERGY_Brent",
        "METAL_Gold", "METAL_Silver",
        "FX_EURUSD", "FX_JPYUSD",
        "AG_Corn", "AG_Wheat",
    ]
    N = len(assets)

    days = 3 * 252
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)

    # latent factors
    F = np.zeros((days, 3))
    F[:, 0] = np.random.normal(0, 0.015, size=days)  # risk-on
    F[:, 1] = np.random.normal(0, 0.012, size=days)  # rates
    F[:, 2] = np.random.normal(0, 0.010, size=days)  # USD

    # loadings
    L = np.zeros((N, 3))
    L[0] = [ 1.0, -0.2, -0.1]  # SP500
    L[1] = [ 1.1, -0.2, -0.1]  # EuroStoxx
    L[2] = [-0.3,  1.0,  0.0]  # US 10Y
    L[3] = [-0.2,  1.1,  0.0]  # Bund
    L[4] = [ 0.5, -0.2,  0.2]  # WTI
    L[5] = [ 0.5, -0.2,  0.2]  # Brent
    L[6] = [ 0.3, -0.2, -0.6]  # Gold
    L[7] = [ 0.4, -0.2, -0.5]  # Silver
    L[8] = [ 0.0,  0.0, -1.0]  # EURUSD
    L[9] = [-0.2,  0.0, -0.8]  # JPYUSD
    L[10]= [ 0.2,  0.0,  0.0]  # Corn
    L[11]= [ 0.2,  0.0,  0.0]  # Wheat

    idio = np.random.normal(0, 0.01, size=(days, N))
    raw = F @ L.T + idio

    target_daily_vol = np.array([0.012, 0.013, 0.007, 0.007, 0.02, 0.02, 0.011, 0.014, 0.006, 0.008, 0.015, 0.015])
    scale = target_daily_vol / raw.std(axis=0, ddof=1)
    returns = raw * scale

    ret_df = pd.DataFrame(returns, index=dates, columns=assets)
    return ret_df

def vol_normalize(ret_df, window_vol=63):
    rolling_vol = ret_df.rolling(window_vol).std().shift(1)
    return (ret_df / rolling_vol).dropna()

def run_pca(window_data, n_components):
    X = window_data - window_data.mean(axis=0)
    pca = PCA(n_components=n_components)
    pca.fit(X.values)

    explained = pd.Series(pca.explained_variance_ratio_, index=[f"PC{k+1}" for k in range(n_components)])
    loadings = pd.DataFrame(pca.components_.T, index=window_data.columns, columns=[f"PC{k+1}" for k in range(n_components)])
    factors = pd.DataFrame(pca.transform(X.values), index=window_data.index, columns=[f"PC{k+1}" for k in range(n_components)])

    # Fix sign so SP500 loads positively on PC1 (if present)
    if "EQ_US_SP500" in loadings.index and loadings.loc["EQ_US_SP500", "PC1"] < 0:
        loadings["PC1"] *= -1
        factors["PC1"] *= -1

    return explained, loadings, factors

def top_bottom(s, k=6):
    s = s.sort_values()
    return pd.concat([s.head(k).rename("Weight"), s.tail(k).rename("Weight")])

def label_factors(factors, window_data):
    """Crude labelling: correlate PC returns with simple baskets."""
    baskets = {
        "EquityBasket": window_data[["EQ_US_SP500", "EQ_EU_EuroStoxx"]].mean(axis=1),
        "BondBasket":   window_data[["BOND_US_10Y", "BOND_DE_Bund"]].mean(axis=1),
        "EnergyBasket": window_data[["ENERGY_WTI", "ENERGY_Brent"]].mean(axis=1),
        "MetalsBasket": window_data[["METAL_Gold", "METAL_Silver"]].mean(axis=1),
        "USDProxy":    -window_data[["FX_EURUSD", "FX_JPYUSD"]].mean(axis=1),  # minus because up USD ~ down EURUSD, JPYUSD
    }
    baskets = pd.DataFrame(baskets).loc[factors.index]
    corr = factors.corrwith(baskets, axis=0)
    # Return a table of correlations per PC
    out = pd.DataFrame({pc: baskets.corrwith(factors[pc]) for pc in factors.columns})
    return out

# %%
# def main():
outdir = Path("pca_demo_outputs")
outdir.mkdir(exist_ok=True)

ret_df = make_synthetic_data()
vol_norm = vol_normalize(ret_df, window_vol=63)

win = 252
window_data = vol_norm.iloc[-win:]
n_components = min(max(2, window_data.shape[1] // 2), 6)

explained, loadings, factors = run_pca(window_data, n_components)

# Save CSVs
explained.to_csv(outdir / "explained_variance.csv")
loadings.to_csv(outdir / "loadings.csv")
factors.to_csv(outdir / "pc_returns.csv")

# %% 
# Top/Bottom for PC1 & PC2 (if exist)
for pc in ["PC1", "PC2"]:
    if pc in loadings.columns:
        tb = top_bottom(loadings[pc], k=6)
        tb.to_csv(outdir / f"{pc}_top_bottom.csv")

# Plots
ax = explained.plot(kind="bar", rot=0, title="Explained variance ratio (latest 1Y window)")
ax.figure.tight_layout()
ax.figure.savefig(outdir / "explained_variance.png")
plt.close(ax.figure)

for pc in ["PC1", "PC2"]:
    if pc in factors.columns:
        ax = factors[pc].cumsum().plot(title=f"{pc} cumulative sum (latest 1Y window)")
        ax.figure.tight_layout()
        ax.figure.savefig(outdir / f"{pc}_cumsum.png")
        plt.close(ax.figure)

# Tiny risk-management demo
assets = list(window_data.columns)
portfolio_w = pd.Series(
    {
        "EQ_US_SP500":  0.4,
        "EQ_EU_EuroStoxx": 0.2,
        "BOND_US_10Y":  -0.2,
        "BOND_DE_Bund": -0.1,
        "ENERGY_WTI":   0.2,
        "ENERGY_Brent": 0.2,
        "METAL_Gold":   0.1,
        "METAL_Silver": 0.1,
    }, index=assets
).fillna(0.0)

expo = portfolio_w.values @ loadings.values
expo = pd.Series(expo, index=loadings.columns)
expo.to_csv(outdir / "exposures_before.csv")

# Hedge PC1 & PC2 with SPX and US10Y if present
hedge_assets = [a for a in ["EQ_US_SP500", "BOND_US_10Y"] if a in assets]
hedge_pcs = [pc for pc in ["PC1", "PC2"] if pc in loadings.columns]
if len(hedge_assets) == 2 and len(hedge_pcs) == 2:
    H = loadings.loc[hedge_assets, hedge_pcs].values.T
    b = -expo[hedge_pcs].values.reshape(2, 1)
    x = np.linalg.solve(H, b)
    hedge_w = pd.Series({hedge_assets[0]: x[0, 0], hedge_assets[1]: x[1, 0]})
    new_w = portfolio_w.copy()
    new_w.loc[hedge_assets] += hedge_w
    new_expo = pd.Series(new_w.values @ loadings.values, index=loadings.columns)

    pd.DataFrame({"Before": expo[hedge_pcs], "After": new_expo[hedge_pcs]}).to_csv(outdir / "exposures_before_after.csv")
    hedge_w.to_csv(outdir / "hedge_weights.csv")

# Optional labelling
labels = label_factors(factors, window_data)
labels.to_csv(outdir / "factor_label_correlations.csv")

# if __name__ == "__main__":
#     main()
# %%
