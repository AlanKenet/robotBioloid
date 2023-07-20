import numpy as np
from numpy import pi, cos, sin

from matplotlib import pyplot as plt
import matplotlib.animation as animation

import robots as rbt
from robots import Robot, Trayectoria

def mostrarmref(cadena,tipo):
    colores = ['red', 'navy', 'darkgreen']
    etiquetas = ['x', 'y', 'z']
    selector = np.identity(3)

    if tipo == 'completo':
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

    if tipo == 'final':
        i = cadena.gdl + 1

        for j in range(3):
                etiqueta = r'$%s$' % (etiquetas[j])

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

def obtenerangulos(i,gdl):
    Q = [0]*gdl

    for cc in range(gdl):
        Q[cc] = trayectoria.dq[cc,i]

    return Q

def init():
    ax.set_xlim3d((-limx, limx))
    ax.set_xlabel('X')

    ax.set_ylim3d((-limy, 160))
    ax.set_ylabel('Y')

    ax.set_zlim3d((-limz, limz))
    ax.set_zlabel('Z')

    # ax.view_init(azim = 30, vertical_axis = 'y')

def conservarax():
    ax.set_xlim3d((-limx, limx))
    ax.set_xlabel('X')

    ax.set_ylim3d((-limy, 160))
    ax.set_ylabel('Y')

    ax.set_zlim3d((-limz, limz))
    ax.set_zlabel('Z')

def graficarrobot(mostrarmr, tipo):
    plt.plot(bioloid.cadenas[0].posfin[0], bioloid.cadenas[0].posfin[1], bioloid.cadenas[0].posfin[2], lw = 3, color = 'tab:red',
         marker = 'o', markerfacecolor = 'plum', markeredgecolor = 'plum', label = bioloid.cadenas[0].nombre)

    plt.plot(bioloid.cadenas[1].posfin[0], bioloid.cadenas[1].posfin[1], bioloid.cadenas[1].posfin[2], lw = 3, color = 'tab:red',
             marker = 'o', markerfacecolor = 'palegreen', markeredgecolor = 'palegreen', label = bioloid.cadenas[1].nombre)

    plt.plot(bioloid.cadenas[2].posfin[0], bioloid.cadenas[2].posfin[1], bioloid.cadenas[2].posfin[2], lw = 3, color = 'tab:red',
             marker = 'o', markerfacecolor = 'lightslategray', markeredgecolor = 'lightslategray', label = bioloid.cadenas[2].nombre)

    plt.plot(bioloid.cadenas[3].posfin[0], bioloid.cadenas[3].posfin[1], bioloid.cadenas[3].posfin[2], lw = 3, color = 'tab:red',
             marker = 'o', markerfacecolor = 'coral', markeredgecolor = 'coral', label = bioloid.cadenas[3].nombre)

    plt.plot(bioloid.cadenas[0].posfin[0,0], bioloid.cadenas[0].posfin[1,0], marker = 'o', markerfacecolor = 'black', markeredgecolor = 'black')

    ax.legend(loc='upper left')

    if mostrarmr:
        for cc in range(4):
            mostrarmref(bioloid.cadenas[cc],tipo)

def update(i):
    ax.clear()
    conservarax()

    Q = obtenerangulos(i,3)

    bioloid.cadenas[0].cinematicadirecta(Q)

    bioloid.cadenas[0].obtenermref()

    graficarrobot(True, 'final')

#Axes parametros
limx = 220
limy = 306
limz = 220

fig = plt.figure()
ax = fig.add_subplot(projection='3d', xlim=(-limx, limx), ylim=(-limy, 160), zlim=(-limz, limz))

ax.view_init(azim = 30, vertical_axis = 'y')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#Extraer robot
datos = rbt.extraerdatos('config/robot.yml')
robot = datos.get('bioloid')

bioloid = Robot(robot)

#Parametros de trayectoria
puntos = np.array( ( [ -214,  0,  14.5],
                     [  -72,  0, 156.5],
                     [ -214,  0,  14.5]) )

intervalosdetiempo = np.array( [ 0,  10, 15 ] )

trayectoria = Trayectoria(bioloid.cadenas[0], puntos, intervalosdetiempo, 'lineal')

# Inicio

for i in range(4):
    if i < 2:
        Q = [0, 0, 0]
        v = 4
    else:
        Q = [0, 0, 0, 0, 0, 0]
        v = 7

    bioloid.cadenas[i].cinematicadirecta(Q)
    print( bioloid.cadenas[i].nombre )
    print( bioloid.cadenas[i].H[v] )

graficarrobot(True, 'final')

# ani = animation.FuncAnimation(fig, update, frames = len(trayectoria.dq[0]), init_func = init, interval = 100, repeat = True, fargs = ())

plt.show()
