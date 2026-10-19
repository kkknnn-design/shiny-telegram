## 18. 字符串：从字符数组到复制与容量

本章根据 2026-10-15《解释数组指针关系》中的课堂讲解补入。阅读顺序是：字符如何存放 → 结束符 → 可修改性 → 指针数组 → 长度与容量 → 字符串复制。先修内容是数组、指针和 const。

### 字符、字符数组和字符串

`char` 保存字符编码。ASCII 环境下，`'A'` 的值为十进制 65、十六进制 41；这三个写法表达同一个数值。输出格式决定显示方式，不能由此认为所有 C 实现都必须使用 ASCII。

```c
char ch = 'A';
printf("%c %d %x\n", ch, (int)ch, (unsigned int)(unsigned char)ch);
/* ASCII 环境：A 65 41 */
```

`%c` 输出一个字符，`%s` 从给定地址读取字符直到第一个零字符。`'\0'` 是数值为零的字符；`'0'` 是数字零的字符，两者不同。`'\n'` 是一个换行字符，虽然代码中用两个可见符号书写，但只占一个 char 元素。

```c
char a[] = "ABC";                 // 4 元素，末尾有 '\0'
char b[] = {'A', 'B', 'C'};       // 3 元素，没有结束符
char c[] = {'A', 'B', 'C', '\0'}; // 4 元素，是字符串
char d[3] = "ABC";               // C 中合法，但没有 '\0'
char e[10] = {'A', 'B', 'C'};     // 其余元素补零，是字符串
char Mes[] = {'\n', 'A', 'B', 'C', 'D', '\0'};
```

你问“既然 C 会补充 \0，为什么还要自己写”：自动补零有具体条件。字符串字面量自带结束符，但定长字符数组恰好只能容纳普通字符时可以省去它；逐项初始化时，未显式给值的剩余数组元素补零，完全填满的数组不会额外增加一个元素。因此 b 和 d 不能交给 `%s` 或 strlen；它们仍然是合法字符数组，却不是零结尾字符串。

`Mes` 与 `char Mes[] = "\nABCD";` 的内容相同。输出时使用 `printf("%s", Mes);`，不要把可变内容直接放在格式参数位置；否则内容中的 `%` 会被解释成格式说明。

### 数组可以改，字符串字面量不能改

```c
char str1[10] = "ABC";
char str2[] = "DEF";
const char *str3 = "GHI";

str1[1] = '_';
str2[1] = '_';
/* str3[1] = '_'; 约束违反，编译器须给出诊断 */
printf("%s %s %s\n", str1, str2, str3);
/* A_C D_F GHI */
```

str1 和 str2 自己拥有可写字符存储；str3 是保存地址的指针。const 禁止通过它写字符。即使写成 `char *p = "GHI";`，也不能修改字面量：尝试写入会产生未定义行为。指针能否改指向，与所指字符能否修改，是两个问题。

### 字符串指针数组与双下标

```c
char *sarr[] = {str1, str2};
const char *sarr2[] = {str1, str2, str3, "banana"};
printf("%s %s\n", sarr[1], sarr2[3]); // D_F banana
printf("%c\n", sarr[1][2]);          // F
sarr2[0] = "hello";                 // 可以改保存的地址
/* sarr2[0][0] = 'X'; 不允许通过 const char * 写字符 */
```

sarr 是数组，每个元素为 char 指针。`sarr[1]` 取第二个指针；`sarr[1][2]` 再取该指针指向位置之后的第三个字符，等价于 `*(*(sarr + 1) + 2)`。它不同于 `char (*p)[5]`：后者是一个指向五元素字符数组的指针。

### strlen 看内容，sizeof 看对象

strlen 声明在 `<string.h>`，返回第一个结束符之前的字节数，不包含结束符。它要求输入已经是有效字符串，不能用它先判断一个无结束符数组是否安全。sizeof 是运算符，计算对象或类型的字节大小。

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char str1[10] = "ABC";
    char str2[] = "DEF";
    char Mes[] = "\nABCD";
    printf("%zu %zu %zu\n", strlen(str1), strlen(str2), strlen(Mes));
    printf("%zu %zu %zu\n", sizeof str1, sizeof str2, sizeof Mes);
    // 两行分别为：3 3 5 和 10 4 6
    str1[1] = '\0';
    printf("%zu %zu\n", strlen(str1), sizeof str1); // 1 10
    return 0;
}
```

两者结果类型都是 size_t，输出用 `%zu`。对 `const char *p = "GHI";`，`strlen(p)` 为 3，`sizeof p` 是指针自身大小，不能推断为 4，也不能据此获得目标容量。函数参数中的数组声明会调整为指针，同样不能在函数内用 sizeof 参数求原数组容量。

课堂中的 `ls` 是小写字母 l 和 s，不是数字 1 加 s，也不是关键字。它只是长度变量，规范写法为 `size_t ls = strlen(str2);`。中文等多字节编码下，strlen 计算字节数，不等同于人所理解的汉字个数。

### strcpy：复制结束符，不检查容量

`strcpy(dst, src)` 从源复制到目标，包含结束符。前提是源为有效字符串、目标可写且容量至少为 `strlen(src) + 1`，源目标区域不能重叠。

```c
char dst[10] = "ABC";
char src[] = "D_F";
strcpy(dst, src);
printf("%s\n", dst); // D_F
```

实际写入 D、_、F、零字符，共四个字节。数组剩余位置不会被该函数自动清零。不能写 `dst = src` 给整个数组赋值；若两边都是指针，赋值只是改变地址，也不会复制字符串。

### strncpy：写满指定数量不代表得到字符串

`strncpy(dst, src, n)` 最多从源取 n 个字符；若先遇结束符，则用零填满目标的这 n 个位置。若源的前 n 个字符都不是零，目标不会自动追加结束符。目标必须有至少 n 个可写位置，区域仍不得重叠。

```c
char dst[10] = "ABCDEFG";
char src[] = "DEF";
size_t ls = strlen(src); // 3
strncpy(dst, src, ls);
printf("%s\n", dst);   // DEFDEFG：旧尾部仍在
dst[ls] = '\0';
printf("%s\n", dst);   // DEF
```

这里手工补零合法，因为 ls 小于目标容量；不能在任意长度下照抄。给源数组 `src[ls]` 写零不会替目标补结束符。课堂照片中若末行辨认为源数组，应结合目标核查，不能把模糊笔迹当作确定原代码。

下面例子先检查容量，再完整复制；空间不足时保留原目标，不进行截断：

```c
size_t ls = strlen(src);
if (ls < sizeof dst) { // 这里 dst 必须确实是数组对象
    strcpy(dst, src);
} else {
    puts("destination too small");
}
```

### strcpy_s、strncpy_s 与微软扩展

在支持相应接口的环境中，`strcpy_s(dst, capacity, src)` 有三个参数；微软的 `strncpy_s(dst, capacity, src, count)` 有四个。两者不能仅凭照片中的模糊函数名混为一谈。`_countof(array)` 是微软提供的数组元素个数宏，不是通用标准 C 写法，不能用指针推算原数组容量。

```c
/* 以下为 Microsoft CRT 环境示例 */
char dst[10] = "ABC";
errno_t err = strcpy_s(dst, _countof(dst), "DEF");
if (err != 0) {
    /* 按项目要求处理复制失败 */
}
```

容量必须如实描述目标可写范围，并为结束符留位置。微软 CRT 某些参数错误会先触发无效参数处理器，默认行为可能终止程序，不能假定任何错误都会正常返回到 if。标准 C 的 Annex K 接口是可选部分，可用性和配置因实现而异；跨平台示例优先明确管理容量，不能假设所有编译器都提供上述函数。

### 练习：把长度、容量和结束符分开检查

1. `char a[5] = "ABCD";` 的 strlen 与 sizeof 各是多少？若改成 `char a[4] = "ABCD";`，能否继续调用 strlen？
2. `char a[8] = "ABCDEFG"; strncpy(a, "XY", 2);` 后字符串是什么？如何得到仅含 XY 的字符串？
3. `const char *names[] = {"one", "two"};` 中 `names[0] = "three"` 与 `names[0][0] = 'T'` 哪个合法？
4. `char a[10] = {'A', 'B', 'C'};` 没有显式写结束符，为什么仍可用于 `%s`？

答案：1. 分别为 4 和 5；改为四元素后没有结束符，不能调用 strlen。2. 为 XYCDEFG；容量足够时令 `a[2] = '\0';`。3. 前者合法，后者违反 const 限制。4. 部分初始化使剩余元素补零，a[3] 已是结束符。

