import numpy as np
from numpy import sin, cos

import yaml

class Robot:
    nombre = ''
    tipo = ''
    base = np.array( ( [1, 0, 0,   0],
                       [0, 1, 0,   0],
                       [0, 0, 1,   0],
                       [0, 0, 0,   1] ) )

    numerodecadenas = 0
    cadenas = []

    def __init__(self, datosrobot):
        self.datosrobot = datosrobot

        self.nombre = datosrobot.get('nombre')

        self.tipo = datosrobot.get('tipo')

        if datosrobot.get('base') != 'origen':
            self.base = datosrobot.get('base')

        self.numerodecadenas = datosrobot.get('numerodecadenas')

        self.crearcadenas( datosrobot.get('cadenas') )

    def crearcadenas(self, listadecadenas):

        for nombrecadena in listadecadenas:
            self.cadenas.append( CadenaCinematica( listadecadenas.get(nombrecadena) ) )

        self.cadenas = np.array(self.cadenas).reshape(self.numerodecadenas)

class CadenaCinematica:
    Apre = []
    A = []
    H = []
    posfin = []

    Aref = []
    posmref = []

    def __init__(self, datoscadena):
        self.datoscadena = datoscadena

        self.nombre = datoscadena.get('nombre')
        self.gdl = datoscadena.get('gdl')
        self.limites = datoscadena.get('limites')
        self.params = datoscadena.get('params')

        self.crearprelocales( self.params )

        self.calcularlocales( [0]*self.gdl )

        self.cinematicadirecta( [0]*self.gdl )

        self.crearlocalesmref()

        self.obtenermref()

    def crearprelocales(self, paramsdh):
        cantidad = paramsdh.get('cantidad')

        posiciontheta = paramsdh.get('posiciontheta')
        posiciontheta.insert(0,0)

        offset = paramsdh.get('offset')
        offset = np.deg2rad(offset)

        d = paramsdh.get('d')

        a = paramsdh.get('a')

        alpha = paramsdh.get('alpha')
        alpha = np.deg2rad(alpha)

        Adh = np.identity(4)
        Adh = np.array( [Adh] * cantidad )

        self.Apre = np.array( [ np.identity(4) ] * ( (2 * self.gdl) + 1 ) )

        for cc in range(cantidad):
            Adh[cc] = np.array( calcdh(offset[cc], d[cc], a[cc], alpha[cc]) )

            for cd in range( len(posiciontheta) ):
                if cc == posiciontheta[cd] - 1:
                    apos = (cd - 1) * 2
                    for ce in range(posiciontheta[cd-1], posiciontheta[cd]):
                        self.Apre[apos] = self.Apre[apos] @ Adh[ce]

                if (cc == cantidad - 1) and (cd == len(posiciontheta) - 1):
                    apos = cd * 2
                    self.Apre[apos] = self.Apre[apos] @ Adh[cc]
                    break

        self.Apre.reshape( ( (2 * self.gdl) + 1, 4, 4 ) )

    def calcularlocales(self, angulos):
        self.A = np.array( [np.identity(4)] * (self.gdl + 1) )

        for xi in range(self.gdl + 1):
            if xi != self.gdl:
                self.A[xi] = self.Apre[xi * 2] @ np.array( calcdh(angulos[xi], 0, 0, 0) )
            else:
                self.A[xi] = self.Apre[xi * 2]

    def cinematicadirecta(self, angulos):
        self.calcularlocales(angulos)

        self.H = np.array( [np.identity(4)] * (self.gdl + 2) )
        self.H[0] = Robot.base

        for xi in range(self.gdl + 1):
            self.H[xi+1] = self.H[xi] @ self.A[xi]

        self.H = np.around(self.H, 5)

        self.obtenerposiciones()

    def obtenerposiciones(self):
        self.posfin = np.zeros( ( 3, (self.gdl + 2) ) )

        for xi in range(self.gdl + 2):
            for xj in range(3):
                self.posfin[xj,xi] = self.H[xi,xj,3]

        self.posfin = np.around(self.posfin, 1)

    def cinematicainversabrazo(self, x, y, z, codo):
        if self.nombre == 'Brazo Izquierdo':
            v = cibi(x, y, z, codo)

        if self.nombre == 'Brazo Derecho':
            v = cibd(x, y, z, codo)

        return v

    def crearlocalesmref(self):
        tamref = 30
        self.Aref = np.array( [np.identity(4)]*3 )

        self.Aref[0] = np.array( calcdh(             0,      0, tamref, 0 ) )
        self.Aref[1] = np.array( calcdh(np.deg2rad(90),      0, tamref, 0 ) )
        self.Aref[2] = np.array( calcdh(             0, tamref,      0, 0 ) )

    def obtenermref(self):
        Href = np.array( [np.identity(4)] * 3 )
        self.posmref = np.zeros( (self.gdl + 2, 3, 3, 2) )

        for xi in range(self.gdl + 2):
            for xj in range(3):
                Href[xj] = self.H[xi] @ self.Aref[xj]

                for xk in range(3):
                    self.posmref[xi, xj, xk, 0] = self.H[xi,xk,3]
                    self.posmref[xi, xj, xk, 1] = Href[xj,xk,3]

class Trayectoria:
    nombrecadena = []
    puntos = []
    intervalosdetiempo = []
    interpolacion = []

    dt = 0.1

    q = []
    dq = []

    def __init__(self, cadena, puntos, intervalosdetiempo, interpolacion):
        self.nombrecadena = cadena.nombre
        self.puntos = puntos
        self.intervalosdetiempo = intervalosdetiempo
        self.interpolacion = interpolacion

        self.crearvaloresarticulares(cadena)

        self.dq = np.array( ([[]]*cadena.gdl) )

        self.creartrayectoria(cadena)

    def crearvaloresarticulares(self, cadena):
        for cc in range( len(self.puntos) ):
            self.q.append( cadena.cinematicainversabrazo(self.puntos[cc,0], self.puntos[cc,1], self.puntos[cc,2], 'arriba') )

        self.q = np.array(self.q)

    def creartrayectoria(self, cadena):
        for cc in range( len(self.puntos)-1 ):
            q = [[]]*cadena.gdl

            for cd in range(cadena.gdl):
                if self.interpolacion == 'lineal':
                    q[cd] = interpolacionlineal( self.q[cc,cd], self.q[cc+1,cd], self.intervalosdetiempo[cc], self.intervalosdetiempo[cc+1], self.dt )

            q = np.array(q).reshape(3,-1)
            self.dq = np.concatenate((self.dq, q), axis = 1)

            del q

        self.dq = np.around(self.dq,4)
        self.dq = self.dq.flatten()
        self.dq = self.dq.reshape(3,-1)

#Funciones
def extraerdatos(ubicacion):
    with open(ubicacion, 'r') as archivo:
        data = yaml.safe_load(archivo)
    return data

def calcdh(theta, d, a, alpha):

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
    t = np.around(t,5)
    return t

def cibi(x, y, z, codo):
        l0 = 47
        l1 = 25
        l2   = 14.5
        l3 = 67.5
        l4 = 74.5

        q1 = np.arctan2(-y,z)

        s = ( np.sqrt( (y**2) + (z**2) ) )- l2

        s = np.around(s,5)

        t = x - l0 - l1

        lmi = np.sqrt( (s**2) + (t**2) )
        lmi = np.around(lmi,5)

        c3 = ( (lmi**2) - (l3**2) - (l4**2) )/( 2 * l3 * l4 )
        c3 = np.around(c3,2)

        #Codo arriba
        if codo == 'arriba':
            q3 = np.arctan2( ( np.sqrt( 1 - (c3**2) ) ) , c3)


        #Codo abajo
        if codo == 'abajo':
            q3 = -np.arctan2( ( np.sqrt( 1 - (c3**2) ) ) , c3)


        gama1 = np.arctan2(s,t)

        gama2 = np.arctan2( ( l4 * sin(q3) ) , l3 + ( l4 * cos(q3) ) )

        q2 = -(gama1 + gama2)

        v = [q1,q2,q3]

        return v

def cibd(x, y, z, codo):
        l0 = 47
        l1 = 25
        l2 = 14.5
        l3 = 67.5
        l4 = 74.5

        q1 = np.arctan2(y,z)

        s = ( np.sqrt( (y**2) + (z**2) ) )- l2
        s = np.around(s,5)

        t = -x - l0 - l1

        lmd = np.sqrt( (s**2) + (t**2) )
        lmd = np.around(lmd,5)

        c3 = ( (lmd**2) - (l3**2) - (l4**2) )/( 2 * l3 * l4 )
        c3 = np.around(c3,2)

        #Codo arriba
        if codo == 'arriba':
            q3 = np.arctan2( ( np.sqrt( 1 - (c3**2) ) ) , c3)


        #Codo abajo
        if codo == 'abajo':
            q3 = -np.arctan2( ( np.sqrt( 1 - (c3**2) ) ) , c3)


        gama1 = np.arctan2(s,t)

        gama2 = np.arctan2( ( l4 * sin(q3) ) , l3 + ( l4 * cos(q3) ) )

        q2 = (gama1 - gama2)

        v = [q1,q2,q3]

        return v
def interpolacionlineal(qini, qfin, tini, tfin, dt):
        A = np.array( ( [tini, 1],
                        [tfin, 1]) )

        b = np.array( ( [qini],
                        [qfin]) )

        a = np.linalg.solve(A,b)

        muestras = np.arange(tini+dt, tfin+dt, dt)

        q = a[0] * muestras + a[1]
        q = np.array(q)

        return q