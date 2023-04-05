import sympy as sp
import numpy as np
import math as mt

#performs a fast fourier transform with the required coefficients
def FastFourierTransform(Coeffs):
    if(not(mt.log(len(Coeffs), 2).is_integer())): #make sure length of input is a power of 2
        raise Exception("Please make your array length a power of 2")
    return FastFourierTransformHelper(Coeffs) #now we can let it actually compute

#helper for the Fast Fourier Transform
def FastFourierTransformHelper(Coeffs):
    n = len(Coeffs)
    if(n == 1):
        return Coeffs #down to the single point we were looking for, start resolving call stack
    rootOfUnity = sp.E ** ((2*sp.pi*sp.I) / n) #constant used to find nth root of unity
    evenCoeffs = Coeffs[::2] #take every other term starting from 0 (evens)
    oddCoeffs = Coeffs [1::2] #take every other term starting from 1 (odds)
    evenFunc = FastFourierTransformHelper(evenCoeffs) #recursively solve even function
    oddFunc = FastFourierTransformHelper(oddCoeffs) #recursively solve odd function
    result = [0] * n #make the resultant index, fill with zeros
    for i in range(int(n/2)):
        result[i] = evenFunc[i] + rootOfUnity**i * oddFunc[i]  #two calculations for price of one baby
        result[i + int(n/2)] = evenFunc[i] - rootOfUnity**i * oddFunc[i]  #two calculations for price of one baby
    return result

#performs an inverse Fast Fourier Transform with the given coefficients
def InverseFastFourierTransform(Coeffs):
    if(not(mt.log(len(Coeffs), 2).is_integer())): #make sure length of input is a power of 2
        raise Exception("Please make your array length a power of 2")
    partialRes = InverseFastFourierTransformHelper(Coeffs)
    return list(map(lambda x: x * (1/len(Coeffs)), partialRes)) #multiply every value by 1/n to account for inverse coefficient!

#helper for the Inverse Fast Fourier Transform
def InverseFastFourierTransformHelper(Coeffs):
    n = len(Coeffs)
    if(n == 1):
        return Coeffs #down to the single point we were looking for, start resolving call stack
    rootOfUnity = sp.E ** ((-2*sp.pi*sp.I) / n) #constant used to find nth root of unity, inverse of earlier matrix
    evenCoeffs = Coeffs[::2] #take every other term starting from 0 (evens)
    oddCoeffs = Coeffs [1::2] #take every other term starting from 1 (odds)
    evenFunc = InverseFastFourierTransformHelper(evenCoeffs) #recursively solve even function
    oddFunc = InverseFastFourierTransformHelper(oddCoeffs) #recursively solve odd function
    result = [0] * n #make the resultant index, fill with zeros
    for i in range(int(n/2)):
        result[i] = evenFunc[i] + rootOfUnity**i * oddFunc[i]  #two calculations for price of one baby
        result[i + int(n/2)] = evenFunc[i] - rootOfUnity**i * oddFunc[i]  #two calculations for price of one baby
    return result

if __name__ == "__main__":
    #time to test it out!
    testCoefficentForm = [3,2,1,0]
    print("Original:", testCoefficentForm)
    temp = FastFourierTransform(testCoefficentForm)
    print("After FFT:", temp)
    print(type(temp[0]))
    print("After IFFT:",InverseFastFourierTransform(temp))