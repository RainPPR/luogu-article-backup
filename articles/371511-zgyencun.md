---
title: POJ3233 Matrix Power Series 题解
date: 1709965291
description: 题目描述： 给定一个 ntimes n 的矩阵 A，和一个正整数 k， 求一个矩阵 SAA2A3dotsAk。 题解： 考虑矩阵乘法优化线性递推。 设 SiAA2A3dotsAk。
author: 371511
---

题目描述：

给定一个 $n\times n$ 的矩阵 $A$，和一个正整数 $k$，

求一个矩阵  $S=A+A^2+A^3+\dots+A^k$。

题解：

考虑矩阵乘法优化线性递推。

设 $S_i=A+A^2+A^3+\dots+A^k$。

把矩阵当成矩阵的元素，即设矩阵 $F_k=\begin{bmatrix}A^k&S_k\end{bmatrix}$


考虑设计转移矩阵 $B$，满足 $BF_{k-1}=F_k$。

易得，$B=\begin{bmatrix}A&0\\A&1\end{bmatrix}$，其中 $0$ 表示零矩阵，$1$ 表示单位矩阵。

根据矩阵乘法优化线性递推，那么 $F_k=B^kF_0$。

由定义，$F_0=\begin{bmatrix}1&1\end{bmatrix}$，然后就很简单了。代码：

```cpp
#include <iostream>
#include <cstdio>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <string>
#include <string.h>
#include <vector>

using namespace std;

int n, k, m;

struct matrix_int {
	int n; vector<vector<int> > a;
	matrix_int() { }
	matrix_int(int n): n(n) { a.resize(n, vector<int>(n)); }
	void set() { for (int i = 0; i < n; ++i) a[i][i] = 1; }
	void reset(int x = 0) { for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) a[i][j] = x; }
	void print() { for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) cout << a[i][j] << (j == n - 1 ? "\n" : " "); }
	friend matrix_int operator +(const matrix_int &a, const matrix_int &b) {
		int n = a.n; matrix_int r(n);
		for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
		r.a[i][j] = (a.a[i][j] + b.a[i][j]) % m;
		return r;
	}
	friend matrix_int operator *(const matrix_int &a, const matrix_int &b) {
		int n = a.n; matrix_int r(n);
		for (int i = 0; i < n; ++i)
		for (int k = 0; k < n; ++k)
		for (int j = 0; j < n; ++j)
		r.a[i][j] = (r.a[i][j] + 1ll * a.a[i][k] * b.a[k][j] % m) % m;
		return r;
	}
};

matrix_int zero, one;

struct matrix_matrix {
	int n; vector<vector<matrix_int> > a;
	matrix_matrix() { }
	matrix_matrix(int n): n(n) { a.resize(n, vector<matrix_int>(n)); }
	void set() { for (int i = 0; i < n; ++i) a[i][i] = one; }
	void reset(matrix_int x = zero) { for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) a[i][j] = x; }
	friend matrix_matrix operator *(const matrix_matrix &a, const matrix_matrix &b) {
		int n = a.n; matrix_matrix r(n);
		for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
		r.a[i][j] = matrix_int(a.a[0][0].n);
		for (int i = 0; i < n; ++i)
		for (int k = 0; k < n; ++k)
		for (int j = 0; j < n; ++j)
		r.a[i][j] = r.a[i][j] + a.a[i][k] * b.a[k][j];
		return r;
	}
};

template<typename tp>
tp qpow(tp a, int k) {
	tp r = a; --k;
	while (k) {
		if (k & 1) r = r * a;
		a = a * a; k >>= 1;
	} return r;
}

void solev() {
	cin >> n >> k >> m;
	if (n == 0 && k == 0) return;
	matrix_int a(n);
	for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) cin >> a.a[i][j];
	zero = matrix_int(n), one = matrix_int(n); one.set();
	matrix_matrix b(2);
	b.a[0][0] = a, b.a[0][1] = zero;
	b.a[1][0] = a, b.a[1][1] = one;
	b = qpow(b, k);
	b.a[1][0].print();
}

signed main() {
	ios::sync_with_stdio(false);
	cin.tie(0), cout.tie(0);
	solev();
	return 0;
}
```

PS：洛谷上有双倍经验（[UVA11149 Power of Matrix](https://www.luogu.com.cn/problem/UVA11149)）但是卡输入格式卡输出个数卡输入大小，
