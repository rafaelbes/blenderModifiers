bl_info = {
            "name": "Create Spring",
            "category": "Object",            
}

import bpy
import bmesh
import math

class SpringGenerator(bpy.types.Operator):
    """Spring Generator"""
    bl_idname = "object.spring_generator"
    bl_label = "Spring Generator"
    bl_options = {'REGISTER', 'UNDO'}
    r = bpy.props.FloatProperty(name="Raio", default=2, min=1, max=20)
    grau = bpy.props.IntProperty(name="Tamanho do período em graus", default=360, min=0)
    max_z = bpy.props.FloatProperty(name="Altura maxima da mola", default=2)
    z = bpy.props.FloatProperty(name="Altura inicial", default=1)
    verts = bpy.props.IntProperty(name="Quantidade de vértices na mola", default=9, min=4)
    
    def execute(self,context):
    
        verts = []
        
        delta_z = self.max_z / self.verts 
        grau = self.grau
        r = self.r
        z = self.z
        parcial = math.floor(grau / self.verts)

        add = delta_z
        first = True
        j = 0

        for i in range(0,self.grau,parcial):
            verts.append( (r*math.cos(i*math.pi/100), r*math.sin(i*math.pi/100), z+delta_z) )
            delta_z += add
            if(first == True):
                first = False
                j = 0
                continue
            if(i == grau-1):
                continue
        

        mesh = bpy.data.meshes.new("empty")
        obj = bpy.data.objects.new("Spring",mesh)

        scene = bpy.context.scene
        scene.objects.link(obj)  # put the object into the scene (link)
        scene.objects.active = obj  # set as the active object in the scene
        obj.select = True  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()

        for v in verts:
            bm.verts.new(v)
        
        for j in range(0,len(bm.verts)-1):
            bm.verts.ensure_lookup_table()
            v1 = bm.verts[j]
            v2 = bm.verts[j+1]
            bm.edges.new((v1, v2))

        bm.to_mesh(mesh)  
        bm.free()
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SpringGenerator.bl_idname)
    
def register():
    bpy.utils.register_class(SpringGenerator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SpringGenerator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()