import numpy as np
from numpy import pi, cos, sin

from matplotlib import pyplot as plt
# import matplotlib.animation as animation

def calcTH(paramsDH):
    a = paramsDH[0]
    alpha = paramsDH[1]
    d = paramsDH[2]
    theta = paramsDH[3]

    r_I = np.identity(3)

    r_theta = np.array( ([cos(theta), -sin(theta), 0],
                         [sin(theta),  cos(theta), 0],
                         [         0,           0, 1]) )

    r_alpha = np.array( ([1,          0,           0],
                         [0, cos(alpha), -sin(alpha)],
                         [0, sin(alpha),  cos(alpha)]) )

    p_0 = np.array( np.zeros( (3,1) ) )

    p_d = np.array( ([0],[0],[d]) )

    p_a = np.array( ([a],[0],[0]) )

    t_a     = np.vstack(  [np.hstack( [r_I,p_a] )    , np.array( [0, 0, 0, 1] ) ] )
    t_alpha = np.vstack(  [np.hstack( [r_alpha,p_0] ), np.array( [0, 0, 0, 1] ) ] )
    t_d     = np.vstack(  [np.hstack( [r_I,p_d] )    , np.array( [0, 0, 0, 1] ) ] )
    t_theta = np.vstack(  [np.hstack( [r_theta,p_0] ), np.array( [0, 0, 0, 1] ) ] )

    t = t_theta @ t_d @ t_a @ t_alpha

    return t,

GDL = 6

L = [20,20,20,20]

# Q = [pi/4, pi/4, pi/4, pi/4, pi/4, pi/4]
Q = [0, 0, 0, 0, 0, 0]
# Q = [pi/2, pi/2, pi/2, pi/2, pi/2, pi/2]

posFin = np.zeros( (3,GDL+1) )

dH  = np.array([ [    20,     0,    0,       Q[0] ],
                 [    20,     0,    0,       Q[1] ],
                 [    20,     0,    0,       Q[2] ],
                 [    20,     0,    0,       Q[3] ],
                 [    20,     0,    0,       Q[4] ],
                 [    20,     0,    0,       Q[5] ], ])
    
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

plt.plot(posFin[0],posFin[1],posFin[2],'o-',lw=2)



posRef = np.zeros( (3,3,2) )

tamRef = 10

colores = ['y', 'g', 'r']

ARef = np.zeros( (4, 4) )

ARef = np.array( calcTH( [tamRef, 0, 0, 0 ] ) ).reshape(4,4)

HRef = np.zeros( (3,4, 4) )

for i in range(GDL):
    HRef[0] = np.array( calcTH( [ dH[i,0],        dH[i,1], dH[i,2],        dH[i,3] ] ) )
    HRef[1] = np.array( calcTH( [ dH[i,0],        dH[i,1], dH[i,2], (pi/2)+dH[i,3] ] ) )
    HRef[2] = np.array( calcTH( [ dH[i,0], (pi/2)+dH[i,1], dH[i,2], (pi/2)+dH[i,3] ] ) )


    for j in range(2):
        print(HRef[j])
        print('')

        HRef[j] = H[i] @ HRef[j]

        HRef[j] = HRef[j] @ ARef

        # for k in range(3):
        #     posFin[j,i+1] = H[i+1,j,3]

    # plt.plot(posFin[0],posFin[1],posFin[2],'o-',lw=2)


    # for j in range(3):
    #     HRef = np.dot( H[k+1], ARef[j] )

    #     print(ARef[j])
    #     print(H[k+1])
    #     print(HRef)
    #     print('')

    #     for i in range(2):
    #         posRef[j,i] = [ H[k+1,j,3], HRef[i,3] ]

    #         print(H[k+1,j,3], HRef[i,3])
    #         print(posRef[j,i])
    #         print('')


    #     # print('')
    #     print(posRef[j])
    #     print('')
    #     print('')
    #     plt.plot([posRef[j,0,0], posRef[j,0,1]],
    #              [posRef[j,1,0], posRef[j,1,1]],
    #              [posRef[j,2,0], posRef[j,2,1]], colores[j])


plt.show()
