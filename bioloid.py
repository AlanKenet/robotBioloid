import numpy as np
from numpy import pi, cos, sin

from matplotlib import pyplot as plt
# import matplotlib.animation as animation

def calcTH(paramsDH):
    theta = paramsDH[0]
    d = paramsDH[1]
    a = paramsDH[2]
    alpha = paramsDH[3]

    r_I = np.identity(3)

    r_theta = np.array( ([cos(theta), -sin(theta), 0],
                         [sin(theta),  cos(theta), 0],
                         [         0,           0, 1]) )

    r_alpha = np.array( ([1,          0,           0],
                         [0, cos(alpha), -sin(alpha)],
                         [0, sin(alpha),  cos(alpha)]) )

    p_0 = np.array( np.zeros( (3,1) ) )

    p_d = np.array( ([0], [0], [d]) )

    p_a = np.array( ([a], [0], [0]) )

    t_theta = np.vstack(  [np.hstack( [r_theta,p_0] ), np.array( [0, 0, 0, 1] ) ] )
    t_d     = np.vstack(  [np.hstack( [r_I,p_d] )    , np.array( [0, 0, 0, 1] ) ] )
    t_a     = np.vstack(  [np.hstack( [r_I,p_a] )    , np.array( [0, 0, 0, 1] ) ] )
    t_alpha = np.vstack(  [np.hstack( [r_alpha,p_0] ), np.array( [0, 0, 0, 1] ) ] )

    t = t_theta @ t_d @ t_a @ t_alpha

    return t,

GDL = 6

L = [20,20,20,20]

Q = [pi/4, pi/4, pi/4, pi/4, pi/4, pi/4]
# Q = [0, 0, 0, 0, 0, 0]
# Q = [pi/2, pi/2, pi/2, pi/2, pi/2, pi/2]

posFin = np.zeros( (3,GDL+1) )

#DH parametros = [theta, d,  a, alpha]
dH  = np.array([ [ Q[0], 0, 20,    0 ],
                 [ Q[1], 0, 20,    0 ],
                 [ Q[2], 0, 20,    0 ],
                 [ Q[3], 0, 20,    0 ],
                 [ Q[4], 0, 20,    0 ],
                 [ Q[5], 0, 20,    0 ], ])

A = np.zeros( (GDL, 4, 4) )

H = np.zeros( (GDL+1, 4, 4) )
H[0] = np.identity(4)

limt = 120

fuenteTam = 7

fig = plt.figure()
ax = fig.add_subplot(projection='3d', xlim=(-limt, limt), ylim=(-limt, limt), zlim=(-limt, limt))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

for i in range(GDL):
    A[i] = np.array( calcTH( dH[i] ) )

    H[i+1] = H[i] @ A[i]

    for j in range(3):
        posFin[j,i+1] = H[i+1,j,3]

plt.plot(posFin[0], posFin[1], posFin[2], lw = 2, color = 'indigo',
         marker = 'o', markerfacecolor = 'mediumpurple', markeredgecolor = 'mediumpurple')



posRef = np.zeros( (3, 3, 2) )

tamRef = 12

colores = ['red', 'gold', 'chartreuse']

ARef = np.zeros( (3, 4, 4) )
ARef[0] = np.array( calcTH( [     0,      0, tamRef, 0 ] ) )
ARef[1] = np.array( calcTH( [(pi/2),      0, tamRef, 0 ] ) )
ARef[2] = np.array( calcTH( [     0, tamRef,      0, 0 ] ) )

HRef = np.zeros( (3, 4, 4) )

for i in range(GDL):
    for j in range(3):
        HRef[j] = H[i+1] @ ARef[j]

        for k in range(3):
            posRef[j,k,0] = H[i+1,k,3]
            posRef[j,k,1] = HRef[j,k,3]

        plt.plot([posRef[j,0,0], posRef[j,0,1]],
                 [posRef[j,1,0], posRef[j,1,1]],
                 [posRef[j,2,0], posRef[j,2,1]], colores[j])



plt.show()
