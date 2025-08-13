---
title: 题解：CF1098D Eels
date: 1721956541
description: UPD 20240726 题解被打回后：修改了缺少的逗号（  分析合并策略 设一次合并 A 和 B，我们钦定 Age B。 若这次合并是危险的，那么有 Ale2B， 我们考虑证明结论，从小到大合并可以最大化危险合并次数
author: 1218731
---

UPD 20240726 题解被打回后：修改了缺少的逗号（

### 分析合并策略

设一次合并 $A$ 和 $B$，我们钦定 $A\ge B$。

若这次合并是危险的，那么有 $A\le2B$，

我们考虑证明结论，**从小到大合并可以最大化危险合并次数**。

考虑证明对于一个小的集合 $S=\{A,B,C\}$，其中 $C\ge A\ge B$，

---

如果合并了当前鱼的集合 $S$ 中最小的两个 $A,B$，

那么下一次合并，若 $A+B\ge C$ 那么一定满足 $A+B\le 2C$。

---

反过来，如果合并了较大的两个 $C,A$，

那么下一次合并，有 $A+C\ge B$，但是 $A+C\le 2B$ 一定不成立。

---

因此，我们证明了对于任意大小为 $3$ 的集合成立，

也就是说，对于任意原集合的大小为 $3$ 的子集都成立，

容易得出，对于原集合也成立。

### 统计答案

我们使用经典策略，将鱼分为以下若干块，

$$
[1,2),[2,4),\dots,[2^i,2^{i+1}),\dots
$$

我们发现，每个块内的合并一定都是危险的，

也就是不危险的合并一定存在于不同的块之间。

我们考虑证明结论，**不危险的合并一定发生于块首**。

根据前面的结论，我们从小到大合并，

因此对于每一个位置，一定是前面都合并完了，

那么一个位置 $i$ 的贡献为，

$$
\left[2\sum_{j<i}a_j<a_i\right]
$$

我们分类讨论，

+ 若 $a_i$ 是块首元素，那么直接判断这个式子即可；

+ 若 $a_i$ 不是块首元素，注意到 $2a_{i-1}>a_i$ 的，那么上式一定不成立。

于是，我们使用可删堆（`multiset`）维护这若干个块即可。

### 代码

```cpp
#include <bits/stdc++.h>

using namespace std;

#define endl "\n"

using ll = long long;

ll sum[30];
multiset<int> app[30];

signed main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr), cout.tie(nullptr);
	int Q;
	cin >> Q;
	while (Q--) {
		string op;
		int x;
		cin >> op >> x;
		int k = __lg(x);
		if (op == "+") sum[k] += x, app[k].insert(x);
		else sum[k] -= x, app[k].erase(app[k].find(x));
		ll pre = 0, ans = 0;
		for (int i = 0; i < 30; ++i) {
			if (app[i].empty()) continue;
			ans += app[i].size();
			if (*app[i].begin() > 2 * pre) --ans;
			pre += sum[i];
		}
		cout << ans << endl;
	}
	return 0;
}
```
