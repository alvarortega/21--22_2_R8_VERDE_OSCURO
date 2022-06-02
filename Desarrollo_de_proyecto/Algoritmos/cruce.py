#Librerías.
from funcion_objetivo import funcion_objetivo_2
import numpy as np
from random import uniform

#Rankear población por fitness.
def rankear_poblacion(poblacion,rigideces_ideales):
    fitness_poblacion=[]
    for i in poblacion:
        fitness_individuo=funcion_objetivo_2(i,rigideces_ideales)[0]
        fitness_poblacion.append(fitness_individuo)
    poblacion_fitness_indice=np.argsort(fitness_poblacion)
    return[poblacion[i]for i in poblacion_fitness_indice]
#Lista de cuartetos de padres.
def cuatro_padres(poblacion_rankeada,rigideces_ideales):
    fitness_rankeado=[funcion_objetivo_2(i,rigideces_ideales)for i in poblacion_rankeada]
    probabilidades_ruleta=[fitness_rankeado[i]/sum(fitness_rankeado)for i in range(len(fitness_rankeado))]
    probabilidades_ruleta=[np.cumsum(probabilidades_ruleta)]
    cuartetos=[]
    grupo_padres=[]
    for i in range(int(len(poblacion_rankeada)/4)):
        while len(grupo_padres)<4:
            flecha=uniform(0,1)
            indice_individuo_seleccionado=np.argmin([flecha>probabilidades_ruleta[i2]for i2 in range(len(probabilidades_ruleta))])
            if poblacion_rankeada[indice_individuo_seleccionado]not in grupo_padres:
                grupo_padres.append(poblacion_rankeada[indice_individuo_seleccionado])
        cuartetos.append(grupo_padres)
        grupo_padres=[]
    return cuartetos
#Descendencia. 
def mutantes(cuartetos,cr,f):
    lista_mutantes=[]
    for i in cuartetos:
        x,r1,r2,r3=i
        x=np.array(x)
        r1=np.array(r1)
        r2=np.array(r2)
        r3=np.array(r3)
        v=r1+(f*(r2-r3))
        y=[]
        u=[np.repeat(uniform(0,1),len(x))][0]
        for i in range(len(x)):
            if u[i]<=cr:
                y.append(v[i])
            else:
                y.append(x[i])
        lista_mutantes.append(y)
    return lista_mutantes