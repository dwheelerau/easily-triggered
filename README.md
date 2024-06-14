# Dog-go-moo
A docker container with megadetector v5 and yolov10 models installed. This has GPU support. 
The container is tagged `dwheelerau/dog-go-moo:v0.5`.  

## Quick start
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


## ToDo  
Modify the docker file to include a repo of scripts for processing the outputs from the models.  
