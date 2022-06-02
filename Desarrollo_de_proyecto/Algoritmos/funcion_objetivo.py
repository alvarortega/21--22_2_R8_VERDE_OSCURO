#Librerías.
import pickle
import numpy as np

#Cargar modelos predictivos.
modelo_axial=pickle.load(open('modelo_axial.pkl','rb'))
modelo_radial=pickle.load(open('modelo_radial.pkl','rb'))
modelo_torsional=pickle.load(open('modelo_torsional.pkl','rb'))
modelo_cardanic=pickle.load(open('modelo_cardanic.pkl','rb'))

#Función objetivo.
def funcion_objetivo_2(individuo,rigideces_ideales):
    error_axial=abs(rigideces_ideales['axial']-modelo_axial.predict(np.array(individuo).reshape(1,-1)))
    if error_axial>89.888:
        error_axial=error_axial*100
    error_radial=abs(rigideces_ideales['radial']-modelo_radial.predict(np.array(individuo).reshape(1,-1)))
    if error_radial>2080.1383:
        error_radial=error_radial*100
    error_torsional=abs(rigideces_ideales['torsional']-modelo_torsional.predict(np.array(individuo).reshape(1,-1)))
    if error_torsional>123565.2212:
        error_torsional=error_torsional*100
    error_cardanic=abs(rigideces_ideales['cardanic']-modelo_cardanic.predict(np.array(individuo).reshape(1,-1)))
    if error_cardanic>3580.7743:
        error_cardanic=error_cardanic*100
    return((.1*error_axial)+(.7*error_axial)+(.1*error_torsional)+(.1*error_cardanic))