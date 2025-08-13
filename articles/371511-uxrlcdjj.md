---
title: 题解：P10590 磁力块
date: 1723083437
description: b'6aKY55uu77yaW1AxMDU5MCDno4HlipvlnZddKGh0dHBzOi8vd3d3Lmx1b2d1LmNvbS5jbi9wcm9ibGVtL1AxMDU5MCnvvIxbQ0YxOThFIEdyaXBwaW5nIFN0b3J5XShodHRwczovL3d3dy5sdW9ndS5jb20uY24vcHJvYmxlbS9DRjE5OEUp44CCCgrotKrlv4PnmoTogIM='
author: 371511
---

题目：[P10590 磁力块](https://www.luogu.com.cn/problem/P10590)，[CF198E Gripping Story](https://www.luogu.com.cn/problem/CF198E)。

贪心的考虑，我们希望对于已有的每一个磁石都吸引一遍。

那么直接类似 BFS 的做，复杂度是 $\mathcal O(n^2)$ 的。

考虑 BFS + 分块。

我们记 $d_i$ 表示第 $i$ 个磁石到 $(x_0,y_0)$ 的距离。

先将所有的点按照到 $d_i$ 升序排序，按照 $\sqrt n$ 大小分块。

块内再开一个数组，将所有的点按照质量升序排序。

分别考虑每一个磁石 $R,P$，将没有被吸引过的磁石的块分为以下三类：

1. 这一块的 $d_i$ 全都 $\le R$。

2. 这一块的 $d_i$ 全都 $>R$。

3. 这一块的 $d_i$ 包括了 $\le,> R$ 的。

考虑如何处理：

+ 对于第一类，我们直接暴力从头遍历直到 $m_i>P$。

+ 对于第二类，我们不管。

+ 对于第三类，我们暴力的遍历，可以吸引的加入并标记为删除。

考虑复杂度：

+ 对于第一类，每个点最多被遍历一次（然后就入队了），因此是 $\mathcal O(n)$ 的。

+ 对于第三类，每次最多处理 $1$ 个这样的块，每次复杂度是 $\mathcal O(\sqrt n)$ 的。

因此，时间复杂度为 $\mathcal O(n\sqrt n)$。

实现细节：

+ 我们并不需要实际删除节点，可以打标记表示删除。

+ 代码：

```cpp
#ifndef M_DEBUG
#define NDEBUG 1
#define FAST_IO 1
#define D(x) ({ void(0); })
#else
#define D(x) ({ auto t = (x); cerr << "| DEBUG #" << __LINE__ << " IN " << __FUNCTION__ << "() \t| \t" << #x << " = \t[" << t << "]\n"; void(0); })
#endif

#include <bits/stdc++.h>

#ifdef FAST_IO
#define endl "\n"
#endif

using namespace std;

// -----------------------------------------------------------------------------

using ll = long long;

constexpr int N = 3e5 + 10;

namespace solev {
    int n;
    int p0, r0;
    int x0, y0;

    struct query {
        int p;
        ll r2;
        query() = default;
        query(int p, int r): p(p), r2(1ll * r * r) {}
    };

    // -------------------------------------------------------------------------

    struct magic {
        int m, p, r;
        ll dis2;
        magic() = default;
        magic(int x, int y, int m, int p, int r): m(m), p(p), r(r), dis2(1ll * (x - x0) * (x - x0) + 1ll * (y - y0) * (y - y0)) {}
    } a[N];

    bool cmp_d(const magic &a, const magic &b) {
        return a.dis2 < b.dis2;
    }

    bool cmp_m(const magic &a, const magic &b) {
        return a.m < b.m;
    }

    int block, cnt;
    int belong[N];
    int L[N], R[N];
    ll mind[N], maxd[N];

    int beg[N];

    void init() {
        sort(a + 1, a + n + 1, cmp_d);
        block = sqrt(n);
        for (int i = 1; i <= n; ++i)
            belong[i] = (i - 1) / block + 1;
        cnt = (n - 1) / block + 1;
        for (int i = 1; i <= cnt; ++i) {
            L[i] = (i - 1) * block + 1;
            R[i] = min(L[i] + block - 1, n);
            beg[i] = L[i];
            mind[i] = a[L[i]].dis2;
            maxd[i] = a[R[i]].dis2;
            sort(a + L[i], a + R[i] + 1, cmp_m);
        }
        R[cnt] = n;
    }

    queue<query> q;

    bool del[N];

    void m_push(const query &u) {
        int p = u.p;
        ll r2 = u.r2;
        for (int j = 1; j <= cnt; ++j) {
            if (mind[j] > r2)
                break;
            if (maxd[j] <= r2) {
                for (int i = beg[j]; i <= R[j]; ++i) {
                    if (del[i]) continue;
                    if (a[i].m > p) break;
                    q.emplace(a[i].p, a[i].r);
                    beg[j] = i + 1;
                }
            }
            else {
                for (int i = beg[j]; i <= R[j]; ++i) {
                    if (del[i]) continue;
                    if (a[i].m > p) continue;
                    if (a[i].dis2 > r2) continue;
                    q.emplace(a[i].p, a[i].r);
                    del[i] = true;
                }
            }
        }
    }

    // -------------------------------------------------------------------------

    int Main() {
        cin >> x0 >> y0 >> p0 >> r0 >> n;
        for (int i = 1; i <= n; ++i) {
            int x, y, m, p, r;
            cin >> x >> y >> m >> p >> r;
            a[i] = magic(x, y, m, p, r);
        }
        init();
        q.emplace(p0, r0);
        int ans = 0;
        while (!q.empty()) {
            auto u = q.front();
            q.pop();
            m_push(u);
            ++ans;
        }
        return ans - 1;
    }
}

// -----------------------------------------------------------------------------

signed main() {
    #ifdef FAST_IO
    ios::sync_with_stdio(false);
    cin.tie(nullptr), cout.tie(nullptr);
    #endif
    cout << solev::Main() << endl;
    return 0;
}
```

END.
