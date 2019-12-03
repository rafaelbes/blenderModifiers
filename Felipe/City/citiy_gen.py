import bpy
import bmesh

import random

#configuracoes
c_precision = 0.01

width = 100
height = 100
radius = 20









centers = []

objs = bpy.context.selected_objects

for o in objs:
    centers.append( (o.location.x, o.location.y) )
    o.select = False




w = int(width/c_precision)*2
h =  int(height/c_precision)*2
collisions = [[0 for x in range(w)] for y in range(h)]


mesh = bpy.data.meshes.new("empty")
obj = bpy.data.objects.new("city",mesh)

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

#converte a coordenada em um indice na matriz de colisoes
def c_index(i):
    return int(i/c_precision + w/2)

#retorna 1 se houver alguma construcao na area passada por parametro
#retorna 0 caso contrario
def check_collision(x, y, w, h):
    col = 0
    for i in range(c_index(y), c_index(y+h)):
        for j in range(c_index(x), c_index(x+w)):
            if (collisions[i][j] == 1):
                col = 1
                break
            
        if (col == 1):
            break
        
            
    return col

def mark_region(x,y,w,h):
    for i in range(c_index(y), c_index(y+h)):
        for j in range(c_index(x), c_index(x+w)):
            collisions[i][j] = 1

#posiciona a base da construcao
def bulding_base(x, y, w, h):
    
    v4 = bm.verts.new((x,y,0))
    v3 = bm.verts.new((x,y+h,0))
    v2 = bm.verts.new((x+w,y+h,0))
    v1 = bm.verts.new((x+w,y,0))
    
    bm.verts.ensure_lookup_table()
    
    mark_region(x,y,w,h)
    
    bm.faces.new( (v1,v2,v3,v4) )

def random_placement(c_x,c_y):
    x = random.randint(c_index(c_x - radius), c_index(c_x + radius))
    y = random.randint(c_index(c_y - radius),c_index( c_y + radius))
    w = random.randint(2,5)
    h = random.randint(2,5)
    
    return (x,y,w,h)

def rise_building(f):
    pass

for c in centers:
    for i in range(10):
        x,y,w,h = random_placement(c[0],c[1])

        while (check_collision(x,y,w,h) == 1):
            x,y,w,h = random_placement(0,0)


        bulding_base(x,y,w,h)


bm.to_mesh(mesh)  
bm.free() 

#print(collisions[c_index(5)][c_index(10)])

#bpy.context.space_data.transform_orientation = 'NORMAL'
