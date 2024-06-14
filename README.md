# Dog-go-moo
A docker container with megadetector v5 and yolov10 models installed. This has GPU support. 
The container is tagged `dwheelerau/dog-go-moo:v0.5`.  

Megadetector is used to classify images as empty, person, vehicle, or animal. A script sorts
images into folders based on these classifications. The animal folder is then processed
with yolov10, with the class categories cattle, dog, xxxx (not bear).  

## Quick start to process
```
docker run --gpus all -it -v `pwd`:/project eb25af9717a5 /bin/bash
# will log you into the container
## MD
python -m megadetector.detection.run_detector_batch 'MDV5A' cattle/ cattle-md.json
## Yolo just dogs=16 and cows=19 classes
yolo predict model=/build/weights/yolov10l.pt source=cattle/ conf=0.25 save_txt=True line_width=2 show_labels=True classes=[16,19]
```

See 202406pfleming for more commands.  

## Workflow for testing
1. start container dog-go-moo

2. run MD  
`python -m megadetector.detection.run_detector_batch 'MDV5A' /project/ project.json --recursive --threshold 0.3`  

3. Run `script/json_to_csv.py` to get a human friendly output.  

`python scripts/json_to_csv.py -i project.json -t 0.3`   

4. Copy images from the original directories to subdirectories in a destination based on md classes.  
`python ../scripts/collect_image_files.py -b ../data/ -i ../data/project.csv -o ./`

5. From the container, run yolov10 on the animal directory generated in step 4. Note you need to loop 
through the subdirs in animal. In this case the output is saved via the `projec` var. Note
I got poorer performance when I specified the image dims using `imgsz=[1080,1920]`  
```
# https://docs.ultralytics.com/usage/cfg/#predict-settings
# saving images for testing, turn this off via  save=False
for dir in /project/tmp/animal/*; 
do 
	outdir=$(basename $dir); yolo predict model=/build/weights/yolov10l.pt source=$dir project=/project/yolov10/$outdir save_txt=True line_width=2 show_labels=True classes=[16,19] conf=0.25;
done

## turning off image saving
 for dir in /project/tmp/animal/*; do outdir=$(basename $dir); yolo predict model=/build/weights/yolov10l.pt source=$dir project=/project/yolov10/$outdir save=False save_txt=True save_conf=True classes=[16,19] conf=0.25;done
```

The resulting text outputs files is `100RECNX/predict/labels/infile.txt`  
```
class xy xy xy xy confidence
16 0.534338 0.533914 0.28263 0.911393 0.959702
```

In the above example, image in `100RECNX` will be saved in `/project/yolov10/100RECNX/`.  

6. Run the `script/xx` to collect the outputs from yolo and copy the files to subdirectories [ToDo]  

## Yolo class labels
```
0="person"
1="bicycle"
"car"
"motorcycle"
"airplane"
"bus"
"train"
"truck"
"boat"
"traffic light"
"fire hydrant",
"stop sign"
"parking meter"
"bench"
"bird"
"cat"
16="dog"
"horse"
18="sheep"
19="cow"
"elephant"
"bear"
"zebra",
"giraffe"
"backpack"
"umbrella"
"handbag"
"tie"
"suitcase"
"frisbee"
"skis"
"snowboard"
"sports ball"
"kite",
"baseball bat"
"baseball glove"
"skateboard"
"surfboard"
"tennis racket"
"bottle"
"wine glass"
"cup"
"fork"
"knife",
"spoon"
"bowl"
"banana"
"apple"
"sandwich"
"orange"
"broccoli"
"carrot"
"hot dog"
"pizza"
"donut"
"cake"
"chair",
"couch"
"potted plant"
"bed"
"dining table"
"toilet"
"tv"
"laptop"
"mouse"
"remote"
"keyboard"
"cell phone",
"microwave"
"oven"
"toaster"
"sink"
"refrigerator"
"book"
"clock"
"vase"
"scissors"
"teddy bear"
"hair drier"
"toothbrush"
```


## ToDo  
Modify the docker file to include a repo of scripts for processing the outputs from the models.  
