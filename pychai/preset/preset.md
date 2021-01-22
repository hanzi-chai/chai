# 预设（`pychai.preset`）

## 预设域（`preset.field`）

退化映射是一种非常重要的看法，它能够将每一个具体的字中的切片转化为抽象的切片，也即在不同字中有微小形变的切片 $p,p', p''\cdots$ 在输入方案的角度来看可以看作是一个字根 $r$。

### 笔画归类与排序（`preset.field.featureList`）

在 31 种笔画中，有一些笔画从字源上讲是同源的，出于不违反人们的文字习惯考虑，我们可能会将几种不同的笔画归为一个**笔画类**，例如竖钩和竖可能归为一类。给定一种分类方法，对于笔画 $b$ 来说，我们记它所属的类为 $\operatorname{cat}(b)$。所有笔画类构成一个集合 $X$。

我们现在可以定义一种最简单的退化映射。记切片或字根 $p$ 的笔画序列为 $\operatorname{str}(p)=(b_1,\cdots,b_n)$，则这个映射可以表示为


$$
\mathcal O:p\to X^n
$$


$$
\mathcal O(p)=(\operatorname{cat}(b_1),\cdots,\operatorname{cat}(b_n))
$$

**实例** 假设我们只分横竖撇点折五类，$X=\{1,2,3,4,5\}$，设 $p_1$ 是由「土」的全部笔画构成的切片，$p_2$ 是由「工」的全部笔画构成的切片，则


$$
\mathcal O(p_1)=\mathcal O(p_2)=(1,2,1)
$$

### 笔画关系（`preset.field.topologyList`）

显然，这种分类是非常粗糙的，我们还需要加入更多信息。我们可以定义一个**关系映射**，将两个笔画映射到它们之间的关系：

$$
\mathcal R:B^2\to R
$$

这样我们就可以定义更好一点的退化映射：


$$
\mathcal O:P\to X^{n}\times R^{n^2}
$$


$$
\mathcal O(p)=\left[(\operatorname{cat}(b_1),\cdots,\operatorname{cat}(b_n)),(\mathcal R(b_1,b_1),\cdots,\mathcal R(b_n,b_n))\right]
$$

**实例** 我们记「散（$\odot$）、连（$\oplus$）、交（$\otimes$）」是三种关系，并且笔画和自己没有关系、两个笔画的关系是相互的。则上述的 $p_1,p_2$ 会变为


$$
\mathcal O(p_1)=[(1,2,1),(1\otimes2,1\odot3,2\oplus3)]
$$

$$
\mathcal O(p_2)=[(1,2,1),(1\oplus2,1\odot3,2\oplus3)]
$$

可见我们实现了区分。

### 笔画长度（未实现）

不过，我们还是区分不开「土」和「士」。为此我们可以给所有同类笔画定义笔画长度序，用 ABCD 标记。然后记「士」为 $p_3$，则我们大致可以写成


$$
\mathcal O(p_1)=\rm[(1B,2A,1A),(1\otimes2,1\odot3,2\oplus3)]
$$

$$
\mathcal O(p_3)=\rm[(1A,2A,1B),(1\otimes2,1\odot3,2\oplus3)]
$$

## 预设筛（`preset.sieve`）

### 取大筛（`preset.sieve.bias`）

回顾一下择优函数的定义：将可行拆分集 $W$ 单射到实数集 $\mathbb R$。我们首先将一个字的笔画数计为 $L$，则任何一个字根不可能有 $L+1$ 个笔画。那么我们定义

$$
\mathcal H(d)=\sum_{i=1}^k\operatorname{len}(p_i)(L+1)^{-i}
$$

就实现了「取大优先」。

### 字根关系筛（`preset.sieve.topology`）

我们可以基于笔画关系定义字根关系。如果两个字根间有笔画相交，则为交；不交但有笔画为连，则为连；其余为散。这样定义出来的映射记为 $\tilde{\mathcal R}(r_1,r_2)$，然后定义发生交、连、散的次数分别为 $u_1,u_2,u_3$。字根数量不可能超过 $L$，所以我们定义


$$
\mathcal H(d)=u_1(L+1)^2+u_2(L+1)+u_3+\sum_{i=1}^k\operatorname{len}(p_i)(L+1)^{-i}
$$

这样，我们就能把「天」拆成「一大」，把「夫」拆成「二人」。

### 字根数量筛（`preset.sieve.length`）

例如在有笔顺限制的情况下把「区」拆成「匚乂」，如果我们定义 $\operatorname{len}(d)$ 为其中含字根的个数，那么我们设法把 $\operatorname{len}(d)$ 加入 $\mathcal H$ 中即可。
