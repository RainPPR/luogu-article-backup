---
title: P1485 火枪打怪 题解
date: 1691640916
description: 新手第一次写题解 qwq 因为这道题我整整调了一整天，所以我尽可能讲的详细又简洁。  题目描述 共有 n 个怪物，血量为 mi，现在要打死这些怪物（血量  0）。每次攻击第 i 个怪物，它会掉 p 滴血，同时左侧第
author: 371511
---

新手第一次写题解 qwq

~~因为这道题我整整调了一整天~~，所以我尽可能讲的详细又简洁。

## 题目描述

共有 $n$ 个怪物，血量为 $m_i$，现在要打死这些怪物（血量 $< 0$）。每次攻击第 $i$ 个怪物，它会掉 $p$ 滴血，同时左侧第 $j$ 个怪物会掉 $\max(0, p - (i - j) ^ 2)$ 滴血。

共使用 $k$ 次攻击，求最小的 $p$。

## 简要分析

### 0x01

求一个可行的最小值，对于每一个值都是明显的**是否可行**。

同时因为 $p$ 越大，$k$ 一定会越来越小（或者维持不变），所以答案是具有单调性的。

因此可以看出，题目可以使用二分答案来做。

瞄一眼数据范围 $10^{10}$ 好吧我直接开 `long long` 了。

然后就是考虑怎么设计 Check 函数了。

### 0x02

题目说明，当攻击怪物时，只有左侧的怪物会“收到牵连”，所以可以很快的想到，从右侧开始遍历更加方便（没有后效性）。

对于每一个怪物我们都要把它打死（因为再继续往左遍历，右面的怪物不会受到任何影响了）。

所以我们只需要考虑这个怪物会收到多大的牵连就可以了，所以我们接着从题目给的公式入手。

### 0x03

（$f_i$ 为第 $i$ 个怪物收到的溅射伤害值）

（$cnt_i$ 为打死第 $i$ 个怪物的最小攻击次数）

因为是倒着遍历，所以我们考虑将式子转换为一个（或多个，实际上是多个）后缀和进行运算的形式：

$$
\begin{aligned}
	f_i	&= \sum_{j = i + 1}^{\min(n, i + \lfloor \sqrt p \rfloor)} cnt_j \times (p - (j - i) ^ 2) \\
		&= \textstyle \sum cnt_j \times (p - i ^ 2 - j ^ 2 + 2i \times j) \\
		&= \textstyle \sum cnt_j \times p - \sum cnt_j \times j ^ 2 - \sum cnt_j \times i ^ 2 + \sum cnt_j \times 2i \times j \\
		&= \textstyle p \times \sum cnt_j - \sum cnt_j \times j ^ 2 - i ^ 2 \times \sum cnt_j + 2i \times \sum cnt_j \times j \\
		&= \textstyle (p - i ^ 2) \times \sum cnt_j + 2i \times \sum cnt_j \times j - \sum cnt_j \times j ^ 2
\end{aligned}
$$

然后设三个后缀和数组：

$$
\begin{aligned}
	c_i &= \textstyle \sum_{j = i + 1}^n cnt_j \\
	cj_i &= \textstyle \sum_{j = i + 1}^n cnt_j \times j \\
	cjj_i &= \textstyle \sum_{j = i + 1}^n cnt_j \times j ^ 2 
\end{aligned}
$$

然后我们就可以把原式转换为：

$$
\begin{aligned}
	\\
	f_i	&= (p - i ^ 2) \times \sum_{j = i + 1}^{i + \lfloor \sqrt p \rfloor} cnt_j + 2i \times \sum_{j = i + 1}^{i + \lfloor \sqrt p \rfloor} cnt_j \times j - \sum_{j = i + 1}^{i + \lfloor \sqrt p \rfloor} cnt_j \times j ^ 2\\
		&= (p - i ^ 2) \times (c_i - c_{i + \lfloor \sqrt p \rfloor}) + 2i \times (cj_i - cj_{i + \lfloor \sqrt p \rfloor}) - (cjj_i - cjj_{i + \lfloor \sqrt p \rfloor}) \\
	\\
	cnt_i &= \lceil \frac{m_i - f_i + 1}{p} \rceil \\
		&= \lfloor \frac{m_i - f_i + p}{p} \rfloor
\end{aligned}
$$

这样分析就结束了（~~但是我做了一整天［哭］~~）

## 我的代码

有注释

```cpp
#include <bits/stdc++.h>

// 开 long long 不然会爆掉
#define int long long

using namespace std;

const int N = 1e6 + 10;

int read()
{
    int num = 0, flag = 1;
    char ch = getchar();
    for (; !isdigit(ch); ch = getchar())
        if (ch == '-')
            flag = -1;
    for (; isdigit(ch); ch = getchar())
        num = (num << 3) + (num << 1) + ch - '0';
    return num * flag;
}

int n, k;
int m[N];

int c[N];   // cnt 的后缀数组
int cj[N];  // cnt * j 的后缀数组
int cjj[N]; // cnt * j * j 的后缀数组

// 获取某一个怪物背的锅的数量
int getd(int i, int j, int p)
{
    return (p - i * i) * (c[i] - c[j]) + 2 * i * (cj[i] - cj[j]) - (cjj[i] - cjj[j]);
}

bool check(int p)
{
    int x = sqrt(p), res = k;
    for (int i = n; i >= 1; --i)
    {
        int D = getd(i, i + x, p);              // 背的锅
        int cnt = (max(m[i] - D, -p) + p) / p;  // 攻击次数

        if ((res -= cnt) < 0)
            return false;

        // 处理后缀数组
        c[i - 1] = c[i] + cnt;
        cj[i - 1] = cj[i] + cnt * i;
        cjj[i - 1] = cjj[i] + cnt * i * i;
    }
    return true;
}

signed main()
{
    n = read(), k = read();
    for (int i = 1; i <= n; ++i)
        m[i] = read();

    // 二分
    int l = 1, r = 1e11;
    while (l < r)
    {
        int mid = l + r >> 1;
        if (check(mid))
            r = mid;
        else
            l = mid + 1;
    }

    printf("%lld\n", l);
    return 0;
}
```

