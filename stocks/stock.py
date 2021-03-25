import pandas as pd
import quandl as q
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

tick = input("Tickers of the stock: ")
sd = input("Start Date in YYYY-MM-DD: ")
ed = input("End Date in YYYY-MM-DD: ")
data = yf.download(tick, start = sd, end = ed)
print(data)

mdata = data.apply(lambda x: x[-1])
monthly_return = mdata.pct_change() * 100
monthly_return.fillna(0, inplace=True)

cnt = data['Adj Close'].count()
print(cnt)
short_lb, long_lb = min(50, cnt), min(200, cnt)
signal_df = pd.DataFrame(index=data.index)
signal_df['signal'] = 0.0
signal_df['short_mav'] = data['Adj Close'].rolling(window=short_lb, min_periods = 1, center=False).mean()
signal_df['long_mav'] = data['Adj Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)   
signal_df['positions'] = signal_df['signal'].diff()
signal_df[signal_df['positions'] == -1.0]

fig = plt.figure()
plt1 = fig.add_subplot(111,  ylabel='Price in $')
data['Adj Close'].plot(ax=plt1, color='r', lw=2.)
signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, signal_df.short_mav[signal_df.positions == -1.0],'v', markersize=10, color='k')
plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, signal_df.short_mav[signal_df.positions == 1.0], '^', markersize=10, color='m')     
plt.show()
