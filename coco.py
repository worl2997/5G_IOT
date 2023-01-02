import xml.etree.ElementTree as ET
import os
import shutil
import json

# number of classes
# class names
names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def read_cls(path):
    ret = []
    with open(path, "r") as f:
        lines = f.readlines()
        for _str in lines:
            ret.append(_str.rstrip())
    
    return ret

def ms_coco(anno_path, cls):

    classes = {}
    dic = {}
    img_bbox = {}
    img_path = []
    with open(anno_path, 'r') as cf:
        json_data = json.load(cf)

    image = json_data['images']
    for imgs in image:
        dic[imgs['id']]= [imgs['file_name'], imgs['height'], imgs['width']]
        img_bbox[imgs['file_name']] = []
        img_path.append(imgs['file_name'])

    nc = len(json_data['categories'])
    for i in range(0, nc, 1):
        if json_data['categories'][i]['name'] not in cls:
            classes[json_data['categories'][i]['id']] = "skip"
        else:
            classes[json_data['categories'][i]['id']] = json_data['categories'][i]['name']

    anno = json_data['annotations']
    for an in anno:
        cls_id = an['category_id']

        if classes[cls_id] == "skip":
            continue

        img_name = dic[an['image_id']][0]

        height = int(dic[an['image_id']][1])
        width = int(dic[an['image_id']][2])

        x1 = int(an['bbox'][0])
        y1 = int(an['bbox'][1])
        w = int(an['bbox'][2])
        h = int(an['bbox'][3])

        wp = 1.0 / float(width) 
        hp = 1.0 / float(height)

        cx = x1 + w / 2
        cy = y1 + h / 2

        img_bbox[img_name].append([cls_id, cx * wp, cy * hp, w * wp, h * hp])

    '''
    classes = [id, category]
    img_bbox = dictionary [id_string] ->list [cls, cx, cy, w, h] with normalization as 0~1
    img_path = file name list
    '''
    return classes, img_bbox, img_path



# Convert
#custom class 
custom_cls = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign']
nc = len(custom_cls)
dir = './coco'
path = './COCOdevkit'

# coco  /images/ train2017 / xxxx.jpg
#       /labels/ train2017 / xxxx.txt
#       
for year, image_set in ('2017', 'train'), ('2017', 'val'):
    
    img_list_file_path = os.path.join(dir, image_set+year+'.txt')
    img_list_file = open(img_list_file_path, "w")
    anno_path = os.path.join(path, 'annotations', 'instances_'+image_set+year+'.json')
    cls_dic, img_bbox, img_path = ms_coco(anno_path, custom_cls)

    image_path = os.path.join(dir, 'images', image_set+year)
    label_path = os.path.join(dir, 'labels', image_set+year)
    create_folder(image_path)
    create_folder(label_path)
    
    for img in img_path:
        label_name = img.split('.')[0] + '.txt'
        new_lbs_path = os.path.join(dir, 'labels', image_set+year, label_name)
        img_box = []
        for box in img_bbox[img]:
            if cls_dic[box[0]] != "skip":
                new_cls_id = custom_cls.index(cls_dic[box[0]])
                img_box.append([new_cls_id, box[1], box[2], box[3], box[4]])

        if len(img_box) > 0:
            # 학습을 위한 파일 복사
            origin_img_path = os.path.join(path, 'images',image_set+year, img)
            dest_img_path = os.path.join(image_path, img)
            shutil.copyfile(origin_img_path, dest_img_path)
            img_list_file.write('./images/'+image_set+year+'/'+img +'\n')
            out_file = open(new_lbs_path, "w")
            for data in img_box:
                out_file.write(str(data[0])+' '+str(data[1]) + ' ' +str(data[2]) + ' ' + str(data[3]) +' ' + str(data[4]) + '\n')