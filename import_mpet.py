from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import bpy
from bpy_extras.image_utils import load_image
import os
import time

from .mpet import Mpet


def load_mpet(scene, file):
    dirname = os.path.dirname(file.name)
    filename = os.path.basename(file.name)

    model = Mpet()
    model.load(file)

    materials = []

    # Make materials for each texture.
    for texture in model.textures:
        tex = bpy.data.textures.new(texture.fn.decode('utf-8'), type='IMAGE')
        tex.image = load_image(texture.fn.decode('utf-8'), dirname)

        mat = bpy.data.materials.new('Material')

        mtex = mat.texture_slots.add()
        mtex.texture = tex
        mtex.texture_coords = 'UV'

        materials.append(mat)

    # Make meshes for each mesh.
    for mesh in model.meshes:
        bmesh = bpy.data.meshes.new(filename)

        # Flatten vertices down to [x,y,z,x,y,z...] array.
        verts = [[v.x, v.y, v.z] for v in mesh.vertices]
        verts = [coord for vert in verts for coord in vert]
        bmesh.vertices.add(len(mesh.vertices))
        bmesh.vertices.foreach_set("co", verts)

        # Polygons
        num_faces = len(mesh.polygons)
        bmesh.polygons.add(num_faces)
        bmesh.loops.add(num_faces * 3)
        faces = []
        for p in mesh.polygons:
            faces.extend((
                p.indices[0].index,
                p.indices[1].index,
                p.indices[2].index
            ))
        bmesh.polygons.foreach_set("loop_start", range(0, num_faces * 3, 3))
        bmesh.polygons.foreach_set("loop_total", (3,) * num_faces)
        bmesh.loops.foreach_set("vertex_index", faces)

        bmesh.validate()
        bmesh.update()

        obj = bpy.data.objects.new(filename, bmesh)
        scene.objects.link(obj)


def load(operator, context, filepath=""):
    time1 = time.clock()
    print('importing pangya model: %r' % (filepath))

    with open(filepath, 'rb') as file:
        load_mpet(context.scene, file)

    print('import done in %.4f sec.' % (time.clock() - time1))

    return {'FINISHED'}
