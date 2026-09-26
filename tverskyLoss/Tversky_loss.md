# Tversky Loss

```math
\mathrm{TverskyLoss}
=
1
-
\frac{TP}
{TP + \alpha FP + \beta FN}
```



```math
\alpha = 0.3,\qquad \beta = 0.7
```



```math
\mathrm{TverskyLoss}
=
1
-
\frac{TP}
{TP + 0.3FP + 0.7FN}
```


| lr | pos_weight | epoch数 | Best Dice | Best epoch | Best threshold | Val Loss |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0006 | 10 | 40 | **0.29333** | 39 | **0.92** | 0.76451 |
