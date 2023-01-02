#!/bin/bash
# COCO 2017 dataset http://cocodataset.org
# Download command: bash ./scripts/get_coco.sh
mkdir pascal
mkdir pascal/images
mkdir pascal/labels

# Download/unzip images
d='./' # unzip directory
url=http://host.robots.ox.ac.uk/pascal/VOC/voc2012/
f1='VOCtrainval_11-May-2012.tar'

if test -f $f1; then
    echo 'file already downloaded .. skip download process...'
else
  for f in $f1; do
    echo 'Downloading' $url$f '...'
    curl -L $url$f -o $f && tar -xvf $f & # download, unzip, remove in background
  done
fi
wait # finish background tasks