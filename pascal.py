import xml.etree.ElementTree as ET
import os
import shutil

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def convert_box(size, box):
        dw, dh = 1. / size[0], 1. / size[1]
        x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
        return [x * dw, y * dh, w * dw, h * dh]

def pascal(anno_path, image_path, cls):
    
    classes = { 0 : 'background', 1 : 'aeroplane', 2 : 'bicycle', 3: 'bird', 4 : 'boat', 5: 'bottle', 6: 'bus', 7:'car', 8:'cat', 9: 'chair', 10: 'cow', 
                11: 'diningtable', 12:'dog', 13: 'horse', 14: 'motorbike', 15:'person', 16:'pottedplant', 17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

    img_bbox = {}
    img_path = []

    r_classes = {v:k for k,v in classes.items()}
    
    img_name = os.listdir(image_path)

    for img in img_name:
        file_names = img
        anno_names = file_names.replace('jpg', 'xml')
        img_path.append(img)
        img_bbox[img] = []

        xml = ET.parse(os.path.join(anno_path, anno_names)).getroot()

        for img_size in xml.iter('size'):

            width = int(img_size.find('width').text)
            height = int(img_size.find('height').text)

        for obj in xml.iter('object'):
            # VOC 는 원점이 1,1 부터 시작이므로 0,0 으로 바꾼다

            cls_name = str(obj.find('name').text)
            diff_score = int(obj.find('difficult').text)
            
            if cls_name not in cls:
                c_id = r_classes[cls_name]
                classes[c_id] = 'skip'
            elif diff_score == 1:
                skippppppppppp = 1
            else:


                xmlbox = obj.find('bndbox')
                xmin = float(xmlbox.find('xmin').text)
                ymin = float(xmlbox.find('ymin').text)
                xmax = float(xmlbox.find('xmax').text)
                ymax = float(xmlbox.find('ymax').text)

                cx, cy, w, h = convert_box((width,height), [xmin, xmax, ymin, ymax])
                cls_id = r_classes[cls_name]

                img_bbox[img].append([cls_id, cx, cy, w, h])

    return classes, img_bbox, img_path


# Convert
dir = './pascal'
path = './VOCdevkit'
# Convert
custom_cls=['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair'] 
nc = len(custom_cls)


for year, image_set in ('2012', 'train'), ('2012', 'val'):
    set_path = os.path.join(path,'VOC'+year)
    anno_path = os.path.join(set_path, 'Annotations')
    image_path = os.path.join(set_path, 'JPEGImages')

    imgs_path = os.path.join(dir,'images', image_set+year)
    lbs_path = os.path.join(dir,'labels', image_set+year)
    path_year = os.path.join(path, 'VOC'+year)
    create_folder(imgs_path)
    create_folder(lbs_path)

    cls_dic, img_bbox, img_path = pascal(anno_path, image_path, custom_cls)

    img_list_file_path = os.path.join(dir, image_set+year+'.txt')
    img_list_file = open(img_list_file_path, "w")

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
            origin_img_path = os.path.join(image_path, img)
            dest_img_path = os.path.join(imgs_path, img)
            shutil.copyfile(origin_img_path, dest_img_path)

            img_list_file.write('./images/'+image_set+year+'/'+img +'\n')
            out_file = open(new_lbs_path, "w")
            for data in img_box:
                out_file.write(str(data[0])+' '+str(data[1]) + ' ' +str(data[2]) + ' ' + str(data[3]) +' ' + str(data[4]) + '\n')





# def convert_label(data_path, img_path, lb_path, year, image_id):
        
#     anno_path = os.path.join(data_path,'Annotations', image_id + '.xml' )
#     out_path = os.path.join(lb_path , image_id +'.txt')
#     out_file = open(out_path, "w")
#     tree = ET.parse(anno_path)
#     root = tree.getroot()
#     size = root.find('size')

#     w = int(size.find('width').text)
#     h = int(size.find('height').text)

#     axis = []
#     for obj in root.iter('object'):
#         cls = obj.find('name').text
#         if cls in names and not int(obj.find('difficult').text) == 1:
            
#             xmlbox = obj.find('bndbox')
#             xmin = float(xmlbox.find('xmin').text)
#             ymin = float(xmlbox.find('ymin').text)
#             xmax = float(xmlbox.find('xmax').text)
#             ymax = float(xmlbox.find('ymax').text)

#             ret = convert_box((w,h), [xmin, xmax, ymin, ymax])
#             cls_id = names.index(cls)  # class id
#             ret.append(cls_id)
#             axis.append(ret)
#     origin_img_path = os.path.join(data_path, 'JPEGImages', image_id +'.jpg')
#     dest_img_path = os.path.join(img_path, image_id+'.jpg')
#     shutil.copyfile(origin_img_path ,dest_img_path)
#     for axi in axis:
#         out_file.write(str(axi[4]) + ' ' +str(axi[0]) +' ' +str(axi[1]) + ' ' + str(axi[2]) + ' ' + str(axi[3]) + '\n')

# # pascal/images/ test2012 / xxxx.jpg
# #       /labels/ test2012 / xxxx.txt
# #       
# for year, image_set in ('2012', 'train'), ('2012', 'val'):

#     img_list_file_path = os.path.join(dir, image_set+year +'.txt')
#     img_list_file = open(img_list_file_path, "w")

#     imgs_path = os.path.join(dir,'images', image_set+year)
#     lbs_path = os.path.join(dir,'labels', image_set+year)
#     path_year = os.path.join(path, 'VOC'+year)
#     create_folder(imgs_path)
#     create_folder(lbs_path)

#     file_path = os.path.join(path, 'VOC'+year+'/ImageSets/Main/'+image_set+'.txt')
#     with open(file_path, "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             id = line.rstrip()
#             convert_label(path_year, imgs_path, lbs_path, year, id)
#             img_list_file.write('./images/'+image_set+year+'/'+id +'.jpg\n')
