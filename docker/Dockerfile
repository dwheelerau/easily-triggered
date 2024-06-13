#To build this file:
#sudo docker build -f Dockerfile . -t dwheelerau/megadetector:ubuntu2004

#To run this, mounting your current host directory in the container directory,
# at /project, and excute the check_installtion script which is in your current
# working direcotry run:
#sudo docker run --gpus all -it -v `pwd`:/project dwheelerau/marsupial:ubuntu2004 /bin/bash -c "cd /project && python /build/marsupial/prediction_batch.py -i /build/marsupial/data -m /build/marsupial/weights/marsupial_72s.pt -o processed_images"

#To push to docker hub:
#sudo docker push dwheelerau/marsupial:ubuntu2004

# Pull base image.
#FROM nvidia/cuda:11.2.0-cudnn8-devel-ubuntu20.04
#MAINTAINER Dave Wheeler NSWDPI
FROM nvidia/cuda:12.2.0-base-ubuntu22.04
MAINTAINER Dave Wheeler NSWDPI

# Set up ubuntu dependencies
RUN apt-get update -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata vim wget git build-essential git curl libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 python3-opencv && \
  rm -rf /var/lib/apt/lists/*

###### 
# Make the dir everything will go in
WORKDIR /build

# Intall anaconda 3.9
ENV PATH="/build/miniconda3/bin:${PATH}"
ARG PATH="/build/miniconda3/bin:${PATH}"
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py39_22.11.1-1-Linux-x86_64.sh &&\
	mkdir /build/.conda && \
	bash miniconda.sh -b -p /build/miniconda3 &&\
	rm -rf miniconda.sh

RUN conda --version

# clone the repo for the scripts and utils
RUN git clone https://github.com/microsoft/CameraTraps.git

RUN python -m pip install --upgrade pip
RUN pip --version
#RUN pip install PytorchWildlife
RUN pip install megadetector

# Yolov10
RUN pip install -q git+https://github.com/THU-MIG/yolov10.git

RUN mkdir /build/weights

# get the 10l weights
RUN wget -P /build/weights/ -q https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10l.pt
RUN conda install -y -c conda-forge huggingface_hub

CMD /bin/bash
