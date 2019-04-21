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

    if random.choice([True, False]):  # 随机决定是否进行买入卖出操作
        if context.portfolio.positions[security].closeable_amount > 0:
            # 如果已经持仓，则卖出
            order_target(security, 0)  # 卖出所有股票,使这只股票的最终持有量为0
        else:
            # 如果未持仓，则全仓买入
            order_value(security, cash)  # 用所有 cash 买入股票
