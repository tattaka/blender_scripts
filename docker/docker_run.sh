docker run -it --runtime=nvidia --net=host -e DISPLAY=$DISPLAY --name $1\
	-e NVIDIA_DRIVER_CAPABILITIES=all -e NVIDIA_VISIBLE_DEVICES=all \
	-v $HOME/blender/scripts:/root/blender:rw -v \
	$HOME/.Xauthority:/root/.Xauthority:rw blender:2.78
