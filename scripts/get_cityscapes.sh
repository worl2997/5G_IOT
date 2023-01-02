# 압축 풀고

mkdir cityscapes
mkdir cityscapes/images
mkdir cityscapes/labels


d='./CITYSCAPESdevkit'
f1='cityscapes.zip'
unzip -q $f1 -d $d &
wait