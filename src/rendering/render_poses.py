import sys
import argparse
import json
import bpy
import os


"""" --------------- CLI setup ------------- """
# CLI code from https://developer.blender.org/diffusion/B/browse/master/release/scripts/templates_py/background_job.py

# get the args passed to blender after "--", all of which are ignored by
# blender so scripts may receive their own arguments
argv = sys.argv

if "--" not in argv:
    argv = []  # as if no args are passed
else:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"

# When --help or no args are given, print this help
usage_text = (
    "Run blender in background mode with this script:"
    "  blender --background --python " + __file__ + " -- [options]"
)

parser = argparse.ArgumentParser(description=usage_text)

parser.add_argument('project_dir',
                    help='path to source code')

parser.add_argument('config_file',
                    help='json file specifying rendering parameters')

parser.add_argument('object_folder',
                    help='path to folder containing object files')

parser.add_argument('output_folder',
                    help='path to folder to which poses should be saved')

args = parser.parse_args(argv)

if not argv:
    parser.print_help()
    exit(-1)

print(args)


"""" --------------- Blender Setup ------------- """
# Ensure source directory in Blender python path
sys.path.append(os.path.join(args.project_dir))

import rendering.RenderInterface as Render

"""" --------------- Blender Setup ------------- """
with open(args.config_file) as config_file:
    config = json.load(config_file)

print(config)

#
# num_images = 1
#
# """ ************* User specified stuff here ************* """
# # required file paths for the script to run
# texture_path = 'D:\\PycharmProjects\\3DModels\\Ocado\\Halloumi\\Halloumi.jpg'
# obj_path = 'D:\\PycharmProjects\\3DModels\\Ocado\\Halloumi\\Halloumi.obj'
# render_folder = 'D:\\PycharmProjects\\3DModels\\Ocado\\Halloumi\\render'
#
# """
# Rendering with default parameters
# RenderInterface has a BlenderRandomScene obejct that controls
# random variables responsible for the scene. These random variables
# have distributions associated with them. Here we show how to render
# with the default distributions
# """
# RI = Render.RenderInterface(num_images=num_images)
# RI.load_subject(obj_path, texture_path, render_folder)
# RI.render_all(dump_logs = True)
#
# """
# Setting distribution parameters.
# One can change the distribution parameters of certain attributes
# in the rendering engine. This involves specifying the attribute
# that needs to be adjusted (as long as the attribute exists) and
# then specifying the parameter to tune.
#
# For instance num_lamps is varied according to the continuous
# uniform distribution U[l,r]. This makes l and r (the upper and lower
# bount of the U-distibution) tunable parameters
# For lamp energy, this is a truncated normal with parameters:
# {mu: mean, sigmu: sigma/mu, l: lower bound, r: upper bound}
# amd any of these can be tuned.
# """
# RI.set_attribute_distribution_params('num_lamps','l',5)
# RI.set_attribute_distribution_params('num_lamps','r',8)
# RI.set_attribute_distribution_params('lamp_energy','mu',500.0)
# RI.set_attribute_distribution_params('lamp_size','mu',5.)
# RI.set_attribute_distribution_params('camera_radius','sigmu',0.1)
# RI.render_all()
#
# """
# You could also change the distribution of an attribute entirely, by
# giving it a distribution name. This will be one of the distributions
# specified in RandomLib/random_render.py
# The function signature is as follows:
# RI.set_attribute_distribution(attr_name, dist=dist_name, kwargs)
# Where kwargs is a keyword argument dict of the required parameters
# for each distribution
# """
# RI.set_attribute_distribution('lamp_energy',{'dist':'UniformD','l':2000.0,'r':2400.0})
# RI.render_all()