#!/bin/bash
# COCO 2017 dataset http://cocodataset.org
# Download command: bash ./scripts/get_coco.sh
mkdir coco
mkdir coco/images
mkdir coco/labels

# Download/unzip labels
d='./COCOdevkit' # unzip directory
url=http://images.cocodataset.org/annotations/
f1=annotations_trainval2017.zip

if test -f $f1; then
    echo 'file already downloaded .. skip download process...'
else
  for f in $f1; do
    echo 'Downloading' $url$f '...'
    curl -L $url$f -o $f && unzip -q $f -d $d & # download, unzip, remove in background
  done
fi

# Download/unzip images
d='./COCOdevkit/images' # unzip directory
url=http://images.cocodataset.org/zips/
f1='train2017.zip' # 19G, 118k images
f2='val2017.zip'   # 1G, 5k images
f3='test2017.zip'  # 7G, 41k images (optional)
for f in $f1 $f2 $f3; do
    if test -f $f; then
        echo 'file already downloaded .. skip download process...'
    else
        echo 'Downloading' $url$f '...'
        curl -L $url$f -o $f && unzip -q $f -d $d &# download, unzip, remove in background
    fi
done

wait # finish background tasks