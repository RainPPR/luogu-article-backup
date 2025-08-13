---
title: CF1884B Haunted House 题解
date: 1698660806
description: 借鉴了当前 另一篇题解httpswwwluogucomcnblogpost655309，加了更多的说明。

 简化题意

给定一个长度为 n 的二进制串 S，求 f1f2cdotsfn。

其
author: 371511
---

借鉴了当前 [另一篇题解](https://www.luogu.com.cn/blog/_post/655309)，加了更多的说明。

## 简化题意

给定一个长度为 $n$ 的二进制串 $S$，求 $f(1),f(2),\cdots,f(n)$。

其中，$f(i)$ 定义为，每次交换相邻的两个二进制位，将 $S$ 的后 $i$ 为全变为 $0$ 的最小交换次数。

## 分析

特殊的，$f(0)=0$。

假设我们已经求出了 $f(i-1)$，那么就可以用 $f(i-1)$ 步将后 $i-1$ 位变为 $0$。

然后考虑再处理一位。

先贪心的考虑这一位，一定是将这个 $1$ 与后面的第一个 $0$ 交换，而交换的花费为这两位的下标相减（需要依次交换这么多个相邻元素。

以上如果不理解的，可以自己手动模拟两个。

然后，为什么一位一位的考虑，就一定是最优解呢？

证明：这个操作方法，截至到每一位，后面所有的 $1$ 一定会依次从后往前占用前面的 $0$，而不存在比这更优的方法。

## 实现

两个指针，一个 $i$ 记录当前的位置，一个 $j$ 记录前面第一个 $0$。

注意：每次都需要将 $j$ 指针前移一位，表示这个 $0$ 已经被占用。

## 代码

评测记录：<https://codeforces.com/contest/1884/submission/230477092>

```cpp
#include <bits/stdc++.h>

using namespace std;

using ll = long long;

void solve(int n, string s) {
    ll ans = 0;
    for (int i = n - 1, j = n - 1; ~i; --i, --j) {
        while (j >= 0 && s[j] == '1') --j;
        if (j < 0) printf("-1 ");
        else printf("%lld ", ans += i - j);
    }
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T; cin >> T;
    while (T--) {
        int n; string s;
        cin >> n >> s;
        solve(n, s);
    } return 0;
}
```

