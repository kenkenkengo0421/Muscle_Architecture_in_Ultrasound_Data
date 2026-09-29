# UMUDチャレンジ：超音波データによる筋肉構造の解析

[公式：umud-challenge-muscle-architecture-in-ultrasound-data](https://www.kaggle.com/competitions/umud-challenge-muscle-architecture-in-ultrasound-data)

# 課題概要

このコンテストの目的は、超音波画像から3つの主要な筋肉構造変数を正確に推定できるアルゴリズムを構築することです。


テストデータセット内の各超音波画像について、これら3つの値を予測する必要があります。
[提出されたデータは、 UMUDスコアという](https://www.kaggle.com/code/paulritsche/umud-score)複合指標を用いてランク付けされます。この指標は、3つの変数すべてにおける予測精度を評価するものです。


# リポジトリ内の主なファイル、ノートブック

| 名称      | ファイル名  | 備考     |
| ---------- | ---- | ------ |
|データの確認 | [study.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/study.ipynb) | |
|apoセグメンテーション(UNet)|[apo_model.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/apo_model.ipynb)||
|fascセグメンテーション(UNet)|[fasc_model.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/fasc_model.ipynb)||
|fascセグメンテーション(DeepLabV3+)|[DeepLabV3+_fasc_model.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/DeepLabV3+_fasc_model.ipynb)||
|fascセグメンテーション(FPN)|[FPN_fasc_model.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/FPN_fasc_model.ipynb)||
|fascアンサンブル検証(UNet + DeepLabV3+)|[UNet_DeepLab_fasc_ensemble.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/UNet_DeepLab_fasc_ensemble.ipynb)||
|fascアンサンブル検証(UNet + FPN)|[UNet_FPN_fasc_ensemble.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/UNet_FPN_fasc_ensemble.ipynb)||
|fascアンサンブル検証(UNet + DeepLabV3+ + FPN)|[UNet_Deep_FPN_fasc_ensemble.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/UNet_Deep_FPN_fasc_ensemble.ipynb)||
|予測と提出|[best_submission_of_predict_ensemble_fasc.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/best_submission_of_predict_ensemble_fasc.ipynb)||
|予測と提出(テスト中)|[test_submission_of_predict_ensemble_fasc.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/test_submission_of_predict_ensemble_fasc.ipynb)||

# 評価指標

提出された提案は、3つのアーキテクチャ変数すべてにおける予測誤差を測定するUMUDスコアを使用して評価されます。

このスコアは、以下の項目における
正規化された平均絶対誤差（MAE)に基づいています。

![alt用テキスト](img/img.png)


```
羽状角(Pennation Angle)（PA）：筋束と腱膜の間の角度（度）黄色
    
筋束長(Fascicle Length)（FL）：筋束の長さ（ミリメートル）（緑色）
    
筋厚(Muscle Thickness)（MT）：表層腱膜と深層腱膜間の距離（ミリメートル）（ピンク色）
```



各変数の誤差は、異なる単位や尺度であっても比較可能な影響を確保するために、あらかじめ定義された許容値によって正規化されます。スコアが低いほど、パフォーマンスが優れていることを示します。



# モデルの指標

## 主指標：Validation Dice

予測maskと正解maskの一致度を評価する。

```math
\mathrm{Dice}
=
\frac{2TP}
{2TP + FP + FN}
```

- `TP`：正解maskが1で、予測maskも1だった画素
- `FP`：正解maskは0だが、予測maskを1とした画素
- `FN`：正解maskは1だが、予測maskを0とした画素
- apo / fasc それぞれで確認する
- 大きいほど良い
- モデル保存時の主な判断基準とする


## 副指標：Validation Loss

学習時の予測誤差を確認する。


```math
\mathrm{Loss}
=
\mathrm{BCEWithLogitsLoss}
+
\mathrm{DiceLoss}
```


### BCEWithLogitsLoss


```math
\mathrm{BCE}
=
-\left[
w \, y \log(p)
+
(1-y)\log(1-p)
\right]
```

- `y`：正解maskの値（0 または 1）
- `p`：モデルが予測した確率
- `w`：正例に対する重み（pos_weight）


### DiceLoss

```math
\mathrm{DiceLoss}
=
1
-
\frac{2\sum (p \cdot y)}
{\sum p + \sum y}
```

- 小さいほど良い
- 学習状態の確認用として使用する
- Validation Diceと合わせて確認する


## 最終評価：Kaggle Public Score

モデル完成後、submissionを作成してKaggle上で確認する。

```math
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
```

- PA の許容値：6 deg
- FL の許容値：12 mm
- MT の許容値：3 mm
- 小さいほど良い
- ローカルでは正解 PA / FL / MT が存在しないため、直接計算しない


# モデルの検証結果


## apo検証(UNet)

<details><summary></summary>

* 副指標：Validation Loss検証

| lr | pos_weight | epoch数 | Best Dice | Best epoch | Best threshold | Val Loss |
|---:|---:|---:|---:|---:|---:|---:|
| 0.001 | 1.5 | 20 | 0.73735 | 19 | 0.18 | 0.35728 |
| 0.0005 | 1.5 | 20 | 0.79126 | 19 | 0.20 | 0.28659 |
| 0.0005 | 1.5 | 40 | 0.80430 | 35 | 0.12 | 0.26615 |

</details>

## fasc検証(UNet)


<details><summary></summary>

* 副指標：Validation Loss検証

|     lr | pos_weight | epoch数 |   Best Dice | Best epoch | Best threshold |    Val Loss |
| -----: | ---------: | -----: | ----------: | ---------: | -------------: | ----------: |
|  0.001 |          8 |     10 |     0.20236 |          9 |           0.52 |     0.92495 |
|  0.001 |         10 |     10 |     0.20324 |         10 |           0.52 |     0.94580 |
|  0.001 |         12 |     10 |     0.18640 |          6 |           0.70 |     0.98159 |
|  0.001 |         15 |     10 |     0.20263 |         10 |           0.62 |     0.98624 |
| 0.0005 |         10 |     20 | 　0.26756 |     20 |       0.74 | 0.85621 |
| 0.0005 |         10 |     30 | 0.27714 |     30 |       0.84 | 0.84713 |
| 0.0005 |         10 |     50 | 0.27931 |     39 |       0.80 | 0.84620 |
| 0.0004 |         10 |     40 |     0.28081 |         39 |           0.82 |     0.84204 |
| 0.0006 |         10 |     40 | 0.29608 |     32 |       0.54 | 0.82325 |
| 0.0007 |         10 |     40 | 0.29487 |     21 |       0.78 | 0.82656 |
| 0.0008 |         10 |     40 |     0.21589 |         39 |           0.76 |     0.92668 |
| 0.0006 | 8 | 40 | 0.27510 | 39 | 0.78 | 0.83554 |
| 0.0006 | 12 | 40 | 0.28407 | 40 | 0.88 | 0.85224 |
| 0.0004 | 10 | 40 | 0.28081 | 39 | 0.82 | 0.84204 |
| 0.0006 | 10 | 40 | 0.29802 | 32 | 0.46 | 0.82185 |


## fasc検証(DeepLabV3+)

| lr | pos_weight | epoch数 | Best Dice | Best epoch | Best threshold | Val Loss |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0004 | 10 | 40 | 0.28435 | 39 | 0.54 | 0.84064 |
| 0.0006 | 10 | 40 | 0.28829 | 39 | 0.54 | 0.84616 |
| 0.0005 | 10 | 40 | 0.28763 | 39 | 0.52 | 0.83855 |
| 0.0007 | 10 | 40 | 0.28805| 39 | 0.52 | 0.84466 |


## fasc検証(FPN)

| lr | pos_weight | epoch数 | Best Dice | Best epoch | Best threshold | Val Loss |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0004 | 10 | 40 | 0.28423 | 11 | 0.64 | 0.83904 |
| 0.0006 | 10 | 40 | 0.28580 | 11 | 0.68 | 0.83411 |


</details>

# 環境

* `Linux`- `Ubuntu`

```
git clone https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data.git
```

```
python3 -m venv .venv
```

```
source .venv/bin/activate
```
#deactivate

```
pip install -r requirements.txt
```
#pip freeze > requirements.txt

```
jupyter lab
```

# クローンした後の構成と手順

<details><summary></summary>

```
Muscle_Architecture_in_Ultrasound_Data$ tree

.
├── DeepLabV3+_fasc_model.ipynb
├── FPN_fasc_model.ipynb
├── README.md
├── Source
│   ├── f_1.py
│   └── f_2.py
├── UNet_DeepLab_fasc_ensemble.ipynb
├── UNet_Deep_FPN_fasc_ensemble.ipynb
├── UNet_FPN_fasc_ensemble.ipynb
├── apo_model.ipynb
├── best_model_nb_FPN
│   └── fasc
├── best_model_nb_UNet
│   ├── apo
│   └── fasc
├── best_model_nb_deepLabV3+
│   └── fasc
├── best_submission_of_predict_ensemble_fasc.ipynb     #kaggleベストスコア
├── content                                            #(コードにより自動生成)
│   └── my_dataset
|                └──                                   #(公式の画像image, mask, testデータ)
├── fasc_model.ipynb
├── img
│   └── img.png
├── requirements.txt
├── segmentation_baseline_models
│   ├── DeepLabV3_fasc_model.pth   #(コードにより自動生成)
│   ├── FPN_fasc_model.pth         #(コードにより自動生成)
│   ├── apo_model.pth              #(コードにより自動生成)
│   └── fasc_model.pth             #(コードにより自動生成)
├── study.ipynb
├── submission.csv                 #(コードにより自動生成)
├── test_submission_of_predict_ensemble_fasc.ipynb
└── umud-challenge-muscle-architecture-in-ultrasound-data.zip  #(公式よりDL)




step

1. apo_model.ipynb実行, 
   fasc_model.ipynb, 
   DeepLabV3+_fasc_model.ipynb,
   FPN_fasc_model.ipynb, 実行(colabで実行 or ローカルcudaで実行)
↓
2. apo_model.pth生成
   fasc_model.pth生成
   DeepLabV3_fasc_model.pth生成
   FPN_fasc_model.pth生成
   segmentation_baseline_models/に配置
↓
3. 各ensemble実行、アンサンブル時の両モデルの重み比率、しきい値を自動で決定
↓
4. submission_of_predict_ensemble_fasc.ipynb実行
↓
5. submission.csv生成
↓
6. kaggle提出

```

</details>






