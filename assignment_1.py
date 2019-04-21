import requests
import pandas as pd
import matplotlib.pyplot as plt


class PricesDownloader(object):
    """价格数据下载。

    :argument
    API_PREFIX: CryptoCompare 平台 api 地址，文档地址：
        https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataHistoday
    TO_TIMESTAMP: 获取价格数据的截止日期
    """
    API_PREFIX = 'https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=USD&toTs=%s&limit=800'
    TO_TIMESTAMP = 1555689600

    @classmethod
    def fetch_prices(cls, currency):
        """获取价格

        :arg
            currency: 币种

        :return
            DataFrame
        """
        prices_json = requests.get(cls.API_PREFIX % (currency, cls.TO_TIMESTAMP)).json()['Data']
        return pd.DataFrame(prices_json).set_index('time')


# -----------------
# 1：下载历史价格数据
# -----------------
symbols = ('BTC', 'LTC', 'ETH', 'ETC', 'DASH', 'SC', 'STR', 'XEM', 'XMR', 'XRP')
prices = pd.DataFrame()  # 保存所有币种的每日收盘价
for symbol in symbols:  # 循环获取所有币种价格数据
    prices_symbol = PricesDownloader.fetch_prices(symbol)  # 下载价格数据
    prices[symbol] = prices_symbol['close']  # 将此币种价格加入
prices['datetime'] = pd.to_datetime(prices.index, unit='s')  # 将时间戳转化为 datetime 格式
prices.set_index('datetime', inplace=True)  # 将 datetime 设置为 index
print(prices)

# -------------
# 2：绘制价格曲线
# -------------
prices.plot(logy=True)  # 绘制所有价格
plt.ylabel('Coin Value (USD)')  # 纵坐标名称
plt.show()  # 显示图形

# ------------------
# 3：计算相关系数并绘图
# ------------------
corr = prices.corr()  # 计算相关系数矩阵
plt.matshow(corr)  # 绘制相关系数图形
plt.title('CryptoCurrency Correlations')  # 设置图形名称
plt.xticks(range(len(corr.columns)), corr.columns)  # 设置 x 轴中币种名称
plt.yticks(range(len(corr.columns)), corr.columns)  # 设置 y 轴中币种名称
plt.colorbar().set_label('Pearson Coefficient')  # 显示图例并设置名称
plt.show()  # 显示图形
