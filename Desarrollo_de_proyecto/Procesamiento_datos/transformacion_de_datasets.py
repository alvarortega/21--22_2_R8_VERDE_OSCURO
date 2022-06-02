# %%
import pandas as pd
import numpy as np
import mysql.connector
import pandas as pd

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_bruto'

# %%
def consulta_sql(sql):
    conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
    resultado = pd.read_sql(sql, conn)
    conn.close()
    return resultado

# %%
df_axial = consulta_sql('SELECT * FROM axial')
df_radial = consulta_sql('SELECT * FROM radial')
df_cardanic = consulta_sql('SELECT * FROM cardanica')
df_torsional = consulta_sql('SELECT * FROM torsional')

# %%
df_axial.drop_duplicates(inplace = True) 
df_cardanic.drop_duplicates(inplace = True) 
df_radial.drop_duplicates(inplace = True) 
df_torsional.drop_duplicates(inplace = True)

# %%
df_axial = df_axial[['extRad', 'intRad', 'jointRad', 'distRad', 'extH', 'radH', 'intH', 'displacement', 'stiffness']]
df_radial = df_radial[['extRad', 'intRad', 'jointRad', 'distRad', 'extH', 'radH', 'intH', 'displacement', 'stiffness']]
df_cardanic = df_cardanic[['extRad', 'intRad', 'jointRad', 'distRad', 'extH', 'radH', 'intH', 'displacement', 'stiffness']]
df_torsional = df_torsional[['extRad', 'intRad', 'jointRad', 'distRad', 'extH', 'radH', 'intH', 'displacement', 'stiffness']]


# %%
for df in['df_axial','df_radial','df_torsional','df_cardanic']:
    globals()[df]['fuerza']=globals()[df]['stiffness']*globals()[df]['displacement']

# %%
df_axial['pieza_id'] = df_axial.extRad.astype(str) + df_axial.intRad.astype(str) + df_axial.jointRad.astype(str) + df_axial.distRad.astype(str) + df_axial.extH.astype(str) + df_axial.radH.astype(str) + df_axial.intH.astype(str) 
df_radial['pieza_id'] = df_radial.extRad.astype(str) + df_radial.intRad.astype(str) + df_radial.jointRad.astype(str) + df_radial.distRad.astype(str) + df_radial.extH.astype(str) + df_radial.radH.astype(str) + df_radial.intH.astype(str) 
df_cardanic['pieza_id'] = df_cardanic.extRad.astype(str) + df_cardanic.intRad.astype(str) + df_cardanic.jointRad.astype(str) + df_cardanic.distRad.astype(str) + df_cardanic.extH.astype(str) + df_cardanic.radH.astype(str) + df_cardanic.intH.astype(str) 
df_torsional['pieza_id'] = df_torsional.extRad.astype(str) + df_torsional.intRad.astype(str) + df_torsional.jointRad.astype(str) + df_torsional.distRad.astype(str) + df_torsional.extH.astype(str) + df_torsional.radH.astype(str) + df_torsional.intH.astype(str) 


# %%
df_torsional['pieza_id'].nunique()

# %%
#df_axial.replace(df_axial['pieza_id'].unique(), value = range(len(df_axial['pieza_id'].unique())), inplace= True)
#df_radial.replace(df_radial['pieza_id'].unique(), value = range(len(df_radial['pieza_id'].unique())), inplace= True)
#df_cardanic.replace(df_cardanic['pieza_id'].unique(), value = range(len(df_cardanic['pieza_id'].unique())), inplace= True)
#df_torsional.replace(df_torsional['pieza_id'].unique(), value = range(len(df_torsional['pieza_id'].unique())), inplace= True)


# %%
df_radial = df_radial.reset_index()
df_axial = df_axial.reset_index()
df_torsional = df_torsional.reset_index()
df_cardanic = df_cardanic.reset_index()

# %%
df_radial = df_radial.drop(['index'], axis = 1)
df_axial = df_axial.drop(['index'], axis=1)
df_cardanic = df_cardanic.drop(['index'], axis=1)
df_torsional = df_torsional.drop(['index'], axis=1)

# %%
df_axial

# %%
df_radial

# %%
df_cardanic

# %%
df_torsional

# %%
df_axial.to_csv("../datos_transformados/df_axial.csv")
df_radial.to_csv("../datos_transformados/df_radial.csv")
df_cardanic.to_csv("../datos_transformados/df_cardanic.csv")
df_torsional.to_csv("../datos_transformados/df_torsional.csv")


# %%



