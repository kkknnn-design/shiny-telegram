from pathlib import Path
root=Path(__file__).resolve().parents[1]
old=Path('C:/Users/zheng/Documents/Codex/2026-09-24/ge/outputs/C语言学习笔记_2026-10-05更新版_中俄术语.md').read_text(encoding='utf-8')
old=old[old.index('\n## 0.'):]
body=r'''# C 语言程序设计

从控制流、指针到数组排序与中位数

## 导读：先形成内存和执行模型

本册沿用你此前已整理的基础内容，再按先修关系补充：表达式与控制流 → 函数与返回 → 指针与对象 → 数组及边界 → 递归 → 随机数与排序 → 中位数。旧笔记中的复习题保留为阶段检查，新增章节把近期作业完整接起来。

参考 first CC 中 K&R《C 程序设计语言》第二版。重点对照第 2 章类型与表达式、第 3 章控制流、第 4 章函数与程序结构、第 5 章指针与数组；Windows 学习不要求先做 UNIX 系统接口章节。原书以其时代的标准为背景，课堂环境和后来的标准差异需另外说明。

阅读时先说清“对象存什么、表达式类型是什么、当前执行到哪里”，再看输出。不要只凭变量名字猜它是值还是地址。C 统一采用值传递；所谓传地址，是把地址值传给指针形参。
'''+old+r'''

## 27. 数组和指针：同一地址不代表同一类型

设 `int a[4] = {3, 8, 2, 6};`，表达式 `a` 在大多数表达式中转换成首元素指针，类型为 `int *`；`&a[0]` 也指向首元素。`&a` 则是指向整个数组的指针，类型为 `int (*)[4]`。

它们通常显示相同的起始地址，但加 1 的步长不同：首元素指针前进一个整数，整个数组的指针前进整个四元素数组。类型决定指针运算所用的元素单位，不能只看打印出来的数值。

`int *p[4]` 是含四个指针的数组；`int (*p)[4]` 才是指向四元素数组的指针。括号改变声明结构。

```c
int a[4] = {3, 8, 2, 6};
int *p = &a[1];
printf("%d %d\n", p[0], p[1]); // 8 2
```

`p[0]` 与 `*p` 等价；`p[1]` 与 `*(p + 1)` 等价。这里的下标以 p 当前指向的位置为起点，不一定以原数组 a[0] 为起点。

## 28. 三种交换：先分清改了哪一个对象

**交换两个整数值**，需要两个整数对象的地址：

```c
void swap_values(int *pv, int *qv)
{
    int t = pv[0];
    pv[0] = qv[0];
    qv[0] = t;
}
```

调用 `swap_values(&a[0], &a[3]);` 会改变 a 中的值。这正是你要求的 `pv[0]` 写法；它并没有变成“交换地址”。

**交换相邻值**，只传一个起始指针也可以，但必须确认后面还有一个有效元素：

```c
void swap_neighbors(int *pv)
{
    int t = pv[0];
    pv[0] = pv[1];
    pv[1] = t;
}
```

调用 `swap_neighbors(&a[1]);` 交换 a[1] 与 a[2]。不能把 a[3] 的地址传给它并访问 pv[1]，因为那会越界。

**交换指针数组中的地址**，临时变量应是 `int *`：

```c
void swap_addresses(int *p[], int i, int j)
{
    int *temp = p[i];
    p[i] = p[j];
    p[j] = temp;
}
```

这改变 p 的访问顺序，不改变 a 中整数的排列。看函数时不要只看名字 swap，要看赋值号左边究竟是 `p[i]` 还是 `*p[i]`。

## 29. 选择排序：每轮固定一个位置

从大到小排序时，第 i 轮在尚未排列的区间 i…n−1 中找最大值下标，再与第 i 个位置交换。外层循环固定“这一轮排好哪里”，内层循环负责“在剩余部分找谁最大”。

循环不变量：第 i 轮开始前，前 i 个位置已经按降序放好了最大的 i 个值。完成这一轮后，这个性质扩展到 i+1 个位置。这个解释说明算法为何正确，而不仅是解释每行语法。

**小例子。** 3、8、2、6：第 0 轮找到 8，交换后是 8、3、2、6；第 1 轮从 3、2、6 中找 6，得到 8、6、2、3；第 2 轮得到 8、6、3、2。最后一个数自然就位，所以只需 n−1 轮。

下面是用指针数组实现降序访问的完整课堂程序。注释和输出使用英文。随机数缩放沿用课堂公式，它适合演示，不保证 0…1000 每个值严格等概率。

```c
#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int gen_rnd_int(void)
{
    return (int)(((long long)rand() * 1000) / RAND_MAX);
}

void swap_addresses(int *p[], int i, int j)
{
    int *temp = p[i];
    p[i] = p[j];
    p[j] = temp;
}

int main(void)
{
    int a[100];
    int *p[100];
    int i, j, max_index;
    double median;

    srand((unsigned int)time(NULL));
    printf("Original numbers:\n");
    for (i = 0; i < 100; i++) {
        a[i] = gen_rnd_int();
        p[i] = &a[i];
        printf("%d ", a[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }

    // Sort the pointers by the values they refer to
    for (i = 0; i < 99; i++) {
        max_index = i;
        for (j = i + 1; j < 100; j++) {
            if (*p[j] > *p[max_index])
                max_index = j;
        }
        swap_addresses(p, i, max_index);
    }

    printf("Descending order:\n");
    for (i = 0; i < 100; i++) {
        printf("%d ", *p[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
    median = *p[49] / 2.0 + *p[50] / 2.0;
    printf("Median: %.1f\n", median);
    return 0;
}
```

`max_index` 保存位置，不保存最大值本身；比较的是 `*p[j]`，不是两个地址谁更大。`(i+1)%10==0` 表示已经打印的数量是 10 的倍数，此时换行。

如果改成直接交换 a 中的值，比较和交换对象都要一致替换；不要留下指针版的一半逻辑，又混入数值版的一半逻辑。

## 30. 中位数：排序不是唯一方法

对 100 个数，中间两个次序统计量是第 50 小和第 51 小；数组下标从 0 开始，对应 49、50。平均值可能为半整数，因此用 double。

不排序时，对每一个候选值 v 统计：L 个数严格小于 v，E 个数等于 v。v 在升序中的位置覆盖 L+1…L+E，因此它是第 k 小的充要条件为：

\[
\boxed{L<k\leq L+E}.
\]

这个区间能正确处理重复值。例如 2、2、2、9，候选值 2 的 L=0、E=3，所以第 1、2、3 小都等于 2。不要只统计小于数而忽略重复数。

完整的不排序程序如下，它保留原数组：

```c
#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    int a[100];
    int i, j, less, equal;
    int x = 0, y = 0;
    double median;

    srand((unsigned int)time(NULL));
    printf("Original numbers:\n");
    for (i = 0; i < 100; i++) {
        a[i] = (int)(((long long)rand() * 1000) / RAND_MAX);
        printf("%d ", a[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }

    // Find ranks 50 and 51 without sorting
    for (i = 0; i < 100; i++) {
        less = 0;
        equal = 0;
        for (j = 0; j < 100; j++) {
            if (a[j] < a[i])
                less++;
            else if (a[j] == a[i])
                equal++;
        }
        if (less < 50 && less + equal >= 50)
            x = a[i];
        if (less < 51 && less + equal >= 51)
            y = a[i];
    }
    median = x / 2.0 + y / 2.0;
    printf("Median: %.1f\n", median);
    return 0;
}
```

“为什么 x、y 都等于 a[i]？”因为每一轮的 i 不同，而且两个 if 的条件不同。某个候选值可能只覆盖第 50 小，另一个覆盖第 51 小；若两个位置恰好落在同一重复值区间，也可以得到相同的 x、y。

这个算法时间复杂度为 O(n²)，适合当前知识范围；不排序并不自动意味着比排序快。更高效的选择算法可以以后再学。

## 31. 浮点数、整数与地址

浮点数通常不能精确表示所有十进制小数，例如 1/3。比较近似计算结果时，应根据问题尺度选择绝对或相对容差，而不是把一个固定 0.0001 当成适合所有问题的规则。

```c
#include <math.h>
int close_enough(double a, double b,
                 double abs_tol, double rel_tol)
{
    return fabs(a - b) <= abs_tol + rel_tol * fmax(fabs(a), fabs(b));
}
```

这是有限普通数值的课堂示例，未把 NaN 和无穷的完整策略纳入。`fabs` 接受浮点数；整数绝对值与浮点绝对值函数不是同一个接口。

地址用 `%p` 配 `(void *)p` 输出。不要把地址保存进 int 并假定不会截断。`uintptr_t` 是可选的无符号整数类型，若实现提供它，可用于相应指针与整数转换；它的存在也不使任意整数地址成为可安全访问的对象。

## 32. 新增练习与答案

1. a={3,8,2,6}，调用 swap_neighbors(&a[1]) 后是什么？答：3、2、8、6。
2. 指针数组排好序后，原 a 会自动排序吗？答：不会，只改变通过 p 访问的顺序。
3. 四个数 1、2、2、9 的中位数？答：2。第 2、3 小都在相同重复值区间。
4. a[100] 是否是数组 a[100] 中最后一个元素？答：不是，最后有效元素是 a[99]。
5. main(void) 能否使用 scanf 输入两个整数？答：可以；函数参数与运行中的标准输入不同。也不能由此误推 main 永远不能接命令行参数，标准还允许带 argc、argv 的常见形式。

## 33. 本版增补与教材对照

本版在此前笔记基础上补入近期的数组下标、相邻交换、两地址交换、指针数组排序、选择排序逐轮逻辑、不排序中位数、浮点容差与地址类型。参照 K&R 的类型、表达式、控制流、函数、指针与数组章节重新梳理；旧版提到的读取日期保留为历史来源记录，不作为本次完整性声明。

旧回答中“main 没有上层所以不能有参数”“只用 goto 无法完成进制转换”“数组参数就不涉及指针”等说法均不能作为通则。教材应以函数接口、对象类型、生命周期和合法边界解释问题。
'''
import re
prefix=body[:body.index('\n## 0.')]
sections={}
for m in re.finditer(r'\n## (\d+)\.([^\n]*)\n([\s\S]*?)(?=\n## \d+\.|\Z)',body):
 sections[int(m[1])]=(m[2].strip(),m[3])
order=[0,1,2,3,4,5,11,19,12,6,7,8,9,27,15,16,14,31,10,28,17,13,18,29,30,20,21,22,23,24,32,25,26,33]
chunks=[]
for n,i in enumerate(order):
 title,content=sections[i]
 content=content.replace('第 14—18 章','const、边界、交换和排序相关章节')
 content=re.sub(r'第\s*(\d+)\s*章',lambda m:'第 '+str(order.index(int(m[1]))+1)+' 章' if int(m[1]) in order else m[0],content)
 content=content.replace('上周对话主题','学习中的问题').replace('上周问题对应的核心代码','对话问题对应的核心代码').replace('### 本周速记增补','### 重点速记补充')
 chunks.append('\n## '+str(n+1)+'. '+title+'\n'+content)
body=prefix+'\n'+''.join(chunks)
body=body.replace('旧笔记中的复习题保留为阶段检查，新增章节把近期作业完整接起来。','近期的排序与中位数已归入数组、指针和随机数之后；复习题、速记和来源说明统一放在全册末尾。')
(root/'outputs/教材/01_C语言程序设计.md').write_text(body,encoding='utf-8')
print(len(body))
