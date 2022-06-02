#Librerías.
import poblacion_inicial
import funcion_objetivo
import statistics
import cruce

#Ajustar alturas de la población.
def ajuste_h(poblacion):
    for i in poblacion:
        if i[4]>i[6]:
            i[4]=i[6]
    return poblacion
#Algoritmo completo.
def algo_r8(rigideces_ideales,tamano_poblacion,medidas_fijas,generaciones,cr,f,soluciones):
    poblacion=poblacion_inicial(tamano_poblacion,medidas_fijas)
    scores_inicial=[]
    for i in poblacion:
        scores_inicial.append(funcion_objetivo.funcion_objetivo_2(i,rigideces_ideales)[0])
    print('Error medio ponderado de la población inicial',statistics.mean(scores_inicial))
    for i in range(generaciones):
        poblacion_rankeada=cruce.rankear_poblacion(poblacion,rigideces_ideales)
        cuartetos=cruce.cuatro_padres(poblacion_rankeada,rigideces_ideales)
        lista_mutantes=cruce.mutantes(cuartetos,cr,f)
        for i2 in lista_mutantes:
            poblacion.append(i2)
        poblacion_rankeada=cruce.rankear_poblacion(poblacion,rigideces_ideales)
        poblacion=poblacion_rankeada[0:tamano_poblacion]
        scores_poblacion=[]
        for i2 in poblacion:
            scores_poblacion.append(funcion_objetivo.funcion_objetivo_2(i2,rigideces_ideales)[0])
        print('Generación',i+1,'completada con error medio ponderado',statistics.mean(scores_poblacion))
        poblacion=ajuste_h(poblacion)
    return poblacion[0:soluciones]