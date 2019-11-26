import bpy
import bmesh

import random


def rise(height):
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, height), "constraint_axis":(False, False, True), "constraint_orientation":'NORMAL', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='RANDOM', proportional_size=11.9182)
    

def sub_base(proportion):
    rise(0)
    bpy.ops.transform.resize(value=(proportion, proportion, proportion), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)




index = 6

obj = bpy.context.active_object
obj.data.polygons[index].select = True
bpy.ops.object.mode_set(mode = 'EDIT')

rise(2)
sub_base(0.6)
rise(1)
obj.data.polygons[index].select = False
#bpy.ops.mesh.select_all(action='TOGGLE')
#bpy.ops.mesh.normals_make_consistent(inside=False)
#bpy.ops.mesh.faces_shade_smooth()
#bpy.ops.mesh.vertices_smooth()
#bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.object.mode_set(mode = 'OBJECT')