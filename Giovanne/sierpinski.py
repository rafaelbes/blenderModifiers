import bpy
import bmesh
from mathutils import Vector, Matrix
from math import sqrt
import itertools

def tetraedo(r=1, origin=(0, 0, 0)):
    # Pegando o vetor "central"
    origin = Vector(origin)

    #Formula pegada no http://mathworld.wolfram.com/RegularTetrahedron.html para formar um tetraedro
    #baseada no calculo da area,altura e raio
    area = 4*r/sqrt(6)
    h = area*sqrt(6)/3
    points = [( sqrt(3)*area/3,  0, -r/3), \
              (-sqrt(3)*area/6, -0.5*area, -r/3), \
              (-sqrt(3)*area/6,  0.5*area, -r/3), \
              (0, 0, sqrt(6)*area/3 - r/3)]

    points = [Vector(p) + origin for p in points]
    return points


def Sierpinski(bm, points, level=0):
    tetraedo = []
    #Adicionando os pontos medios de cada vetores
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[:i] + points[i + 1:]
        tetraedo.append([p1] + [(p1 + p)/2 for p in p2])
    #Criação recursiva dos tetraedros,no caso de o nivel ser maior que 0
    #Então aplica-se recursivamente em cada subTetraedo a partir do nivel 0
    if 0 < level:
        for subTetra in tetraedo:
            Sierpinski(bm, subTetra, level-1)
    else:
    #Ciração de faces e vertices utilizando o itertools para pegar o grupo de 3 em 3 vértices
        for subTetra in tetraedo:
            verts = [bm.verts.new(p) for p in subTetra]
            faces = [bm.faces.new(face) for face in itertools.combinations(verts, 3)]


if __name__ == '__main__':
    

    # Criãção do tetraedro frectal
    bm = bmesh.new()
    tetraedroOrigem = tetraedo(5)
    Sierpinski(bm, tetraedroOrigem, level=1)

    #Criação da malha e do objeto
    me = bpy.data.meshes.new("TetraedroMesh")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("Tetraedro", me)
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.update()