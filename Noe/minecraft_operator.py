import math
import bpy
import mathutils

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


    def set_new_coord(dx = 0, dy = 0, dz = 0):
        for vert in self.vertices:
            vert[0] += dx
            vert[1] += dy
            vert[2] += dz

class minecraftOperator(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.minecraf_operator"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Minecraft Operator"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    string = bpy.props.StringProperty(name="String de referência", description="Indica o número e a direção para criação dos cubos", 
                            default="10d-20c-10e-10e-20b-10d-20c-10b-10e-20d-10ce-10be-10bd-10cd-10cfe", 
                            maxlen=100, options={'ANIMATABLE'})

    def execute(self, context):        # execute() is called when running the operator.
        comands = string.split("-")
        scene = bpy.context.scene
        cube = Cube()
        NewMesh = bpy.data.meshes.new("CuboMeshe")
        NewMesh.from_pydata(cube.vertices, [], cube.faces)
        NewMesh.update()
        NewObj = bpy.data.objects.new("Cubo", NewMesh)
        scene.objects.link(NewObj)
        scene.objects.active = NewObj
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
                if(direction == "cfe"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                        j[2] += 1
                elif(direction == "cfd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                        j[2] += 1
                elif(direction == "cte"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction == "ctd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction == "bfe"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                        j[2] -= 1
                elif(direction == "bfd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                        j[2] -= 1
                elif(direction == "bte"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                        j[2] -= 1
                elif(direction == "btd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] -= 1
                        j[2] += 1
                elif(direction[-2:] == "ce"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[2] += 1
                elif(direction[-2:] == "cd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[2] += 1
                elif(direction[-2:] == "cf"):
                    for j in cube.vertices:
                        j[1] += 1
                        j[2] += 1
                elif(direction[-2:] == "ct"):
                    for j in cube.vertices:
                        j[1] -= 1
                        j[2] += 1
                elif(direction[-2:] == "be"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[2] -= 1
                elif(direction[-2:] == "bd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[2] -= 1
                elif(direction[-2:] == "bf"):
                    for j in cube.vertices:
                        j[1] += 1
                        j[2] -= 1
                elif(direction[-2:] == "bt"):
                    for j in cube.vertices:
                        j[1] -= 1
                        j[2] -= 1
                elif(direction[-2:] == "fe"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] += 1
                elif(direction[-2:] == "fd"):
                    for j in cube.vertices:
                        j[0] += 1
                        j[1] += 1
                elif(direction[-2:] == "te"):
                    for j in cube.vertices:
                        j[0] -= 1
                        j[1] -= 1
                elif(direction[-2:] == "td"):
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
                NewMesh = bpy.data.meshes.new("CuboMeshe")
                NewMesh.from_pydata(cube.vertices, [], cube.faces)
                NewMesh.update()
                NewObj = bpy.data.objects.new("Cubo", NewMesh)
                scene.objects.link(NewObj)
                scene.objects.active = NewObj

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def register():
    bpy.utils.register_class(minecraftOperator)


def unregister():
    bpy.utils.unregister_class(minecraftOperator)

if __name__ == "__main__":
   register()