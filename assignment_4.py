"""
算法说明：
    用for循环遍历价格数组，当前最小值与当前最大值的差即为局部最优结果，
    记录到 max_distance 变量，循环到最后直到找到全局最优结果。

另一种遍历算法使用for嵌套，时间复杂度为 n^2，未使用此方法
"""

prices = [7, 1, 5, 3, 6, 4]
# prices = [7, 6, 4, 3, 1]

max_distance = 0  # 已计算出的最大盈利
min_number = prices[0]  # 已知最小价格

for price in prices:
    if price < min_number:  # 更新最小价格
        min_number = price

    distance = price - min_number  # 计算盈利
    if max_distance < distance:  # 当前最大盈利比以前局部最大盈利更优
        max_distance = distance  # 更新最优盈利

print(max_distance)
