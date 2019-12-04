bl_info = {
            "name": "Skin4Springs",
            "category": "Object",            
}

import bpy
import bmesh


class Skin4Springs(bpy.types.Operator):
    """Skin4Spring Modifier"""
    bl_idname = "object.skin4springs"
    bl_label = "Skin4Springs"
    bl_options = {'REGISTER', 'UNDO'}
    
    frac = bpy.props.IntProperty(name="Fração", default=15, min=2)
    altura = bpy.props.FloatProperty(name="Altura dos paralelepípedos", default=0.05, min=0.01)

    def execute(self,context):
        
        mesh = bpy.context.object.data
        bm = bmesh.new()

        frac = self.frac
        altura = self.altura

        # convert the current mesh to a bmesh (must be in edit mode)
        bpy.ops.object.mode_set(mode='EDIT')
        bm.from_mesh(mesh)
        bpy.ops.object.mode_set(mode='OBJECT')  # return to object mode

        reserva = bm.verts[:]
        lista_para_faces = []

        bm.verts.ensure_lookup_table()
        #print("Vértice Corno: x="+str(bm.verts[len(bm.verts)-1].co.x)+" y="+str(bm.verts[len(bm.verts)-1].co.y)+" z="+str(bm.verts[len(bm.verts)-1].co.z))


        for i in reserva:
            bm.verts.ensure_lookup_table()
            #print("Vértice base x="+str(i.co.x) + "  y=" + str(i.co.y) + " z=" + str(i.co.z))
            bm.verts.ensure_lookup_table()
            v1 = bm.verts.new((i.co.x + i.co.x/frac, i.co.y + i.co.y/frac, i.co.z))  # add a new vert
            lista_para_faces.append(v1)
            bm.verts.ensure_lookup_table()
            #print("V1: x="+str(v1.co.x)+" y="+ str(v1.co.y)+" z="+ str(v1.co.z)+"\n")
            v2 = bm.verts.new((i.co.x + i.co.x/frac, i.co.y + i.co.y/frac, i.co.z + altura))
            lista_para_faces.append(v2)
            bm.verts.ensure_lookup_table()
            #print("V2: x="+str(v2.co.x)+" y="+ str(v2.co.y)+" z="+ str(v2.co.z)+"\n")
            v3 = bm.verts.new((i.co.x - i.co.x/frac, i.co.y - i.co.y/frac, i.co.z))    
            lista_para_faces.append(v3)
            bm.verts.ensure_lookup_table()
            #print("V3: x="+str(v3.co.x)+" y="+ str(v3.co.y)+" z="+ str(v3.co.z)+"\n")
            v4 = bm.verts.new((i.co.x - i.co.x/frac, i.co.y - i.co.y/frac, i.co.z + altura))
            lista_para_faces.append(v4)
            bm.verts.ensure_lookup_table()
            #print("V4: x="+str(v4.co.x)+" y="+ str(v4.co.y)+" z="+ str(v4.co.z)+"\n")
            bm.edges.new((v1, v2))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v3, v4))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v1,v3))
            bm.verts.ensure_lookup_table()
            bm.edges.new((v2,v4))
            bm.verts.ensure_lookup_table()
            bm.verts.remove(i)

        #print("Tamanho do reserva: "+str(len(reserva)) + " Tamanho do lista_para_faces: " + str(len(lista_para_faces)))

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
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(Skin4Springs.bl_idname)
    
def register():
    bpy.utils.register_class(Skin4Springs)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Skin4Springs)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()    