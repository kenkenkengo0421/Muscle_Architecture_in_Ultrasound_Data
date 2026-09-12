STEP 1  apo segmentation
        Dataset完成
        U-Net完成
        1 epoch動作確認済み

STEP 2  apo segmentationの評価
        Dice / IoU
        予測maskの可視化

STEP 3  fasc segmentation
        FascDataset
        U-Net
        学習
        Dice / IoU
        予測確認

STEP 4  predicted apo maskの構造解析
        superficial apo
        deep apo
        を抽出

STEP 5  predicted fasc maskの構造解析
        fascicle方向・線を抽出

STEP 6  geometry
        apo + fasc
          ↓
        PA
        FL
        MT

STEP 7  pixel → mm の換算

STEP 8
        test_images
            ↓
        apo_model
        fasc_model
            ↓
        geometry
            ↓
        pa_deg / fl_mm / mt_mm
            ↓
        submission.csv