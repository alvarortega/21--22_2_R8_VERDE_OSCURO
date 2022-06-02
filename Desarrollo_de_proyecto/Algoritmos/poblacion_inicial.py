#Librerías.
from random import uniform

#Generar población inicial.
def poblacion_inicial(tamano_poblacion,medidas_fijas):
    poblacion=[]
    while len(poblacion)<tamano_poblacion:
        extRad=medidas_fijas['extRad']
        intRad=medidas_fijas['intRad']
        jointRad=uniform(1.5504,3)
        distRad=uniform(26.8955,48)
        extH=uniform(30.1237,36)
        radH=uniform(26.3289,27.8)
        intH=uniform(38.5548,50)
        displacement=medidas_fijas['displacement']
        individuo=[extRad,intRad,jointRad,distRad,extH,radH,intH,displacement]
        if individuo not in poblacion:
            poblacion.append(individuo)
    return poblacion