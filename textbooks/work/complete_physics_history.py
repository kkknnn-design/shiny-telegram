from pathlib import Path
p=Path('outputs/教材/05_大学物理.md');s=p.read_text(encoding='utf-8')
a=r'''外场模型还涉及研究对象的缩小。设封闭系统由 \(A,B\) 两部分组成，\(L=T_A+T_B-U(q_A,q_B)\)。若 \(B\) 的运动被当作已知函数 \(q_B(t)\)，只研究 \(A\)，则相互作用变成 \(U(q_A,t)\)，而 \(T_B\) 只是已知的时间函数，不含正在变分的 \(q_A,\dot q_A\)，不会进入 \(A\) 的欧拉—拉格朗日方程。因此可写 \(L_A=T_A-U(q_A,t)\)。这里不是说外部装置没有能量，而是其能量不参与当前待求坐标的变分；装置若需由未知反馈共同决定，就不能擅自把它当作已知外场。

双摆使动能交叉项的几何来源更加明确。固定悬点，杆长 \(l_1,l_2\)，两角均从竖直向下量起，向上为纵轴正向。第一球位置是 \((l_1\sin\varphi_1,-l_1\cos\varphi_1)\)，第二球位置为它再加 \((l_2\sin\varphi_2,-l_2\cos\varphi_2)\)。第二球的速度平方展开后，交叉系数含 \(\cos\varphi_1\cos\varphi_2+\sin\varphi_1\sin\varphi_2\)，即两相对速度方向夹角的余弦。于是

\[
L=\frac12(m_1+m_2)l_1^2\dot\varphi_1^2+
\frac12m_2l_2^2\dot\varphi_2^2+
m_2l_1l_2\cos(\varphi_1-\varphi_2)\dot\varphi_1\dot\varphi_2
+(m_1+m_2)gl_1\cos\varphi_1+m_2gl_2\cos\varphi_2.
\]

若两杆瞬时平行，余弦为一，交叉项最大；若两相对速度垂直，余弦为零。独立角坐标不保证速度方向垂直，所以不能以“两个自由度不同”为由删掉交叉项。令 \(\Delta=\varphi_1-\varphi_2\)，求导后得到完整运动方程：

\[
(m_1+m_2)l_1^2\ddot\varphi_1+m_2l_1l_2\cos\Delta\,\ddot\varphi_2
+m_2l_1l_2\sin\Delta\,\dot\varphi_2^2+(m_1+m_2)gl_1\sin\varphi_1=0,
\]

\[
m_2l_2^2\ddot\varphi_2+m_2l_1l_2\cos\Delta\,\ddot\varphi_1
-m_2l_1l_2\sin\Delta\,\dot\varphi_1^2+m_2gl_2\sin\varphi_2=0.
\]

对运动悬点，可直接展示全导数怎样化简。设悬点的已知坐标为 \(x_0(t),y_0(t)\)，摆球坐标为 \(x=x_0+l\sin\varphi\)、\(y=y_0-l\cos\varphi\)。展开动能，依赖角速度的交叉项是

\[
ml\dot\varphi(\dot x_0\cos\varphi+\dot y_0\sin\varphi)
=\frac d{dt}[ml(\dot x_0\sin\varphi-\dot y_0\cos\varphi)]
-ml\ddot x_0\sin\varphi+ml\ddot y_0\cos\varphi.
\]

丢去纯时间项和这个明确写出的全导数后，有等价的

\[
L_{eq}=\frac12ml^2\dot\varphi^2-ml\ddot x_0\sin\varphi
+ml\ddot y_0\cos\varphi+mgl\cos\varphi.
\]

因此运动方程是 \(l\ddot\varphi+\ddot x_0\cos\varphi+(g+\ddot y_0)\sin\varphi=0\)。水平振动 \(x_0=a\cos\gamma t,y_0=0\) 时，约化拉格朗日量多出 \(mla\gamma^2\cos\gamma t\sin\varphi\)；竖直振动 \(y_0=a\cos\gamma t\) 时，则多出 \(-mla\gamma^2\cos\gamma t\cos\varphi\)。这里纵轴向上；若教材的悬点坐标向下为正，相应的竖直项符号会改变，不能只对照末式正负判断谁对谁错。

再取 \(x_0=a\cos\gamma t,y_0=a\sin\gamma t\)，悬点沿竖直圆周运动，组合项为 \(mla\gamma^2\sin(\varphi-\gamma t)\)。这说明交叉速度项化成外部加速度项后并没有丢失外部驱动，反而更清楚地显示哪种悬点加速度促使摆动。

还有一类系统既绕轴转动又改变形状。明确规定一个理想机构：顶点固定，两侧各有质量 \(m_1\)，距竖直轴 \(a\sin\theta\)、高度 \(-a\cos\theta\)；下端质量 \(m_2\) 在轴上，高度 \(-2a\cos\theta\)；两侧方位角按已知 \(\Omega t\) 转动，杆质量忽略。这些几何关系就是模型定义，不依赖缺失原图。

每个侧球的形变速度大小为 \(a\dot\theta\)，绕轴速度为 \(a\Omega\sin\theta\)，两者垂直，故速度平方相加。下球无绕轴速度，竖直速度为 \(2a\sin\theta\dot\theta\)。总拉格朗日量为

\[
L=a^2(m_1+2m_2\sin^2\theta)\dot\theta^2
+m_1a^2\Omega^2\sin^2\theta+2ag(m_1+m_2)\cos\theta.
\]

旋转项来自真实的切向速度，不是凭空增加一个能量。在形状恒定的非零角平衡下，\(\partial L/\partial\theta=0\)，得到 \(\cos\theta=g(m_1+m_2)/(m_1a\Omega^2)\)，还需右端不超过一、几何约束允许该角度。因 \(\Omega\) 由外部装置维持，装置可交换能量，不能把约化系统的普通机械能直接宣称为封闭系统守恒量。

'''
s=s.replace('## 13. 热学与相对论的课程衔接',a+'## 13. 热学与相对论的课程衔接');p.write_text(s,encoding='utf-8')
