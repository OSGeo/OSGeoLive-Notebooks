
import numpy as np
from scipy import linalg
import math

def conforme(gcpD1, gcpD2, knowD1, output, verbose=False):
    L = np.loadtxt(str(gcpD1))
    A = np.zeros((2*L.shape[0],4),float)
    A[ ::2, 0] = 1.0
    A[1::2, 1] = 1.0
    A[ ::2, 2] = L[:,0]
    A[1::2, 2] = L[:,1]
    A[ ::2, 3] = L[:,1]
    A[1::2, 3] = -L[:,0]
    G = np.loadtxt(str(gcpD2))
    Y = np.zeros((2*G.shape[0],1),float)
    Y[ ::2, 0] = G[:,0]
    Y[1::2, 0] = G[:,1]
    N = np.dot(A.T.conj(), A)
    T = np.dot(A.T.conj(), Y)
    C = np.dot(linalg.inv(N), T)
    Lambda = abs(C[2]+C[3]*1j)
    Alpha = np.angle(C[2]+C[3]*1j)
    E0 = C[0]
    N0 = C[1]
    LX = np.loadtxt(str(knowD1))
    ss = LX.shape[0]
    pq = G.shape[0]
    ENglob = np.zeros((ss,2),float)
    lam = math.sqrt(C[2]** + C[3]**2)
    alp = np.arctan(C[3] / C[2]) / (math.pi / 180.)
    for i in np.arange(ss):
        E2 = E0+LX[i,0]*C[2]+LX[i,1]*C[3]
        N2 = N0+LX[i,1]*C[2]-LX[i,0]*C[3]
        ENglob[i,:] = np.hstack((E2,N2))
    np.savetxt(output, ENglob)
    sq = LX.shape[0]
    sqx = np.zeros((G.shape[0],1),float)
    sqy = np.zeros((G.shape[0],1),float)
    sqx[ ::1, 0] = G[:,0]
    sqy[::1, 0] = G[:,1]
    sizeq = sqx.shape[0]
    scartix = np.zeros((sizeq,1),float)
    scartiy = np.zeros((sizeq,1),float)
    scartiqx = np.zeros((sizeq,1),float)
    scartiqy = np.zeros((sizeq,1),float)
    sqm = np.zeros((sizeq,1),float)
    for i in np.arange(sizeq):
        Vx = E0 + LX[i,0] * C[2,0] + LX[i,1] * C[3,0] - sqx[i,0]
        Vy = N0 + LX[i,1] * C[2,0] - LX[i,0] * C[3,0] - sqy[i,0]
        sqmr = math.sqrt(Vx**2 + Vy**2)
        sqm[i,:] = sqmr
        scartiqx[i,0] = Vx**2
        scartiqy[i,0] = Vy**2
        scartix[i,0] = Vx
        scartiy[i,0] = Vy
    scartiq = np.concatenate((scartiqx,scartiqy))
    scarti = np.concatenate((scartix,scartiy))
    scartixy = np.concatenate((scartiqx,scartiqy),1)
    scartiqxy = np.concatenate((scartix,scartiy),1)
    sumscarti = sum(scartiq)
    varqp = sumscarti / ((2 * sizeq) - 4)
    varp = math.sqrt(varqp)
    varianzaq = varqp * linalg.inv(N)
    varianza = varp * linalg.inv(N)
    varqunitp = np.diag(varianzaq)
    varunitp = np.diag(varianza)
    prec = np.zeros((sq,2),float)
    for i in np.arange(sq):
        xx = math.sqrt((LX[i,0]**2) * (varqunitp[2]) + (LX[i,1]**2) * (varqunitp[3]) + varqunitp[0])
        yy = math.sqrt((LX[i,1]**2) * (varqunitp[2]) + (LX[i,0]**2) * (varqunitp[3]) + varqunitp[1])
        prec[i,:] = np.hstack((xx,yy))
    errore = np.concatenate((scartixy,scartiqxy,sqm),1)
    np.savetxt(output+str('_precision'), prec)
    np.savetxt(output+str('_error'), errore)
    err_med = sum(sqm) / pq
    a = C[2,0]
    b = C[3,0]
    lamvar = math.sqrt(((((2 * a) / math.sqrt(a**2 + b**2))**2) * varqunitp[2]) + ((((2 * b) / math.sqrt(a**2 + b**2))**2) * varqunitp[3]))
    alphavar = math.sqrt(((((-b / a**2) / (1 + (b / a)**2))**2) * varqunitp[2]) + (((1 / a) / (1 + (b / a)**2))**2 * varqunitp[3])) / (math.pi / 180.)
    results = str('Trasformation Parameters :\n')
    results += str("\n")
    results += str('Tx : ')+str(C[0,0])+'\n'
    results += str('Ty : ')+str(C[1,0])+'\n'
    results += str('Rigid Rotation : ')+str(alp)+'\n'
    results += str('Scale Factor  : ')+str(lam)+'\n'
    results += str("\n")
    results += str('Trasformation Parameters Variance :\n')
    results += str("\n")
    results += str('Sigma quadro Rigid Rotation :')+str(alphavar)+'\n'
    results += str('Sigma quadro Scale Factor:')+str(lamvar)+'\n'
    results += str("\n")
    results += str('Results : ')+str("\n")
    results += str(ENglob)
    results += '\n'
    results += str('Mean Error : ')+'\n'
    results += str(err_med)+'\n'
    results += '\n'
    results += str('Precision : ')+'\n'
    results += str(prec)
    results += '\n'
    results += str('Error : ')+str("\n")
    results += str(errore)
    results = results.replace('[','').replace(']','')
    if verbose:
        print(results)
    return ENglob

def affine(gcpD1, gcpD2, knowD1, output, verbose=False):
    L = np.loadtxt(str(gcpD1))
    A = np.zeros((2*L.shape[0],6),float)
    A[ ::2, 2] = 1.0
    A[1::2, 5] = 1.0
    A[ ::2, 0] = L[:,0]
    A[1::2, 4] = L[:,1]
    A[ ::2, 1] = L[:,1]
    A[1::2, 3] = L[:,0]
    G = np.loadtxt(str(gcpD2))
    Y = np.zeros((2*G.shape[0],1),float)
    Y[ ::2, 0] = G[:,0]
    Y[1::2, 0] = G[:,1]
    N = np.dot(A.T.conj(), A)
    T = np.dot(A.T.conj(), Y)
    C = np.dot(linalg.inv(N), T)
    E0 = C[2]
    N0 = C[5]
    LX = np.loadtxt(str(knowD1))
    ss = LX.shape[0]
    ENglob = np.zeros((ss,2),float)
    for i in np.arange(ss):
        E2 = E0+LX[i,0]*C[0]+LX[i,1]*C[1]
        N2 = N0+LX[i,0]*C[3]+LX[i,1]*C[4]
        ENglob[i,:] = np.hstack((E2,N2))
    np.savetxt(output,ENglob)
    sq = LX.shape[0]
    sqx = np.zeros((G.shape[0],1),float)
    sqy = np.zeros((G.shape[0],1),float)
    sqx[ ::1, 0] = G[:,0]
    sqy[::1, 0] = G[:,1]
    sizeq = sqx.shape[0]
    scartix = np.zeros((sizeq,1),float)
    scartiy = np.zeros((sizeq,1),float)
    scartiqx = np.zeros((sizeq,1),float)
    scartiqy = np.zeros((sizeq,1),float)
    sqm = np.zeros((sizeq,1),float)
    for i in np.arange(sizeq):
        Vx = E0 + LX[i,0] * C[0,0] + LX[i,1] * C[1,0] - sqx[i,0]
        Vy = N0 + LX[i,0] * C[3,0] + LX[i,1] * C[4,0] - sqy[i,0]
        sqmr = math.sqrt(Vx**2 + Vy**2)
        sqm[i,:] = sqmr
        scartiqx[i,0] = Vx**2
        scartiqy[i,0] = Vy**2
        scartix[i,0] = Vx
        scartiy[i,0] = Vx
    scartiq = np.concatenate((scartiqx,scartiqy))
    scarti = np.concatenate((scartix,scartiy))
    scartixy = np.concatenate((scartiqx,scartiqy),1)
    scartiqxy = np.concatenate((scartix,scartiy),1)
    sumscarti = sum(scartiq)
    varqp = sumscarti / ((2 * ss) - 4)
    varp = math.sqrt(varqp)
    varianzaq = varqp * linalg.inv(N)
    varianza = varp * linalg.inv(N)
    varqunitp = np.diag(varianzaq)
    varunitp = np.diag(varianza)
    prec = np.zeros((sq,2),float)
    for i in np.arange(sq):
        xx = math.sqrt((LX[i,0]**2) * (varqunitp[0]) + (LX[i,1]**2) * (varqunitp[1]) + varqunitp[2])
        yy = math.sqrt((LX[i,1]**2) * (varqunitp[0]) + (LX[i,0]**2) * (varqunitp[1]) + varqunitp[5])
        prec[i,:] = np.hstack((xx,yy))
    errore = np.concatenate((scartixy,scartiqxy,sqm),1)
    np.savetxt(output+str('_precision'), prec)
    np.savetxt(output+str('_error'), errore)
    err_med = sum(sqm) / sq		
    results = str('Trasformation Parameters :\n')
    results += str('Tx : ')+str(C[2,0])+'\n'
    results += str('Ty : ')+str(C[5,0])+'\n'
    results += str('Rigid Rotation X : ')+str(C[1,0])+'\n'
    results += str('Rigid Rotation Y : ')+str(C[3,0])+'\n'
    results += str('Scale Factor X : ')+str(C[0,0])+'\n'
    results += str('Scale Factor Y : ')+str(C[4,0])+'\n'
    results += '\n'
    results += str('Results : ')+'\n'
    results += str(ENglob)
    results += str("\n")
    results += str('Mean Error : ')+'\n'
    results += str(err_med)+'\n'
    results += '\n'
    results += str('Precision : ')+'\n'
    results += str(prec)+'\n'
    results += '\n'
    results += str('Error : ')+'\n'
    results += str(errore)
    results = results.replace('[','').replace(']','')
    if verbose:
        print(results)
    return ENglob

def vcross(v):
    x, y, z = v
    mat = np.zeros((3,3))
    mat[0] = [ 0, -z,  y]
    mat[1] = [ z,  0, -x]
    mat[2] = [-y,  x,  0]
    return mat
    

def block(v):
    return np.hstack((np.eye(3), -vcross(v), v[:, np.newaxis]))

def helmert(gcp1, gcp2, inputf, output, verbose=False):
    pt1 = np.loadtxt(str(gcp1))
    pt2 = np.loadtxt(str(gcp2))
    A = []
    rhs = []
    for i in range(3):
        A.append(block(pt1[i]))
        rhs.append((pt2[i] - pt1[i])[:, np.newaxis])
    A = np.vstack(A)
    rhs = np.vstack(rhs)
    sol = np.linalg.lstsq(A, rhs)[0]
    res = rhs - np.dot(A, sol)
    XYZ = np.loadtxt(str(inputf))
    XYZsize = XYZ.shape[0]
    ENZglob = np.zeros((XYZsize,3),float)
    for i in np.arange(XYZsize):
        X = sol[0] + (1 + sol[6]) * ( XYZ[i,0] - sol[5] * XYZ[i,1]  + sol[4] * XYZ[i,2] ) 
        Y = sol[1] + (1 + sol[6]) * ( sol[5] * XYZ[i,0] + XYZ[i,1] - sol[3] * XYZ[i,2] ) 
        Z = sol[2] + (1 + sol[6]) * ( -sol[4] * XYZ[i,0] + sol[3] * XYZ[i,1] + XYZ[i,2] ) 
        ENZglob[i,:] = np.hstack((X,Y,Z))
    np.savetxt(output,ENZglob)
    hresults = str('Trasformation Parameters :\n')
    hresults += str("\n")
    hresults = str('Traslation :\n')
    hresults += str("\n")
    hresults += str('Tx : ')+str(sol[0])+'\n'
    hresults += str('Ty : ')+str(sol[1])+'\n'
    hresults += str('Tz : ')+str(sol[2])+'\n'
    hresults += str("\n")
    hresults += str('Rotation :\n ')
    hresults += str("\n")
    hresults += str('Rx : ')+str(sol[3])+'\n'
    hresults += str('Ry : ')+str(sol[4])+'\n'
    hresults += str('Rz : ')+str(sol[5])+'\n'
    hresults += str("\n")
    hresults += str('Scale Factor  :\n ')
    hresults += str("\n")
    hresults += str("S : ")+str(sol[6])+'\n'
    hresults += str("\n")
    hresults += str('Trasformation Residuals :\n')
    hresults += str("\n")
    hresults += str(res)+'\n'
    hresults += str('Results : \n')
    hresults += str("\n")
    hresults += str(ENZglob)
    hresults += '\n'
    hresults = hresults.replace('[','').replace(']','')
    if verbose:
        print(hresults)
    return ENZglob