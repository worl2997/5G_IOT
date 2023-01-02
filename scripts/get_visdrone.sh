#!/bin/bash
# COCO 2017 dataset http://cocodataset.org
# Download command: bash ./scripts/get_coco.sh
mkdir visdrone
mkdir visdrone/images
mkdir visdrone/labels

# Train set
d='./VISDRONEdevkit' # unzip directory
f1='VisDrone2019-DET-train.zip'
unzip -q $f1 -d $d 

#Val set
d='./VISDRONEdevkit' # unzip directory
f1='VisDrone2019-DET-val.zip'
unzip -q $f1 -d $d
wait # finish background tasks