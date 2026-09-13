
# ロードマップ、メモ等

## STEP 1
* apo segmentation
* Dataset完成
* U-Net完成
* 1 epoch動作確認済み

## STEP 2  apo segmentationの評価
* Dice / IoU
* 予測maskの可視化

## STEP 3  fasc segmentation
* FascDataset
* U-Net
* 学習
* Dice / IoU
* 予測確認

## STEP 4  predicted apo maskの構造解析
* superficial apo
* deep apo
* を抽出

## STEP 5  predicted fasc maskの構造解析
* fascicle方向・線を抽出

## STEP 6  geometry
* apo + fasc
↓
PA,FL,MT

## STEP 7  pixel → mm の換算

## STEP 8
* test_images
↓
* apo_model
* fasc_model
↓
* geometry
↓
* pa_deg / fl_mm / mt_mm
↓
* submission.csv


# model作成時の構成

```
セル0
zip処理
```
```
セル１
関数、ライブラリの定義、
```

```
セル2
設定と確認など
```

```
セル3

全データ
↓
train
val
--------------
train画像
↓
モデル
↓
予測
↓
trainの正解maskと比較
↓
loss計算
↓
重み更新
--------------
val画像
↓
学習途中のモデル
↓
予測
↓
valの正解maskと比較
↓
validation lossを計算


loss      → 0 に近づける
```

```
セル4

保存した apo_model.pth を読込

保存モデル + val
↓
予測mask
↓
正解maskと比較
↓
Dice / IoU


----

Dice, IoU  → 1 に近づける


Dice = 2 × 重なった部分
       ─────────────
       予測部分 + 正解部分

IoU = 重なった部分
      ───────────
      予測と正解を合わせた全体
```

