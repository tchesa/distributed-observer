# classe que representa um ponto

import numpy as np
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import random

class Point:
  x = 0
  y = 0
  c = 'red'

  def __init__(self, x, y, c):
    self.x = x
    self.y = y
    self.c = c

  def __str__(self):
    return 'Point ({},{})[{}]'.format(self.x, self.y, self.c)
