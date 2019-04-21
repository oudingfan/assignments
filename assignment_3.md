# 解题思路
以数字货币名称为节点，兑换汇率为边的权重w，构造有向图。

要找到可行的套利路径，即从要增加数量的币种开始，找到一个回到此币种回路，使回路上的权重相乘（权重相乘即为兑换操作），结果大于1（比初始币多），相乘结果越大收益越多，即：

```
w1 * w2 * w3 * ... * wn > 1
```

为了将最大值问题转化为最小值问题，做两次变换：

1. 权重取对数，将乘法问题转化为加法问题：
```
ln(w1) + ln(w2) + ln(w3) + ... + ln(wn) > ln(1)
```

2. 两边乘以 -1：
```
[-ln(w1)] + [-ln(w2)] + [-ln(w3)] + ... + [-ln(wn)] < 0
```

问题即变为找到权重和小于0情况下最小的路径，有负权重的情况下不能使用 Dijkstra 算法，可以使用 Bellman Ford 算法。

典型的 Bellman Ford 最短路径中不允许有“权重和为负的回路”存在，因为如果有“权重和为负的回路”的话，可以无限循环此回路使路径无限小。

而我们的算法正是要找到此“权重和为负的回路”，所以在经典的 Bellman Ford 算法上略作修改，如果发现此回路则返回它即可。

# 伪代码

```python
def bellman_ford(graph):
    # 获取图的基本信息
    edges_length = graph.edges_length  # 边数
    w = graph.w  # 权重

    # 初始化算法相关变量
    distance = [float('inf')] * edges_length  # 到起始点的最短路径
    distance[0] = 0  # 起始点到自己的距离为0
    predecessor = [None] * edges_length  # 前导节点

    # 将所有权重取对数、取负
    for i in range(edges_length):
        for j in range(edges_length):
            w[i][j] = -math.log(w[i][j])

    # 进行松弛操作，向最短路径靠拢
    for _ in range(edges_length - 1):  # 循环(边数-1)遍
        for edge in graph:  # 遍历所有边
            u, v = edge.neighbour  # 取出边连接的节点
            if distance[v] > distance[u] + w[u][v]:  # 如果经过uv这条边更短，则选择这条边
                distance[v] = distance[u] + w[u][v]
                predecessor[v] = u

    # 再循环一次，如果还能够松弛，则存在负权回路，即找到了最佳套利路径，返回此路径
    for node in graph:  # 遍历所有节点
        u, v = node.neighbour  # 取出边连接的节点
        if distance[v] > distance[u] + w[u][v]:  # 如果经过uv这条边更短，则选择这条边
            return predecessor
    else:  # 未找到
        return False
```