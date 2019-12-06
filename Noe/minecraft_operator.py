import bpy
import math
import mathutils
import random

class Cube:
    
    def __init__(self):
        self.vertices = \
                    [
                        mathutils.Vector((0.5, 0.5, -0.5)),
                        mathutils.Vector((0.5, -0.5, -0.5)),
                        mathutils.Vector((-0.5, -0.5, -0.5)),
                        mathutils.Vector((-0.5, 0.5, -0.5)),
                        mathutils.Vector((0.5, 0.5, 0.5)),
                        mathutils.Vector((0.5, -0.5, 0.5)),
                        mathutils.Vector((-0.5, -0.5, 0.5)),
                        mathutils.Vector((-0.5, 0.5, 0.5))
                    ]
        self.faces = \
            [
                 [0, 1, 2, 3],
                 [4, 5, 6, 7],
                 [0, 4, 5, 1],
                 [1, 5, 6, 2],
                 [2, 6, 7, 3],
                 [4, 0, 3, 7]
             ]

def to_list_of_lists(vertex_list):
    cubeVertex = []
    for v in vertex_list:
        cubeVertex.append([v[0], v[1], v[2]])
    return cubeVertex

class MinecraftOperator(bpy.types.Operator):
    bl_idname = "object.minecraft_operator"
    bl_label = "Minecraft Operator"
    bl_options = {'REGISTER', 'UNDO'}
    my_string = bpy.props.StringProperty(name="String de referência", 
    default="20c-10d-20b-10e-20t-10d-20c-20f-10e-20t-10d-10e-20b-10d-20f")
    
    def execute(self, context):
        print("String: ", self.my_string)
        comands = self.my_string.split("-")
        scene = bpy.context.scene
        cube = Cube()
        NewMesh = bpy.data.meshes.new("CuboMesh")
        NewMesh.from_pydata(cube.vertices, [], cube.faces)
        NewMesh.update()
        NewObj = bpy.data.objects.new("Cubo", NewMesh)
        scene.objects.link(NewObj)
        scene.objects.active = NewObj
        cubes_positions = []
        cubes_positions.append(to_list_of_lists(cube.vertices))
        for comand in comands:
            try:
                qtd_cubes = int(comand[:-1])
                direction = comand[-1]
            except ValueError:
                try:
                    qtd_cubes = int(comand[:-2])
                    direction = comand[-2:]
                except ValueError:
                    qtd_cubes = int(comand[:-3])
                    direction = comand[-3:]
            for it in range(qtd_cubes):
                if(direction == "cfe" or direction == "cef" or direction == "efc" or direction == "ecf"
                or direction == "fec" or direction == "fce"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                        j[2] += 1
                elif(direction == "cfd" or direction == "cdf" or direction == "dcf" or direction == "dfc"
                or direction == "fcd" or direction == "fdc"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                        j[2] += 1
                elif(direction == "cte" or direction == "cet" or direction == "ect" or direction == "etc"
                or direction == "tce" or direction == "tec"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction == "ctd" or direction == "cdt" or direction == "dct" or direction == "dtc"
                or direction == "tcd" or direction == "tdc"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction == "bfe" or direction == "bef" or direction == "ebf" or direction == "efb"
                or direction == "feb" or direction == "fbe"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                        j[2] -= 1
                elif(direction == "bfd" or direction == "bdf" or direction == "dbf" or direction == "dfb"
                or direction == "fdb" or direction == "fbd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                        j[2] -= 1
                elif(direction == "bte" or direction == "bet" or direction == "ebt" or direction == "etb"
                or direction == "tbe" or direction == "teb"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                        j[2] -= 1
                elif(direction == "btd" or direction == "tdb" or direction == "dbt" or direction == "dtb"
                or direction == "bdt" or direction == "tbd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction[-2:] == "ce" or direction[-2:] == "ec"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[2] += 1
                elif(direction[-2:] == "cd" or direction[-2:] == "dc"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[2] += 1
                elif(direction[-2:] == "cf" or direction[-2:] == "fc"):
                    for j in cube.vertices:
                        j[1] += 1
                        j[2] += 1
                elif(direction[-2:] == "ct" or direction[-2:] == "tc"):
                    for j in cube.vertices:
                        j[1] -= 1
                        j[2] += 1
                elif(direction[-2:] == "be" or direction[-2:] == "eb"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[2] -= 1
                elif(direction[-2:] == "bd" or direction[-2:] == "db"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[2] -= 1
                elif(direction[-2:] == "bf" or direction[-2:] == "fb"):
                    for j in cube.vertices:
                        j[1] += 1
                        j[2] -= 1
                elif(direction[-2:] == "bt" or direction[-2:] == "tb"):
                    for j in cube.vertices:
                        j[1] -= 1
                        j[2] -= 1
                elif(direction[-2:] == "fe" or direction[-2:] == "ef"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                elif(direction[-2:] == "fd" or direction[-2:] == "df"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                elif(direction[-2:] == "te" or direction[-2:] == "et"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                elif(direction[-2:] == "td" or direction[-2:] == "dt"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] -= 1
                elif(direction[-1] == "e"):
                    for j in cube.vertices:
                        j[0] -= 1
                elif(direction[-1] == "d"):
                    for j in cube.vertices:
                        j[0] += 1
                elif(direction[-1] == "c"):
                    for j in cube.vertices:
                        j[2] += 1
                elif(direction[-1] == "b"):
                    for j in cube.vertices:
                        j[2] -= 1
                elif(direction[-1] == "f"):
                    for j in cube.vertices:
                        j[1] += 1
                elif(direction[-1] == "t"):
                    for j in cube.vertices:
                        j[1] -= 1
                if(to_list_of_lists(cube.vertices) not in cubes_positions):
                    NewMesh = bpy.data.meshes.new("CuboMesh")
                    NewMesh.from_pydata(cube.vertices, [], cube.faces)
                    NewMesh.update()
                    NewObj = bpy.data.objects.new("Cubo", NewMesh)
                    scene.objects.link(NewObj)
                    scene.objects.active = NewObj
                    cubes_positions.append(to_list_of_lists(cube.vertices))
        bpy.ops.object.select_all(action='DESELECT')
        objects = bpy.context.scene.objects
        for obj in objects:
            if obj.name.startswith("Cubo") :
                obj.select = True
        bpy.ops.object.join()

        return {'FINISHED'}

def layout(self, context):
    self.layout.operator(MinecraftOperator.bl_idname)

def register():
    bpy.utils.register_class(MinecraftOperator)
    bpy.types.VIEW3D_MT_object.append(layout)
    
def unregister():
    bpy.utils.unregister_class(MinecraftOperator)
    bpy.types.VIEW3D_MT_OBJECT.remove(layout)

if __name__ == '__main__':
    register()    