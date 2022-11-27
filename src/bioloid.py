import numpy as np
from numpy import pi, cos, sin

from matplotlib import pyplot as plt
import matplotlib.animation as animation

import robots as rbt
from robots import Robot

# def calcularangulo(i):
#     Q = [0,0,0]
#
#     angulo = ( (pi/2) / 50 ) * i
#     Q[0] = angulo
#     Q[1] = angulo
#     Q[2] = angulo
#     return Q
#
# def init():
#     ax.set_xlim3d((-limt, limt))
#     ax.set_xlabel('X')
#
#     ax.set_ylim3d((-limt, limt))
#     ax.set_ylabel('Y')
#
#     ax.set_zlim3d((-limt, limt))
#     ax.set_zlabel('Z')
#
#     ax.view_init(azim = 30, vertical_axis = 'y')
#
# def conservarax():
#     ax.set_xlim3d((-limt, limt))
#     ax.set_xlabel('X')
#
#     ax.set_ylim3d((-limt, limt))
#     ax.set_ylabel('Y')
#
#     ax.set_zlim3d((-limt, limt))
#     ax.set_zlabel('Z')
#
# def update(i):
#     ax.clear()
#     conservarax()
#
#     Q = calcularangulo(i)
#     bioloid.cadenas[0].cinematicadirecta(Q)
#
#     plt.plot(bioloid.cadenas[0].posfin[0], bioloid.cadenas[0].posfin[1], bioloid.cadenas[0].posfin[2], lw = 3, color = 'tab:red',
#              marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[0].nombre)
#
#     plt.plot(bioloid.cadenas[1].posfin[0], bioloid.cadenas[1].posfin[1], bioloid.cadenas[1].posfin[2], lw = 3, color = 'tab:red',
#             marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[1].nombre)
#
#Axes parametros
limt = 250
fuenteTam = 7

fig = plt.figure()
ax = fig.add_subplot(projection='3d', xlim=(-limt, limt), ylim=(-limt, limt), zlim=(-limt, limt))

ax.view_init(azim = 30, vertical_axis = 'y')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#Extraer robot
datos = rbt.extraerdatos('config/robot.yml')
robot = datos.get('bioloid')

bioloid = Robot(robot)

# Inicio

# Q = bioloid.cadenas[0].cinematicainversabrazo(214, 0, 14.5, 'arriba')
# print(Q)
# ln090 = np.linspace(0,pi/2,50)
Q = [np.pi/2, 0, 0]

bioloid.cadenas[1].cinematicadirecta(Q)
print( bioloid.cadenas[1].nombre )
print( bioloid.cadenas[1].A )

# print( bioloid.cadenas[0].posfin )

plt.plot(bioloid.cadenas[0].posfin[0], bioloid.cadenas[0].posfin[1], bioloid.cadenas[0].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[0].nombre)

plt.plot(bioloid.cadenas[1].posfin[0], bioloid.cadenas[1].posfin[1], bioloid.cadenas[1].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[1].nombre)

ax.legend(loc='upper left')

# ani = animation.FuncAnimation(fig, update, np.arange(50).reshape(50), init_func=init, interval = 100, repeat = False, fargs=())
#
plt.show()
