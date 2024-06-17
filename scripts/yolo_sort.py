#!/usr/bin/env python
import argparse
import glob
import os
import shutil

# sort images based on yolo classifications  
# create the parser
my_parser = argparse.ArgumentParser(description='sort images based on yolo classifications',
                                    epilog='example: python scripts/yolo_sort.py -t 0.2 -b yolo_detections -o savedir -i images/ -c 16 19') 

# add detection threshold
my_parser.add_argument('-t', '--threshold', metavar='threshold', type=float,
                       default=0.8, action='store', dest='threshold',
                       help='Detection threshold cut-off value. Must be between 0.0 < 1.0. Default value is 0.8')

my_parser.add_argument('-b', '--detection_basedir', metavar='DBASEDIR', type=str,
                       action='store', dest='detection_basedir', required=True,
                       help='base directory for yolo detection TXT files')
my_parser.add_argument('-i', '--images_basedir', metavar='IBASEDIR', type=str,
                       action='store', dest='image_basedir', required=True,
                       help='base directory for images files JPGs')
my_parser.add_argument('-o', '--out_basedir', metavar='OBASEDIR', type=str,
                       action='store', dest='out_basedir', required=True,
                       help='base directory to copy sorted JPGs')
my_parser.add_argument('-c', '--classes', metavar='CLASSES', type=int,
                       action='store', dest='classes', nargs='+',
                       required=True, help='target yolov10 classes')
my_parser.add_argument('-a', '--all_images',
                       action='store_true', required=False, 
                       help='Copy all images in -i that are not included in --c to a dir called "other"')

args = my_parser.parse_args()

class_dict = {
    0:"person",
    1:"bicycle",
    2:"car",
    3:"motorcycle",
    4:"airplane",
    5:"bus",
    6:"train",
    7:"truck",
    8:"boat",
    9:"traffic light",
    10:"fire hydrant",
    11:"stop sign",
    12:"parking meter",
    13:"bench",
    14:"bird",
    15:"cat",
    16:"dog",
    17:"horse",
    18:"sheep",
    19:"cow",
    20:"elephant",
    21:"bear",
    22:"zebra",
    23:"giraffe",
    24:"backpack",
    25:"umbrella",
    26:"handbag",
    27:"tie",
    28:"suitcase",
    29:"frisbee",
    30:"skis",
    31:"snowboard",
    32:"sports ball",
    33:"kite",
    34:"baseball bat",
    35:"baseball glove",
    36:"skateboard",
    37:"surfboard",
    38:"tennis racket",
    39:"bottle",
    40:"wine glass",
    41:"cup",
    42:"fork",
    43:"knife",
    44:"spoon",
    45:"bowl",
    46:"banana",
    47:"apple",
    48:"sandwich",
    49:"orange",
    50:"broccoli",
    51:"carrot",
    52:"hot dog",
    53:"pizza",
    54:"donut",
    55:"cake",
    56:"chair",
    57:"couch",
    58:"potted plant",
    59:"bed",
    60:"dining table",
    61:"toilet",
    62:"tv",
    63:"laptop",
    64:"mouse",
    65:"remote",
    66:"keyboard",
    67:"cell phone",
    68:"microwave",
    69:"oven",
    70:"toaster",
    71:"sink",
    72:"refrigerator",
    73:"book",
    74:"clock",
    75:"vase",
    76:"scissors",
    77:"teddy bear",
    78:"hair drier",
    79:"toothbrush"
}
target_detections = glob.glob(os.path.join(args.detection_basedir,'**','*.txt'), 
                              recursive=True)
# sort the target classes
args.classes.sort()

# all images available
if args.all_images:
    all_images = glob.glob(os.path.join(args.image_basedir, '**','*.JPG'),
                           recursive=True)

for target in target_detections:
    detections = os.path.basename(target)
    image_subdir = target.replace(args.detection_basedir,'').split(os.sep)[0]
    detections_img = os.path.join(args.image_basedir, 
                                  image_subdir, 
                                  detections.replace('.txt', '.JPG'))
    print('here')
    print(detections_img)
    # don't copy to the 'other' directory
    if args.all_images:
        all_images.remove(detections_img)
    with open(target) as rf:
        detection_classes = []
        for line in rf:
            data = line.strip().split(' ')
            detection_class = int(data[0])
            # prob might not be included
            if len(data) == 6:
                prob = float(data[-1])
            else:
                prob = None
            detection_classes.append((detection_class, prob))
        # this next bit of logic groups paired classes
        if prob:
            uniq_detection_classes = [i[0] for i in detection_classes
                                       if i[1] > args.threshold and
                                       i[0] in args.classes]
        else:
            uniq_detection_classes = [i[0] for i in detection_classes]
        uniq_detection_classes = list(set(uniq_detection_classes))
        uniq_detection_classes.sort()
        if uniq_detection_classes == args.classes:
            # target classes detected in same image
            outdir = '_'.join([class_dict[c] for c in args.classes])
            out_path = os.path.join(args.out_basedir, outdir, image_subdir)
            os.makedirs(out_path, exist_ok=True)
            shutil.copy2(detections_img, out_path)
        else:
            # if empty list due to prob<threshold nothing is done
            for uniq in uniq_detection_classes:
                outdir = class_dict[uniq]
                out_path = os.path.join(args.out_basedir, outdir, image_subdir)
                os.makedirs(out_path, exist_ok=True)
                shutil.copy2(detections_img, out_path)
# -a all images not in -c copied to other 
if args.all_images:
    outdir = "other"
    for image in all_images:
        print(image)
        image_subdir = image.split(os.sep)[-2]
        out_path = os.path.join(args.out_basedir, outdir, image_subdir)
        os.makedirs(out_path, exist_ok=True)
        shutil.copy2(image, out_path)
print()
print("###########################################################")
print("Note: If an image contains two classes not captured by the -c flag, the ")
print("image file will be found duplicated as it will be copied into each class directory")
print("###########################################################")