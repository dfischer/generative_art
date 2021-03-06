################################################################################
# code and images by Aaron Penne
# https://github.com/aaronpenne
################################################################################


################################################################################
# Imports
################################################################################

# Processing mode uses Python 2.7 but I prefer Python 3.x, pull in future tools
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

# Normal Python imports
import os
import sys
import shutil
import logging
from datetime import datetime
from collections import OrderedDict
from random import seed, shuffle, sample

################################################################################
# Globals
################################################################################

# Knobs to turn
w = 500
h = 500
max_frames = 10000

attractor = None
particles = []

use_seed = False
rand_seed = 578919

# Utility variables
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
script_ext = os.path.splitext(script_name)[1]
sketch_name = os.path.splitext(script_name)[0]

# Initialize random number generators with seed
if not use_seed:
    rand_seed = int(random(99999,9999999))
randomSeed(rand_seed)
noiseSeed(rand_seed)
seed(rand_seed)


################################################################################
# Helper methods
#
# These exist here in the script instead of a separate centralized file to
# preserve portability and ability to recreate image with a single script
################################################################################

# Standardizes log formats 
# ex. 2020-06-31 12:30:55 - INFO - log is better than print
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)

def make_dir(path):
  """Creates dir if it does not exist"""
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

def get_filename(counter):
  """Standardizes filename string format 
  ex. comet_12345_20200631_123055_001.png
  """
  return '{}_{}_{}_{:03d}.png'.format(sketch_name, rand_seed, timestamp, counter)

def save_graphic(pg=None, path='output', counter=0):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  if pg:
    pg.save(output_path)
  else:
    save(output_path)
  log.info('Saved to {}'.format(output_path))


def save_code(pg=None, path='output', counter=0):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  make_dir('archive_code')
  src = script_path
  dst = os.path.join('archive_code', output_file + script_ext)
  shutil.copy(src, dst)

def mousePressed():
  save_graphic(None, 'output', frameCount)


################################################################################
# Artwork methods
#
# where the fun actually starts
################################################################################

class Particle:
  def __init__(self, x, y, r=5):
    self.pos = PVector(x, y)
    self.vel = PVector(random(-5,5), random(-5,5))
    self.acc = PVector()
    self.vel_limit = 3000
    self.r = r
    self.c = color(0, 0, 100, 10)

  def move(self):
    self.pos.add(self.vel)

    # limits
    if self.vel.mag() <= self.vel_limit:
      self.vel.add(self.acc)

    """
    # handle x edges
    if self.pos.x > w+self.r:
      self.pos.x = -self.r
    elif self.pos.x < -self.r:
      self.pos.x = w+self.r

    # handle y edges
    if self.pos.y > h+self.r:
      self.pos.y = -self.r
    elif self.pos.y < -self.r:
      self.pos.y = h+self.r
    """

  def render_points(self):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    point(self.pos.x, self.pos.y)
    popStyle()

  def render_lines(self, target):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    line(self.pos.x, self.pos.y, target.x, target.y)
    popStyle()

  def attracted(self, target):
    force = PVector.sub(target, self.pos)
    dsquared = force.magSq()
    dsquared = constrain(dsquared, 25, 100)
    G = 100
    strength = G / dsquared
    force.setMag(strength)
    self.acc = force



################################################################################
# Setup
################################################################################

def setup():
  size(w, h)
  colorMode(HSB, 360, 100, 100, 100)
  background(0)
  frameRate(10)

  global attractor
  attractor = PVector(w/2 + w*0.2*cos(0), h/2 + h*0.2*sin(0))

  global particles
  for n in range(10):
    #particles.append(Particle(random(w), random(h)))
    particles.append(Particle(w/2+random(20,-20), h/2+random(-20,20)))

  save_code(None, 'output', frameCount)


################################################################################
# Draw
################################################################################

def draw():

  #background(0)

  pushStyle()
  stroke(231, 76, 60, 100)
  strokeWeight(10)
  attractor = PVector(w/2 + w*0.2*cos(frameCount*TAU/360), 
                      h/2 + h*0.2*sin(frameCount*TAU/360))
  #point(attractor.x, attractor.y)
  popStyle()

  for idx,p in enumerate(particles):
    p.attracted(attractor)
    p.move()
    #p.render_points()
    p.render_lines(attractor)

  if frameCount % 20 == 0:
    print(frameCount)
  if frameCount % max_frames == 0:
    exit()
