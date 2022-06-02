# %%
import evolutivo_general
import funcion_objetivo

# %%
finalistas=evolutivo_general.algo_r8(rigideces_ideales={'axial':650,'radial':3500,'torsional':1350,'cardanic':12024.2294},
    tamano_poblacion=8000,
    medidas_fijas={'extRad':49,'intRad':32,'displacement':1.7904},
    generaciones=20,
    cr=.55,
    f=1.6,
    soluciones=5)

# %%
funcion_objetivo.funcion_objetivo_2(finalistas[0],{'axial':650,'radial':3500,'torsional':1350,'cardanic':12024.2294})


