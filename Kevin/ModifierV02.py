import bpy
import bmesh

verts = [(1, 1, 1), (0, 0, 0)]  # 2 verts made with XYZ coords
mesh = bpy.context.object.data
bm = bmesh.new()

# convert the current mesh to a bmesh (must be in edit mode)
bpy.ops.object.mode_set(mode='EDIT')
bm.from_mesh(mesh)
bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

for i in range(len(bm.verts)):
    bm.verts.ensure_lookup_table()
    v1 = bm.verts.new((bm.verts[i].co.x + bm.verts[i].co.x/15, bm.verts[i].co.y + bm.verts[i].co.y/15, bm.verts[i].co.z))  # add a new vert
    bm.verts.ensure_lookup_table()
    v2 = bm.verts.new((bm.verts[i].co.x + bm.verts[i].co.x/15, bm.verts[i].co.y + bm.verts[i].co.y/15, bm.verts[i].co.z + 0.05))
    bm.verts.ensure_lookup_table()
    v3 = bm.verts.new((bm.verts[i].co.x - bm.verts[i].co.x/15, bm.verts[i].co.y - bm.verts[i].co.y/15, bm.verts[i].co.z))    
    bm.verts.ensure_lookup_table()
    v4 = bm.verts.new((bm.verts[i].co.x - bm.verts[i].co.x/15, bm.verts[i].co.y - bm.verts[i].co.y/15, bm.verts[i].co.z + 0.05))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v1, v2))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v3, v4))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v1,v3))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v2,v4))
    bm.verts.ensure_lookup_table()
    bm.verts.remove(bm.verts[i])

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished