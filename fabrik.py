#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Robótica Computacional - 
# Grado en Ingeniería Informática (Cuarto)
# Práctica: Resolución de la cinemática inversa mediante FABRIK

import sys
from math import *
import matplotlib.pyplot as plt

class Segment:
  def __init__(self, x1, y1, x2, y2):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

  def length(self):
    return dist([self.x1, self.y1], [self.x2, self.y2])
  
  def show(self, color='black'):
    plt.plot([self.x1, self.x2], [self.y1, self.y2], '-o', color=color)

#### COORDENADAS DE LAS ARTICULACIONES
x = [0,5,10,15]
y = [0,0,0,0]

T = []
for i in range(len(x) - 1):
  T.append(Segment(x[i], y[i], x[i+1], y[i+1]))

start = [x[0], y[0]]

L = max(T[-1].x2, T[-1].y2) + 10 # variable para representación gráfica
EPSILON = .01

# introducción del punto para la cinemática inversa
if len(sys.argv) != 3:
  sys.exit("python " + sys.argv[0] + " x y")
objetivo=[float(i) for i in sys.argv[1:]]

plt.clf()
plt.xlim(-L,L)
plt.ylim(-L,L)
for i in range(len(T)):
  T[i].show()
plt.plot(objetivo[0], objetivo[1], '*', color='lime')
plt.plot(start[0], start[1], 'o', color='orange')
plt.pause(0.0001)
plt.show(block=False)
input()

old_distance = 0
steps = 0
while(True):
  steps += 1
  # FORWARD REACHING
  obj = objetivo.copy()
  for i in range(len(T) - 1, -1, -1):
    obj_d = dist([obj[0], obj[1]], [T[i].x1, T[i].y1])
    joint_d = T[i].length()
    lambda_ = obj_d / joint_d
    
    T[i].x1 = obj[0] - (obj[0] - T[i].x1) / lambda_
    T[i].y1 = obj[1] - (obj[1] - T[i].y1) / lambda_

    T[i].x2 = obj[0]
    T[i].y2 = obj[1]

    obj = [T[i].x1, T[i].y1]


    plt.clf()
    plt.xlim(-L,L)
    plt.ylim(-L,L)
    for j in range(len(T)):
      T[j].show('black')
    T[i].show('red')
    plt.plot(start[0], start[1], 'o', color='orange')
    plt.plot(objetivo[0], objetivo[1], '*', color='lime')
    plt.pause(0.0001)
    plt.show(block=False)
    input()

  # BACKWARD REACHING
  obj = start.copy()
  for i in range(len(T)):
    obj_d = dist([obj[0], obj[1]], [T[i].x2, T[i].y2])
    joint_d = T[i].length()
    lambda_ = obj_d / joint_d
    
    T[i].x2 = obj[0] - (obj[0] - T[i].x2) / lambda_
    T[i].y2 = obj[1] - (obj[1] - T[i].y2) / lambda_

    T[i].x1 = obj[0]
    T[i].y1 = obj[1]

    obj = [T[i].x2, T[i].y2]

    plt.clf()
    plt.xlim(-L,L)
    plt.ylim(-L,L)
    for j in range(len(T)):
      T[j].show('black')
    T[i].show('red')
    plt.plot(start[0], start[1], 'o', color='orange')
    plt.plot(objetivo[0], objetivo[1], '*', color='lime')
    plt.pause(0.0001)
    plt.show(block=False)
    input()
  
  # Condición de parada
  distance = dist([T[-1].x2, T[-1].y2], objetivo)
  if distance < EPSILON * 10:
    print("Objetivo alcanzado en " + str(steps) + " ciclos")
    break
  if abs(old_distance - distance) < EPSILON:
    print("Convergencia en " + str(steps) + " ciclos")
    break
  old_distance = distance



