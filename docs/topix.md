# TOPIX のリターンは正規分布に従うのか

TOPIX のリターンは正規分布に従うのかを検証する．

## ライブラリのインポート

```python
import pandas as pd
import numpy as np
import japanize_matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
az.style.use('arviz-darkgrid')
import yfinance as yf
```

## データの取得

TOPIX の価格データを取得し，日次対数リターンを計算する．

- 出所: Yahoo Finance
- 期間: 2014 年 12 月 01 日 から 2024 年 11 月 29 日

日次リターンの計算方法

$$
R_t = \log{P_t} - \log{P_{t-1}}
$$

```python
import pandas as pd
import yfinance as yf

# TOPIXの価格データを取得
topix = yf.download('^TOPX', start='2014-11-29', end='2024-11-29')
# 対数化
topix['log_adj_close'] = np.log(topix['Adj Close'])
# 階差を計算
topix['log_adj_close_diff'] = topix['log_adj_close'].diff()
# データの先頭を表示
topix.head()
```

## データのプロット

```python
plt.figure(figsize=(12, 6))

plt.subplot(211)
sns.lineplot(x=topix.index, y='log_adj_close_diff', data=topix)
plt.ylabel('')
plt.xlabel('')

plt.subplot(212)
sns.histplot(topix['log_adj_close_diff'], kde=True)
plt.ylabel('')
plt.xlabel('')

plt.show()
```

![alt text](image.png)

## 推定

TOPIX のリターンは正規分布に従うのかを検証する．

### モデル

$$
\begin{aligned}
y &\sim \mathcal{N}(\mu, \sigma) \\
\mu &\sim \mathcal{N}(0, 0.01) \\
\sigma &\sim \text{HalfNormal}(0.01)
\end{aligned}
$$

```python
with pm.Model() as topix_normal:
    # data
    y = pm.Data('y', topix['log_adj_close_diff'].dropna())

    # prior
    mu = pm.Normal('mu', mu=0, sigma=0.01)
    sigma = pm.HalfNormal('sigma', sigma=0.01)

    # likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)

    # sampling
    trace_normal = pm.sample(
        draws=1000,
        tune=1000,
        chains=4,
        nuts_sampler='numpyro'
    )
```

## 推定結果

### トレースプロット

```python
az.plot_trace(trace_normal);
```

![alt text](image-1.png)

### 事後予測

```python
with topix_normal:
    pm.sample_posterior_predictive(trace_normal, extend_inferencedata=True)

az.plot_ppc(trace_normal, num_pp_samples=100)
plt.show()
```

![alt text](image-3.png)

観測データが黒線，事後予測が青線で示されている．

観測データは正規分布よりも尖っており，うまく説明できていないことがわかる．

### リターン

```python
annualized_return = trace_normal.posterior_predictive['y_obs'].values.flatten().mean() * 365.25
annualized_volatility = trace_normal.posterior_predictive['y_obs'].values.flatten().std() * np.sqrt(365.25)
print(f'年率リターン: {annualized_return:.2%}')
print(f'年率ボラティリティ: {annualized_volatility:.2%}')
```

## まとめ

TOPIX のリターンは正規分布に従うとは言い難い．

次回は，t 分布を用いて検証しよう．
