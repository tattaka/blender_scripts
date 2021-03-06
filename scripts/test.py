# -*- coding: utf-8 -*-

import os
import bpy
import math
from datetime import datetime
import csv
import copy
#デフォルトで存在しているCubeとライトを削除
#bpy.data.objects['Lamp'].select = True
bpy.ops.object.delete()

#def makeMaterial(name, diffuse, specular, alpha):
def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

#Cube作成
red = makeMaterial('Red', (1,0,0), (1,1,1), 1)
blue = makeMaterial('Blue', (0,0,1), (1,1,1), 1)

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2))
bpy.ops.rigidbody.object_add(type='ACTIVE')
setMaterial(bpy.context.object, red)

bpy.ops.mesh.primitive_cube_add(location=(3, 0, 6))
bpy.ops.rigidbody.object_add(type='ACTIVE')
setMaterial(bpy.context.object, blue)

bpy.data.objects["Cube"].scale = (2, 2, 2)
bpy.data.objects["Cube.001"].scale = (2, 2, 2)

#平面作成
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
bpy.ops.rigidbody.object_add(type='PASSIVE')
bpy.data.objects["Plane"].scale = (1000, 1000, 1)

#照明

#bpy.data.lamps["Lamp"].type = 'AREA'
#bpy.data.objects["Lamp"].location = (30, 0, 100)
#bpy.data.lamps["Lamp"].energy = 5

bpy.data.objects["Lamp"].location = (0, 0, 30)
bpy.data.lamps["Lamp"].type = 'SUN'
bpy.data.lamps["Lamp"].energy = 0.7

#画像・動画サイズの設定

#bpy.context.scene.render.resolution_x = bpy.context.scene.render.resolution_x / 2
#bpy.context.scene.render.resolution_y = bpy.context.scene.render.resolution_y / 2
bpy.context.scene.render.resolution_x = 128
bpy.context.scene.render.resolution_y = 128
bpy.context.scene.render.resolution_percentage = 100

for i in range(16):
    #カメラ
    distance = 20
    rotation = 3/4 + i * 1/8
    bpy.data.objects["Camera"].location = ((distance-10) * math.cos(math.pi*(rotation - 1/2)), (distance-10) * math.sin(math.pi*(rotation - 1/2)), distance * math.cos(math.pi/4))
    bpy.data.objects["Camera"].rotation_euler = (math.pi/6, 0, rotation*math.pi)
    bpy.data.cameras["Camera"].lens = 10
    # 物理シミュレーション
    bpy.ops.ptcache.bake_all()


    # 画像・動画作成
    tar_dir = "output"
    if not os.path.isdir(tar_dir + str(i)):
        os.makedirs(tar_dir + str(i))
    file_name = os.path.join(tar_dir + str(i), datetime.now().isoformat().replace('.', '').replace(':', ''))
    # file_name_img = os.path.join(tar_dir_img + str(i), datetime.now().isoformat().replace('.', '').replace(':', ''))
    # bpy.ops.render.render()
    # bpy.data.images['Render Result'].save_render(filepath = file_name + ".png")

    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    bpy.data.scenes["Scene"].render.filepath = file_name + ".avi"

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 100
    # bpy.ops.render.render(animation=True)

    object_name = []
    object_locations = []
    for obj in bpy.data.objects:
       object_name.append(obj.name)
    for frame_nr in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end+1):
        object_location = []
        bpy.ops.render.render()
        bpy.context.scene.frame_set(frame_nr)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.visual_transform_apply()
        for obj in bpy.context.scene.objects:
            object_location.append(copy.copy(obj.location))
        object_locations.append(object_location)
        # bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(filepath = file_name + "_" + str(frame_nr) + ".png")
    with open(file_name + "data" + '.csv', 'w') as f:
       writer = csv.writer(f, lineterminator='\n')
       writer.writerow(object_name)
       writer.writerows(object_locations)

    # オブジェクトを表示
    for obj in bpy.data.objects:
        print(obj.name, "scale:", bpy.data.objects[obj.name].scale, "location:", bpy.data.objects[obj.name].location)

    # 保存
    savePath = os.path.abspath(os.path.dirname(__file__))
    bpy.path.relpath(savePath)
    bpy.ops.wm.save_as_mainfile(filepath=file_name + ".blend", relative_remap=True)
