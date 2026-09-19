


# 主指標：Normalized MAE

$$
\mathrm{Score}
=
\frac{1}{3}
\left(
\frac{\mathrm{MAE}_{PA}}{6}
+
\frac{\mathrm{MAE}_{FL}}{12}
+
\frac{\mathrm{MAE}_{MT}}{3}
\right)
$$

- PA の許容値：6 deg
- FL の許容値：12 mm
- MT の許容値：3 mm
- 小さいほど良い


# 副指標：予測失敗率

$$
\mathrm{Failure\ Rate}
=
\frac{\mathrm{Failed\ Images}}
{\mathrm{Total\ Images}}
$$

予測失敗の例：

- PA が NaN
- FL が NaN
- MT が NaN
- apo が正常に抽出できない
- fascicle line が抽出できない