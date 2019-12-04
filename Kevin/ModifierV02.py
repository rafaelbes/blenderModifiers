import bpy
import bmesh

verts = [(1, 1, 1), (0, 0, 0)]  # 2 verts made with XYZ coords
mesh = bpy.context.object.data
bm = bmesh.new()

# convert the current mesh to a bmesh (must be in edit mode)
bpy.ops.object.mode_set(mode='EDIT')
bm.from_mesh(mesh)
bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

reserva = bm.verts[:]
lista_para_faces = []

bm.verts.ensure_lookup_table()
print("Vértice Corno: x="+str(bm.verts[len(bm.verts)-1].co.x)+" y="+str(bm.verts[len(bm.verts)-1].co.y)+" z="+str(bm.verts[len(bm.verts)-1].co.z))


for i in reserva:
    bm.verts.ensure_lookup_table()
    print("Vértice base x="+str(i.co.x) + "  y=" + str(i.co.y) + " z=" + str(i.co.z))
    bm.verts.ensure_lookup_table()
    v1 = bm.verts.new((i.co.x + i.co.x/15, i.co.y + i.co.y/15, i.co.z))  # add a new vert
    lista_para_faces.append(v1)
    bm.verts.ensure_lookup_table()
    print("V1: x="+str(v1.co.x)+" y="+ str(v1.co.y)+" z="+ str(v1.co.z)+"\n")
    v2 = bm.verts.new((i.co.x + i.co.x/15, i.co.y + i.co.y/15, i.co.z + 0.05))
    lista_para_faces.append(v2)
    bm.verts.ensure_lookup_table()
    print("V2: x="+str(v2.co.x)+" y="+ str(v2.co.y)+" z="+ str(v2.co.z)+"\n")
    v3 = bm.verts.new((i.co.x - i.co.x/15, i.co.y - i.co.y/15, i.co.z))    
    lista_para_faces.append(v3)
    bm.verts.ensure_lookup_table()
    print("V3: x="+str(v3.co.x)+" y="+ str(v3.co.y)+" z="+ str(v3.co.z)+"\n")
    v4 = bm.verts.new((i.co.x - i.co.x/15, i.co.y - i.co.y/15, i.co.z + 0.05))
    lista_para_faces.append(v4)
    bm.verts.ensure_lookup_table()
    print("V4: x="+str(v4.co.x)+" y="+ str(v4.co.y)+" z="+ str(v4.co.z)+"\n")
    bm.edges.new((v1, v2))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v3, v4))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v1,v3))
    bm.verts.ensure_lookup_table()
    bm.edges.new((v2,v4))
    bm.verts.ensure_lookup_table()
    bm.verts.remove(i)

print("Tamanho do reserva: "+str(len(reserva)) + " Tamanho do lista_para_faces: " + str(len(lista_para_faces)))

for i in range(0,len(lista_para_faces),4):
    if i+7 > len(lista_para_faces):
        break
    if i == 0:
        bm.faces.new((lista_para_faces[i], lista_para_faces[i+1], lista_para_faces[i+3],lista_para_faces[i+2]))
    bm.faces.new((lista_para_faces[i+4], lista_para_faces[i+5], lista_para_faces[i+7], lista_para_faces[i+6]))        
    bm.faces.new((lista_para_faces[i+1], lista_para_faces[i+5], lista_para_faces[i+7], lista_para_faces[i+3]))
    bm.faces.new((lista_para_faces[i], lista_para_faces[i+4], lista_para_faces[i+6], lista_para_faces[i+2]))
    bm.faces.new((lista_para_faces[i], lista_para_faces[i+4], lista_para_faces[i+5], lista_para_faces[i+1]))
    bm.faces.new((lista_para_faces[i+6], lista_para_faces[i+2], lista_para_faces[i+3], lista_para_faces[i+7]))

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished