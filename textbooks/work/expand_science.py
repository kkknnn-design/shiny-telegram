from pathlib import Path
p=Path('outputs/教材/05_大学物理.md');s=p.read_text(encoding='utf-8-sig')
a=r'''单位向量长度不变，并不意味着它的导数为零。由 \(\mathbf e_\tau\cdot\mathbf e_\tau=1\) 求导，只能得到 \(\mathbf e_\tau\cdot d\mathbf e_\tau/ds=0\)，所以导数垂直原切线。沿轨迹走过弧长 \(ds\)，切线转过 \(d\psi\)，曲率定义给出 \(d\psi=ds/R\)。两个相邻单位切向量的差的大小在极限下为 \(d\psi\)，方向朝向曲率中心，因此

\[
\frac{d\mathbf e_\tau}{ds}=\frac1R\mathbf e_n,
\qquad \frac{d\mathbf e_\tau}{dt}=\frac vR\mathbf e_n.
\]

这不是把切向量直接换成法向量，而是在求切向量的变化率。乘法法则中的第二项没有被删去，它正是法向加速度的来源。只有直线运动、基向量在所用参考系中固定等具体条件，才有相应方向导数为零。

对平面极坐标，也能把这一问题看得更清楚。位置写成 \(\mathbf r=r\mathbf e_r\)，径向和切向基随角度一起旋转，故 \(\dot{\mathbf e}_r=\dot\theta\mathbf e_\theta\)、\(\dot{\mathbf e}_\theta=-\dot\theta\mathbf e_r\)。连续用乘法法则可得

\[
\mathbf v=\dot r\mathbf e_r+r\dot\theta\mathbf e_\theta,
\qquad
\mathbf a=(\ddot r-r\dot\theta^2)\mathbf e_r
+(r\ddot\theta+2\dot r\dot\theta)\mathbf e_\theta.
\]

圆周运动半径固定时，才令 \(\dot r=\ddot r=0\)。若先把一般曲线运动的径向速度删掉，再称之为“圆周公式的推导”，就把约束条件藏到了运算之中。极坐标径向单位向量朝外，而圆周运动的法向单位向量朝内，所以两种写法的径向符号相反，实际加速度方向相同。

'''
s=s.replace('对于受约束系统，', '对于受约束系统，',1)
s=s.replace('例如质量 \\(m\\)', '例如质量 \\(m\\)') if False else s
mark='例如质量 \\(m\\)'
pos=s.index('例如质量')
s=s[:pos]+a+s[pos:]
b=r'''角动量不沿转轴的情形，可用两个质点明确算出，而不依赖图的倾斜印象。设两个相同质量 \(m\) 的质点在刚性杆上，其位置分别为 \((a,0,b)\) 与 \((-a,0,-b)\)，整体绕固定 \(z\) 轴以角速度 \(\omega\) 转动。在所取瞬间，两点速度为 \((0,\omega a,0)\) 和 \((0,-\omega a,0)\)。逐一作叉乘并相加，得到

\[
\mathbf L=(-2mab\omega,0,2ma^2\omega).
\]

只要 \(a,b\) 均非零，就有横向分量，所以总角动量不平行于 \(z\) 轴。另一方面轴向分量仍满足 \(L_z=I_z\omega\)，其中 \(I_z=2ma^2\)。标量轴向公式正确，与完整矢量不平行完全可以同时成立。维持这样的定轴转动，轴承一般还需提供改变角动量方向的力矩；没有轴向加速，不代表全部外力矩都为零。

'''
s=s.replace('若 \\(I=0.20', '若 \\(I=0.20') if False else s
pos=s.index('若 \\(I=0.20') if '若 \\(I=0.20' in s else s.index('若 \(I=0.20')
s=s[:pos]+b+s[pos:]
c=r'''变分与时间微分有不同含义。\(\dot q\) 是同一条轨迹沿时间的变化率，\(\delta q\) 是在同一时刻比较两条邻近候选轨迹的差。设 \(q_\varepsilon=q+\varepsilon\eta(t)\)，其中 \(\eta(t_1)=\eta(t_2)=0\)。对参数 \(\varepsilon\) 求导并在零处取值：

\[
\delta S=\int_{t_1}^{t_2}\left(L_q\eta+L_{\dot q}\dot\eta\right)dt
=\left[L_{\dot q}\eta\right]_{t_1}^{t_2}
+\int_{t_1}^{t_2}\left(L_q-\frac d{dt}L_{\dot q}\right)\eta\,dt.
\]

边界项为零，是因为端点构型固定，绝不是因为端点的速度必须为零。端点处的 \(L_{\dot q}\) 可以非零。由于区间内部的 \(\eta\) 可以自由选择，积分对所有这种变化都为零，才推出欧拉—拉格朗日方程。这个论证说明，边界条件与中间的积分运算共同决定结果，不能把“积分等于零”一般地理解为被积函数逐点为零。

以单摆为例，\(T=ml^2\dot\theta^2/2\)、\(U=mgl(1-\cos\theta)\)。对角速度求偏导先得到 \(ml^2\dot\theta\)，再作时间导数得到 \(ml^2\ddot\theta\)；对角度求偏导得到 \(-mgl\sin\theta\)，因此精确方程是 \(ml^2\ddot\theta+mgl\sin\theta=0\)。这里求偏导时把 \(\theta\) 与 \(\dot\theta\) 视为拉格朗日函数的独立自变量，最后再代回真实轨迹；这与它们沿轨迹由时间导数联系并不冲突。

对理想约束做了坐标消元，约束力常不必显式出现，但不表示约束力不存在。若还要求绳张力，应在求得运动后返回牛顿径向方程；若消元的约束可能失效，例如细绳松弛，应检查约束力是否满足其物理限制，并在必要时改换模型。分析力学的简洁并不免除对模型边界的判断。

'''
s=s.replace('## 13. 热学与相对论的课程衔接',c+'## 13. 热学与相对论的课程衔接')
p.write_text(s,encoding='utf-8')
