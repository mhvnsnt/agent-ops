# Blender smoke check — runs inside `blender -b --python`.
# Proves the headless pipeline works: builds a default cube scene and renders
# one frame. Repos replace/augment this with their own checks (armature
# validation, T-pose framing, white-void background rules, proof thumbnails).
import bpy
import os
import sys

out = os.environ.get("BLENDER_SMOKE_OUT", "/tmp/blender_smoke.png")

# Clean slate, default cube
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))

# Camera + light so the render isn't black
bpy.ops.object.camera_add(location=(6, -6, 4), rotation=(1.1, 0, 0.785))
cam = bpy.context.object
bpy.context.scene.camera = cam
bpy.ops.object.light_add(type="SUN", location=(5, 5, 10))

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 8
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.film_transparent = False
scene.render.filepath = out
scene.render.image_settings.file_format = "PNG"

bpy.ops.render.render(write_still=True)

if not (os.path.exists(out) and os.path.getsize(out) > 0):
    print("BLENDER_SMOKE: FAIL — no output image", file=sys.stderr)
    sys.exit(1)
print(f"BLENDER_SMOKE: OK — rendered {os.path.getsize(out)} bytes to {out}")
