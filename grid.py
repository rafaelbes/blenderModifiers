import bpy, bmesh, random

mesh = bpy.data.meshes.new(name="gridMesh")
obj = bpy.data.objects.new("gridObject",mesh)

scene = bpy.context.scene
scene.objects.link(obj)
scene.objects.active = obj
obj.select = True

mesh = bpy.context.object.data
bm = bmesh.new()

size = 7
ppl = 2*size+1
cv = 0
vertices = []
cy = 0
for i in range(-size, size+1):
    cx = 0
    sc = ppl*cy
    for j in range(-size, size+1):
        nv = bm.verts.new((i, j, 0))
        vertices.append(nv)
        nv.co[2] += random.random()
        if cy != 0 and cx != 0:
            print(cv, cv-ppl, cv-ppl-1, cv-1)
            bm.faces.new((vertices[cv], vertices[cv-ppl], vertices[cv-ppl-1], vertices[cv-1]))
        cx += 1
        cv += 1
    cy += 1



bm.to_mesh(mesh)  
bm.free()  # always do this when finished