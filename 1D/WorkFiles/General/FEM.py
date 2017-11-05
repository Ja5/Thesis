import math


def ShapeFunction(ElementType, x, derivative):
    if ElementType == 'LINE2':
        S = [0.0, 0.0]
        if derivative == 0:
            S[0] = (1 - x) / 2.0
            S[1] = (1 + x) / 2.0
        elif derivative == 1:
            S[0] = -0.5
            S[1] = 0.5
    elif ElementType == 'LINE3':
        S = [0.0, 0.0, 0.0]
        if derivative == 0:
            S[0] = x * (x - 1) / 2.0
            S[1] = x * (x + 1) / 2.0
            S[2] = (1.0 + x) * (1.0 - x)
        elif derivative == 1:
            S[0] = x - 0.5
            S[1] = x + 0.5
            S[2] = -2.0 * x

    return S


def getNodesperElement(ElementType):
    if ElementType == 'LINE2':
        return 2
    elif ElementType == 'LINE3':
        return 3
    else:
        print 'ERROR: not yet defined number of nodes for this element'
        return -1


def Jacobian(ElementType, eleCoordinates, xq):
    S = 0
    jac = 0.0
    nodesElement = getNodesperElement(ElementType)
    S = ShapeFunction(ElementType, xq, 1)
    for i in xrange(len(S)):
        jac = jac + eleCoordinates[i] * S[i]
    return jac


def InterpolateFEM(valueNodes, xq, ElementType):
    valInterpolated = 0.0
    S = ShapeFunction(ElementType, xq, 0)
    for i in xrange(len(valueNodes)):
        valInterpolated = valInterpolated + \
            valueNodes[i] * S[i]
    return valInterpolated


def ElementIntegral(valueNodes, degpolynomial, eleCoordinates, ElementType):
    val = 0.0
    qpoints = int(math.ceil((degpolynomial + 1) * 0.5))
    weigths, xq = GaussPoints(qpoints)
    if qpoints == 1:
        for i in xrange(qpoints):
            fx = InterpolateFEM(valueNodes, xq, ElementType)
            val = val + weigths * fx * \
                Jacobian(ElementType, eleCoordinates, xq)
    else:
        for i in xrange(qpoints):
            fx = InterpolateFEM(valueNodes, xq[i], ElementType)
            val = val + weigths[i] * fx * \
                Jacobian(ElementType, eleCoordinates, xq[i])
    return val


def GaussPoints(qPoints):
    if qPoints == 1:
        weigths = 2.0
        xq = 0.0
    elif qPoints == 2:
        weigths = [1.0, 1.0]
        xq = [-math.sqrt(1.0 / 3), math.sqrt(1.0 / 3)]
    elif qPoints == 3:
        weigths = [5.0 / 9, 8.0 / 9, 5.0 / 9]
        xq = [-math.sqrt(3.0 / 5), 0.0,  math.sqrt(3.0 / 5)]

    return weigths, xq


#******************************
#**********   MAIN   **********
#******************************

if __name__ == "__main__":
    # Interpolation
    valueNodes = [0, 10]

    xf = 0.5
    ElementType = 'LINE3'
    degpolynomial = 2
    eleCoordinates = []
    f = []

    import numpy as np

    # #-------TEST for LINE2 -> f(x)=x^2 for x in [0,10]
    # ElementType = 'LINE2'
    # NumberElements = 10
    # x = np.linspace(0,10,NumberElements+1)
    # for i in xrange(len(x)-1):
    #     eleCoordinates.append([float(x[i]), float(x[i+1])])
    #     f.append([float(pow(x[i],2)), float(pow(x[i+1],2))])
    #-------TEST for LINE3 -> f(x)=x^2 for x in [0,10]
    ElementType = 'LINE3'
    NumberElements = 10
    x = np.linspace(0, 10, NumberElements * 2 + 1)
    for i in xrange(NumberElements):
        eleCoordinates.append(
            [float(x[2 * i]), float(x[2 * i + 2]), float(x[2 * i + 1])])
        f.append([float(pow(x[2 * i], 2)), float(pow(x[2 * i + 2], 2)),
                  float(pow(x[2 * i + 1], 2))])

    # print 'eleCoordinates'
    # print eleCoordinates
    # print 'f'
    # print f

    # def SpatialIntegralFEM():
    valInt = 0
    for i in xrange(NumberElements):
        # Get Element coordinates -> eleCoordinates[i]
        # Get nodal values -> f[i]
        valInt = valInt + \
            ElementIntegral(f[i], degpolynomial,
                            eleCoordinates[i], ElementType)

    print valInt

    print 'fin'
