from pathlib import Path
p=Path('outputs/教材/05_大学物理.md');s=p.read_text(encoding='utf-8')
a=r'''矢量式也可从有限小转角的极限建立。设固定轴方向不变，时间 \(\Delta t\) 内的转角矢量为 \(\Delta\boldsymbol\varphi\)，则旋转的几何展开是

\[
\Delta\mathbf r=\Delta\boldsymbol\varphi\times\mathbf r(t)
+O(|\Delta\boldsymbol\varphi|^2).
\]

若角速度有限，\(\Delta\boldsymbol\varphi=\boldsymbol\omega\Delta t+O(\Delta t^2)\)。两边除以 \(\Delta t\) 并取极限，二阶项变为随 \(\Delta t\) 消失的量，得到 \(\mathbf v=\boldsymbol\omega\times\mathbf r\)。不要把含微分的几何关系当作普通有限函数乘积，再形式化地制造一个没有清楚极限意义的附加项。能略去的是除以时间后仍趋零的高阶增量，而不是所有含微小符号的项。

对已经得到的有限量关系求时间导数，乘法法则必须完整保留：

\[
\mathbf a=\boldsymbol\alpha\times\mathbf r+
\boldsymbol\omega\times\mathbf v
=\boldsymbol\alpha\times\mathbf r+
\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r).
\]

第二项并不消失，它给出向轴的法向加速度。由微小增量求极限，与对速度公式求导，是两种运算阶段；若把前一阶段省略高阶项的理由套到后一阶段，就会把真正的向心加速度错误删掉。

'''
s=s.replace('对连续刚体，把所有质量元的动能相加：',a+'对连续刚体，把所有质量元的动能相加：');p.write_text(s,encoding='utf-8')
