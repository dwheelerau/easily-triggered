# notebook notes and random things as well as AI assisted labelling  

Yolov10 training output from colab notebook `cattle_dog_yolov10_training`.

```
 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% 4/4 [00:03<00:00,  1.08it/s]
                   all        128        230       0.91      0.865      0.911      0.732
                cattle        128        152       0.86      0.769       0.85      0.685
                   dog        128         78       0.96      0.962      0.971      0.778

 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 8/8 [00:05<00:00,  1.46it/s]
                   all        128        230      0.913      0.859      0.909      0.727
                cattle        128        152      0.865      0.758      0.848      0.684
                   dog        128         78      0.962      0.961       0.97      0.769
Speed: 1.1ms preprocess, 21.9ms inference, 0.0ms loss, 2.6ms postprocess per image
Results saved to runs/detect/val
{'metrics/precision(B)': 0.9131801623201614, 
'metrics/recall(B)': 0.8592759284658378, 
'metrics/mAP50(B)': 0.9092502315300575, 
'metrics/mAP50-95(B)': 0.7267732825989388, 
'fitness': 0.7450209774920508}
```
  
- `Colab Notebooks/yolov8_basemodel_peter.ipynb` based model testing and usage.  
- `Calab Notebooks/cattle_dog_yolov8_training.ipynb` training run.  


## GUI support from MS wildlife demo  
Has a nice GUI running on `http://0.0.0.0/`. Allows indiv images
as well as batch inference.  

See the main [repo](https://github.com/microsoft/CameraTraps/blob/main/INSTALLATION.md).  

```
docker pull andreshdz/pytorchwildlife:1.0.2.3
docker run -p 80:80 andreshdz/pytorchwildlife:1.0.2.3 python demo/gradio_demo.py
```
If you want to run any code using the docker image, please use 
`docker run andreshdz/pytorchwildlife:1.0.2.3` followed by the 
command that you want to execute.  


## Envs

## Misc commands  
```
sudo docker build -f Dockerfile . -t dwheelerau/megadetector:ubuntu2004
sudo docker push dwheelerau/megadetector:ubuntu2004
sudo docker pull dwheelerau/megadetector:ubuntu2004
```

## Convert MD json to labelme jsons for AI assisted obj labeling.  
1. clone the megadetector repo 
```
git clone https://github.com/agentmorris/MegaDetector/tree/main
```
2. Follow the install instructions and activate the env
```
### NOTE CHANGE PATH ###
mkdir ~/git
cd ~/git
git clone https://github.com/ecologize/yolov5/
git clone https://github.com/agentmorris/MegaDetector
cd ~/git/MegaDetector
mamba env create --file envs/environment-detector.yml
mamba activate cameratraps-detector
### NOTE CHANGE PATH ###
export PYTHONPATH="$HOME/git/MegaDetector:$HOME/git/yolov5"
```
3. Convert the MD.json to COCO.json (yes I know...)  
```
# threshold set at 0.2 (option def 0.15)
python megadetector/postprocessing/md_to_labelme.py --image_folder ./ md.json coco.json 02
```
4. Convert COCO.json to labelme.json
```
# path is base path here assuming relative paths were not used in md.json
python megadetector/data_management/coco_to_labelme.py COCO.json ./
```

## Convert labelme to yolo   
I installed this in the `labelme` env using pip
```
pip install labelme2yolo
labelme2yolo --json_dir ./ --val_size 0.2
```

https://pypi.org/project/labelme2yolo/

## Convert to gray scale
```
for jpg in *.JPG; do out=$(echo $jpg | sed 's/.JPG/gry.JPG/'); echo $jpg; convert $jpg -colorspace Gray $out;done
```

