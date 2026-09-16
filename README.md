# UMUDチャレンジ：超音波データによる筋肉構造の解析


# ファイル

| 名称      | ファイル名  | 備考     |
| ---------- | ---- | ------ |
| データ確認ファイル | [study.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/study.ipynb) |  |
| 画像サイズ違いについての整合調査ファイル |[Imagesize_investigation.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/Imagesize_investigation.ipynb)     |  |
|apo_fascセグメンテーション|[segmentation.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/segmentation.ipynb)||
|apo_fascセグメンテーションモデルベースライン|[model.md](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/segmentation_baseline_models/model.md)||
|予測=>提出|[submission_of_predict.ipynb](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/submission_of_predict.ipynb)||
|メモ|[step.md](https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data/blob/main/step.md)||

# 環境 

```linux```

```
git clone https://github.com/kenkenkengo0421/Muscle_Architecture_in_Ultrasound_Data.git
```

```
python3 -m venv .venv
```

```
source .venv/bin/activate

#deactivate
```

```
pip install -r requirements.txt

#pip freeze > requirements.txt
```


```
jupyter lab
```


# 課題概要

このコンテストの目的は、超音波画像から3つの主要な筋肉構造変数を正確に推定できるアルゴリズムを構築することです。


テストデータセット内の各超音波画像について、これら3つの値を予測する必要があります。
[提出されたデータは、 UMUDスコアという](https://www.kaggle.com/code/paulritsche/umud-score)複合指標を用いてランク付けされます。この指標は、3つの変数すべてにおける予測精度を評価するものです。

# 評価

**[提出された提案は、3つのアーキテクチャ変数すべてにおける予測誤差を測定するUMUDスコア](https://www.kaggle.com/code/paulritsche/umud-score)**を使用して評価されます。

このスコアは、以下の項目における**正規化された平均絶対誤差（MAE）**に基づいています。

```
羽状角(Pennation Angle)（PA）：筋束と腱膜の間の角度（度）黄色
    
筋束長(Fascicle Length)（FL）：筋束の長さ（ミリメートル）（緑色）
    
筋厚(Muscle Thickness)（MT）：表層腱膜と深層腱膜間の距離（ミリメートル）（ピンク色）
```

![[Pasted image 20260911150238.png]]

各変数の誤差は、異なる単位や尺度であっても比較可能な影響を確保するために、あらかじめ定義された許容値によって正規化されます。スコア**が低いほど、パフォーマンスが優れていることを示します。**


