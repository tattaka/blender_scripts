FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

LABEL authors="tattaka <taka_aki@me.com>"

RUN apt-get update && \
	apt-get install -y \
		curl \
		bzip2 \
		libfreetype6 \
		libgl1-mesa-dev \
		libglu1-mesa \
		libxi6 \
		apt-file\
		software-properties-common\
		tmux nano net-tools inetutils-ping\
		x11-apps\
		nvidia-modprobe\
		libxrender1 && \
	apt-get -y autoremove && \
	rm -rf /var/lib/apt/lists/*

#RUN add-apt-repository -y ppa:thomas-schiex/blender
RUN apt-get -y update && apt-get install -y blender blender-data
