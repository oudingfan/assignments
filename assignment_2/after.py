from jqdata import *
import random


def initialize(context):
    g.security = '510300.XSHG'  # 交易标的代码
    set_benchmark('000300.XSHG')  # 设定沪深300作为基准
    set_option('use_real_price', True)  # 开启动态复权模式(真实价格)
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
                   type='stock')  # 股票相关设定

    run_daily(market_open, time='open', reference_security='000300.XSHG')  # 开盘时运行


def market_open(context):
    security = g.security
    cash = context.portfolio.available_cash  # 取得当前的现金
    close_data = get_bars(security, count=5, unit='1d', fields=['close'])

    MA5 = close_data['close'].mean()  # 取得过去五天的平均价格
    current_price = close_data['close'][-1]  # 取得上一时间点价格

    if random.choice([True, False]):  # 随机决定是否进行买入卖出操作
        if current_price < MA5 and context.portfolio.positions[security].closeable_amount > 0:
            # 如果上一时间点价格低于五天平均价, 则空仓卖出
            order_target(security, 0)  # 卖出所有股票,使这只股票的最终持有量为0
        elif current_price > 1.01 * MA5:
            # 如果上一时间点价格高出五天平均价1%, 则全仓买入
            order_value(security, cash)  # 用所有 cash 买入股票