# Dog-go-moo
A docker container with [megadetector](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md) 
v5 and [yolov10](https://github.com/THU-MIG/yolov10) models installed. 
This will facility rapid removal of 
empty images from camera trap datasets. In my testing the 
false negative rate is less than 1%. The false positive rate 
is somewhat higher (~3-5%) depending on the
background.  

[Yolov10](https://github.com/THU-MIG/yolov10) can be used 
to further categorise images,
however, only a limited number of 
[class labels](#yolo-class-labels) are
available. 

The container is tagged `dwheelerau/dog-go-moo:v0.5` and
is based on a cuda base image to make Nvidia GPUs available.  

## Quick start to process
```
# use `docker images` to find image ID, here it is eb25af9717a5
docker run --gpus all -it -v `pwd`:/project eb25af9717a5 /bin/bash

## Run MD batch detector
python -m megadetector.detection.run_detector_batch 'MDV5A' cattle/ cattle-md.json

## MD JSON to CSV conversion  
python scripts/json_to_csv.py -i ./data/project.json -t 0.3   

## Sort images into Animal, vehicle, person, empty based on CSV
python ./scripts/collect_image_files.py -b ./data/ -i ./data/project.csv -o ./

## RUn Yolov10 on the animal directory  
yolo predict model=/build/weights/yolov10l.pt source=Animal/ conf=0.25 save_txt=True line_width=2 show_labels=True classes=[16,19]
```

The docker images are best used on Windoz systems using
[Docker desktop](https://www.docker.com/products/docker-desktop/). 
After it is installed search for the tagged image 
`dwheelerau/dog-go-moo:v0.5`.  

## Workflow for testing
1. Find the Docker image ID and start container dog-go-moo mounting the current
working directory that contains your camera trap images.  
```
# find the dog-go-moo image ID
docker images

# in this example the image ID is eb25af9717a5 (yours will be different)
docker run --gpus all -it -v `pwd`:/project eb25af9717a5 /bin/bash
```
The above command will mount your current working directory in `/projects/` 
in the container.  

2. Run Megadetector, assumes your images are in the current working 
directory      
```
# check your images are visible
ls /projects/
# run MD with a threshold of 0.3 for detection. Recursively look for images 
python -m megadetector.detection.run_detector_batch 'MDV5A' /project/ project.json --recursive --threshold 0.3  
```
The above command will create a file of detections called `project.json`.    

3. Run `script/json_to_csv.py` to get a human friendly output from the JSON 
file.  

`python scripts/json_to_csv.py -i project.json -t 0.3`   

4. Copy images from the original directories to subdirectories in a destination based on md classes. Note the script preserve the original sub-directory 
structure to avoid file name clashes and help keep your projects organised.   
`python ./scripts/collect_image_files.py -b ./data/ -i ./data/project.csv -o ./sorted`

The above command copies the images into directories in a directory called
`sorted` in your current working directory.  

5. Optional. From the container, run yolov10 on the animal directory generated
in step 4. Note you need to loop 
through the subdirs in animal directory. In this case the output is saved via 
the `project` var. Inote I get poorer performance when I specified the image 
dims using `imgsz=[1080,1920]`, so I use the defaults.    

```
# https://docs.ultralytics.com/usage/cfg/#predict-settings
# Opt 1: saving yolo annotations with BBox info, good for testing
for dir in /project/tmp/animal/*; 
do 
	outdir=$(basename $dir); yolo predict model=/build/weights/yolov10l.pt source=$dir project=/project/yolov10/$outdir save_txt=True line_width=2 show_labels=True classes=[16,19] conf=0.25;
done

## Opt 2: dont save images to avoid using disk space, generates text files  
 for dir in /project/tmp/animal/*; do outdir=$(basename $dir); yolo predict model=/build/weights/yolov10l.pt source=$dir project=/project/yolov10/$outdir save=False save_txt=True save_conf=True classes=[16,19] conf=0.25;done
```
In the above example, image in `100RECNX` will be saved in 
`/project/yolov10/100RECNX/`.  

The resulting text outputs files is `100RECNX/predict/labels/infile.txt`.  
This data looks like this.   
```
class xy xy xy xy confidence
16 0.534338 0.533914 0.28263 0.911393 0.959702
```

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
14="bird"
15="cat"
16="dog"
17="horse"
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
