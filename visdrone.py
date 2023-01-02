import xml.etree.ElementTree as ET
import os
import shutil
import json
import cv2

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def visdrone(anno_path, image_path, cls):


    # class names
    classes = [ 'background', 'pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle',
         'bus', 'motor', 'others']

    img_bbox = {}
    img_path = []


    anno_files = os.listdir(anno_path)
    
    for anno in anno_files:
        img_name = anno.replace('txt','jpg')
        img_bbox[img_name] = []
        with open(os.path.join(anno_path, anno), 'r') as f:
            lines = f.readlines()
            img = cv2.imread(os.path.join(image_path, img_name))
            height, width = img.shape[:2]
            wp = 1.0 / float(width) 
            hp = 1.0 / float(height)
            
            flag = False
            for line in lines:
                comm = line.rstrip().split(',')
                x1 = float(comm[0])
                y1 = float(comm[1])
                w = float(comm[2])
                h = float(comm[3])
                cls_id = int(comm[5])

                if cls_id == 0 or cls_id == 11 or classes[cls_id] not in cls:
                    # background or others or not include custom class list
                    classes[cls_id] = "skip"
                
                else:
                    # object and include custom class list
                    cx = x1 + w / 2.0
                    cy = y1 + h / 2.0
                    img_bbox[img_name].append([cls_id, cx*wp, cy* hp, w* wp, h * hp])
                    flag = True

            if flag == True :
                img_path.append(img_name)
                
    return classes, img_bbox, img_path


# Convert
#custom class 
custom_cls = ['pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle',
         'bus', 'motor']
         
nc = len(custom_cls)
dir = './visdrone'
path = './VISDRONEdevkit'

# visdrone /images/ train2017 / xxxx.jpg
#          /labels/ train2017 / xxxx.txt
#       
for year, image_set in ('2019', 'train'), ('2019', 'val'):
    
    set_path = os.path.join(path, 'VisDrone'+year+'-DET-'+image_set)
    anno_path = os.path.join(set_path, 'annotations')
    imgs_path = os.path.join(set_path, 'images')

    cls_dic, img_bbox, img_path = visdrone(anno_path, imgs_path, custom_cls)

    
    img_list_file_path = os.path.join(dir, image_set+year+'.txt')
    img_list_file = open(img_list_file_path, "w")
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
            origin_img_path = os.path.join(imgs_path, img)
            dest_img_path = os.path.join(image_path, img)
            shutil.copyfile(origin_img_path, dest_img_path)
            img_list_file.write('./images/'+image_set+year+'/'+img +'\n')
            out_file = open(new_lbs_path, "w")
            for data in img_box:
                out_file.write(str(data[0])+' '+str(data[1]) + ' ' +str(data[2]) + ' ' + str(data[3]) +' ' + str(data[4]) + '\n')