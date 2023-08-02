# 林汐等级机制

## 经验阈值 (experience threshold)
经验阈值是指升级所需的经验点数达到的特定值。当用户的经验点数达到或超过经验阈值时，他们就可以升级到下一个等级。在林汐的等级机制中，经验阈值使用 [对数增长算法](#对数增长算法) 计算，使用对数算法计算经验阈值，可以让每次升级所需的经验点数增长得更加缓慢，从而使得用户在低等级时能够较快地升级，而在高等级时需要更多的经验点数才能升级。

## 初始经验阈值 (base exp)
指用户从 Lv.1 升入 Lv.2 一共需要的经验点

## 经验系数 (cardinality)
经验系数用于控制经验阈值的增长速度。较大的经验增长系数将导致经验阈值快速增加，而较小的系数将导致经验阈值增长较慢

## 对数增长算法
对数增长算法常用的函数是对数函数，即 `y = log(x)`，其中 `x` 是输入值，`y` 是对应的输出值。对数函数的特点是：随着x的增加，y的增长速度逐渐减慢。例如，当x从1增加到10时，y的变化很大；但当x从100增加到1000时，y的变化就相对较小了。
