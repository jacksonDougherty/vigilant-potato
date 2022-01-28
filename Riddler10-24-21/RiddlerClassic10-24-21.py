import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import tplquad
from matplotlib.animation import FuncAnimation

def rightInequality(t1, t2):
    denominator = 2-t2-2*t1
    if denominator <= 0:
        return 1
    else:
        return 1 >= 2*t2/denominator*(1-2*t1)

def leftInequality(t1, t3):
    denominator = 2*t1-1+t3
    if denominator <= 0:
        return 1
    else:
        return 1 >= -2*(1-t3)/denominator*(1-2*t1)

def upperInequality(t2, t3):
    denominator = 1+t3-t2
    if denominator == 0:
        return 0
    else:
        return t3-0.5 <= (t2+t3-1)/denominator*t3

def centerInsideTriangle(t1, t2, t3):
    return int(rightInequality(t1, t2) and leftInequality(t1, t3) and upperInequality(t2, t3))

def symmetricalTriangle(t1, t2, t3):
    return int(leftInequality(t1, t2) and leftInequality(t2, t3) and leftInequality(t3, t1))

def parametrizedRight(t1, t2, x):
        return np.sqrt(3)*t2/(2-t2-2*t1)*(x-2*t1)

def parametrizedUpper(t2, t3, x):
    return ((t2+t3-1)/(1+t3-t2)*(x-1+t3)+1-t3)*np.sqrt(3)

def parametrizedLeft(t1, t3, x):
    return -np.sqrt(3)*(1-t3)/(2*t1+t3-1)*(x-2*t1)


def mainPlotTriangle():

    rng = np.random.default_rng(12345)
    t1 = rng.random()
    t2 = rng.random()
    t3 = rng.random()

    xVals = np.linspace(0,2,3)
    yValsUpper = parametrizedUpper(t2, t3, xVals)
    yValsRight = parametrizedRight(t1, t2, xVals)
    yValsLeft = parametrizedLeft(t1, t3, xVals)
    bottomEdge = [[0,2], [0,0]]
    rightEdge = [[2,1],[0,np.sqrt(3)]]
    leftEdge = [[1,0], [np.sqrt(3),0]]

    # Shows an example 
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(xVals, yValsRight, 'b', 
            xVals, yValsUpper, 'g', 
            xVals, yValsLeft, 'c', 
            bottomEdge[0], bottomEdge[1], 'r', 
            rightEdge[0], rightEdge[1], 'r', 
            leftEdge[0], leftEdge[1], 'r', 
            [1], [np.sqrt(3)/2], 'ko')

    ax.set_ylim([-0.25,2.0])

    plt.show()


def mainInequalitySlices():

    x = np.linspace(0, 1)
    y = np.linspace(0, 1)
    X, Y = np.meshgrid(x, y)
    xyBroadcast = np.broadcast(X, Y) 

    rightZ = np.empty(X.shape)
    rightZ.flat = [rightInequality(u,v) for (u,v) in xyBroadcast]

    xyBroadcast.reset()
    leftZ = np.empty(X.shape)
    leftZ.flat = [leftInequality(u,v) for (u,v) in xyBroadcast]

    xyBroadcast.reset()
    upperZ = np.empty(X.shape)
    upperZ.flat = [upperInequality(u,v) for (u,v) in xyBroadcast]

    plt.rcParams['text.usetex'] = True

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, constrained_layout=True)
    axs = [ax1, ax2, ax3]

    cs = axs[0].contourf(X, Y, rightZ, 1)
    axs[0].set_xlabel('$t_1$')
    axs[0].set_ylabel('$t_2$')
    axs[0].set_title('Right leg')

    cbar = fig.colorbar(cs)

    axs[1].contourf(X, Y, upperZ, 1)
    axs[1].set_xlabel('$t_2$')
    axs[1].set_ylabel('$t_3$')
    axs[1].set_title('Upper leg')

    axs[2].contourf(X, Y, leftZ, 1)
    axs[2].set_xlabel('$t_1$')
    axs[2].set_ylabel('$t_3$')
    axs[2].set_title('Left leg')

    plt.show()

def triangleEstimate():

    x = np.linspace(0, 1, 200)
    y = np.linspace(0, 1, 200)
    z = np.linspace(0, 1, 200)
    X, Y, Z= np.meshgrid(x, y, z)
    xyzBroadcast = np.broadcast(X, Y, Z)
    
    centerInside = np.empty(X.shape)
    centerInside.flat = [centerInsideTriangle(u, v, w) for (u, v, w) in xyzBroadcast]
#    centerInside.flat = [symmetricalTriangle(u, v, w) for (u, v, w) in xyzBroadcast]

    return np.sum(centerInside)/centerInside.size


def animateTriangles():

    class NewTriangle:
        def __init__(self, ax) -> None:
            self.lineRight, = ax.plot([], [], 'g')
            self.lineLeft, = ax.plot([], [], 'g')
            self.lineUpper, = ax.plot([], [], 'g')
            self.rng =  np.random.default_rng(12345)
            
        def __updateCoords(self):
            self.t1 = self.rng.random()
            self.t2 = self.rng.random()
            self.t3 = self.rng.random()
            self.leftCoordsX = [2*self.t1, 2-self.t2]
            self.leftCoordsY = [0, np.sqrt(3)*self.t2]
            self.upperCoordsX = [2-self.t2, 1-self.t3]
            self.upperCoordsY = [np.sqrt(3)*self.t2, np.sqrt(3)*(1-self.t3)]
            self.rightCoordsX = [1-self.t3, 2*self.t1]
            self.rightCoordsY = [np.sqrt(3)*(1-self.t3), 0]

        def __call__(self, i):
            self.__updateCoords()
            self.lineLeft.set_data(self.leftCoordsX, self.leftCoordsY)
            self.lineUpper.set_data(self.upperCoordsX, self.upperCoordsY)
            self.lineRight.set_data(self.rightCoordsX, self.rightCoordsY)
            if centerInsideTriangle(self.t1, self.t2, self.t3):
                self.lineLeft.set_color('g')
                self.lineUpper.set_color('g')
                self.lineRight.set_color('g')
            else:
                self.lineLeft.set_color('r')
                self.lineUpper.set_color('r')
                self.lineRight.set_color('r')
            return [self.lineLeft, self.lineRight, self.lineUpper]

    fig, ax = plt.subplots()
    ax.plot([0, 2, 1, 0], [0, 0, np.sqrt(3), 0], 'k', 
            [1], [np.sqrt(3)/2], 'ko')
    
    triFrame = NewTriangle(ax)
    anim = FuncAnimation(fig, triFrame, frames = 50, interval = 400, blit=True, repeat=False)
    plt.show()

    return anim

# mainPlotTriangle()
mainInequalitySlices()
# print(triangleEstimate())
# Probability Estimate = 0.4105 using 200^3 point grid 

#print(tplquad(centerInsideTriangle, 0, 1, lambda x: 0, lambda x: 1, lambda x, y: 0, lambda x, y: 1))
# Python integrator is pretty bad at integrating discontinuous functions like this characteristic function

# animateTriangles()
