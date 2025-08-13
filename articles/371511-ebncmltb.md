---
title: 题解：P10450 [USACO03MAR] Best Cow Fences G
date: 1716514333
description: 考虑朴素算法。 枚举左右端点，前缀和计算平均值。 这样做是 mathcal On2 的。 考虑很经典的平均值的思想，将一个序列减去其平均值，其和为零。 如果我们二分一个数，然后找到一个序列，减去二分的平均值，大于等于零则可行。 于是我
author: 371511
---

考虑朴素算法。

枚举左右端点，前缀和计算平均值。

这样做是 $\mathcal O(n^2)$ 的。

考虑很经典的平均值的思想，将一个序列减去其平均值，其和为零。

如果我们二分一个数，然后找到一个序列，减去二分的平均值，大于等于零则可行。

于是我们可以继续这个思路，考虑如何 check。

前缀和一定是需要的，显然。有一句话说得好，简单好用的工具，能用就用。

然后我们发现，一个长度为 $m$ 的序列，和表示为，$s_r-s_{l-1}$。

如果我们要在有长度要求下，最大化这个值。

显然我们需要一个位置其左侧至少若干位的最小值。

于是，使用类似于双指针的方法，右端不断滑动，左边同时记录最小值。

注意到是浮点数二分，为了精度，我们可以提前将数字乘上 $1000$。

代码：

```cpp
#include <bits/stdc++.h>

using namespace std;

constexpr double eps = 1e-8;

int n, f;
vector<int> a;
vector<double> b;

bool check(double avg) {
	for (int i = 1; i <= n; ++i) b[i] = b[i - 1] + a[i] - avg;
	double lt = 0;
	for (int i = 0, j = f; j <= n; ++i, ++j) {
		lt = min(lt, b[i]);
		if (b[j] - lt >= 0) return true;
	} return false;
}

signed main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr), cout.tie(nullptr);
	cin >> n >> f;
	a.resize(n + 1), b.resize(n + 1);
	for (int i = 1; i <= n; ++i) cin >> a[i], a[i] *= 1000;
	double l = -1e8, r = 1e8;
	while (r - l > eps) {
		double mid = (l + r) / 2;
		if (check(mid)) l = mid;
		else r = mid;
	}
	cout << (long long)r << endl;
	return 0;
}
```

总结一下，这个思想就是，我们可以 $\mathcal O(n^2)$ 的直接求解，也可以 $\mathcal O(n)$ 的判断一个解。

如果这个东西本身具有单调性（或者有人更不直观的说为可二分性），就可以二分把复杂度优化到 $\mathcal O(n\log n)$ 或者其他比较优化的复杂度。
