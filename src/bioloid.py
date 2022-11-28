import numpy as np
from numpy import pi, cos, sin

from matplotlib import pyplot as plt
import matplotlib.animation as animation

import robots as rbt
from robots import Robot

def mostrarmref(cadena):
    colores = ['red', 'navy', 'darkgreen']
    etiquetas = ['x', 'y', 'z']
    selector = np.identity(3)

    for i in range(cadena.gdl + 2):
        for j in range(3):
            etiqueta = r'$%s_%d$' % (etiquetas[j],i)

            ax.text(cadena.posmref[i, j, 0, 1]+ (2 * (i%3) * selector[j,0]),
                    cadena.posmref[i, j, 1, 1]+ (2 * (i%3) * selector[j,1]),
                    cadena.posmref[i, j, 2, 1]+ (2 * (i%3) * selector[j,2]),
                    etiqueta, size = 10, color = colores[j])

            ax.quiver(cadena.posmref[i, j, 0, 0],
                      cadena.posmref[i, j, 1, 0],
                      cadena.posmref[i, j, 2, 0],
                      cadena.posmref[i, j, 0, 1]-cadena.posmref[i, j, 0, 0],
                      cadena.posmref[i, j, 1, 1]-cadena.posmref[i, j, 1, 0],
                      cadena.posmref[i, j, 2, 1]-cadena.posmref[i, j, 2, 0],
                      color = colores[j])


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
#
#     bioloid.cadenas[0].cinematicadirecta(Q)
#
#     bioloid.cadenas[0].obtenermref()
#
#     plt.plot(bioloid.cadenas[0].posfin[0], bioloid.cadenas[0].posfin[1], bioloid.cadenas[0].posfin[2], lw = 3, color = 'tab:red',
#              marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[0].nombre)
#
#     plt.plot(bioloid.cadenas[1].posfin[0], bioloid.cadenas[1].posfin[1], bioloid.cadenas[1].posfin[2], lw = 3, color = 'tab:red',
#             marker = 'o', markerfacecolor = 'maroon', markeredgecolor = 'maroon', label = bioloid.cadenas[1].nombre)
#
#     mostrarmref(bioloid.cadenas[0])

#Axes parametros
limx = 220
limy = 465
limz = 220
fuenteTam = 7

fig = plt.figure()
ax = fig.add_subplot(projection='3d', xlim=(-limx, limx), ylim=(0, limy), zlim=(-limz, limz))

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
Q = [-pi/2, -pi/2, 0]
bioloid.cadenas[1].cinematicadirecta(Q)

print( bioloid.cadenas[1].nombre )
# print( np.shape(bioloid.cadenas[1].posmref) )
# print( bioloid.cadenas[1].posmref )

print( bioloid.cadenas[1].H )

plt.plot(bioloid.cadenas[0].posfin[0], bioloid.cadenas[0].posfin[1], bioloid.cadenas[0].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'plum', markeredgecolor = 'plum', label = bioloid.cadenas[0].nombre)

plt.plot(bioloid.cadenas[1].posfin[0], bioloid.cadenas[1].posfin[1], bioloid.cadenas[1].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'palegreen', markeredgecolor = 'palegreen', label = bioloid.cadenas[1].nombre)

plt.plot(bioloid.cadenas[2].posfin[0], bioloid.cadenas[2].posfin[1], bioloid.cadenas[2].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'lightslategray', markeredgecolor = 'lightslategray', label = bioloid.cadenas[2].nombre)

plt.plot(bioloid.cadenas[3].posfin[0], bioloid.cadenas[3].posfin[1], bioloid.cadenas[3].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'coral', markeredgecolor = 'coral', label = bioloid.cadenas[3].nombre)

ax.legend(loc='upper left')

# mostrarmref(bioloid.cadenas[2])

# ani = animation.FuncAnimation(fig, update, np.arange(50).reshape(50), init_func=init, interval = 100, repeat = False, fargs=())

plt.show()
