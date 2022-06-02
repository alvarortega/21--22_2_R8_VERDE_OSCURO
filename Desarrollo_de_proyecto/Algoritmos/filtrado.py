# %%
# ! pip install -U kaleido

# %%
import pandas as pd
import numpy as np

# Importamos Plotly Express para realizar graficos.
import plotly.express as px 
# import os
# import kaleido


# %%
import mysql.connector
import pandas as pd

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_prep'

# %%
def consulta_sql(sql):
    conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
    resultado = pd.read_sql(sql, conn)
    conn.close()
    return resultado

# %%
axial = consulta_sql('SELECT * FROM axial')
radial = consulta_sql('SELECT * FROM radial')
cardanic = consulta_sql('SELECT * FROM cardanica')
torsional = consulta_sql('SELECT * FROM torsional')

# %% [markdown]
# ### Cargar.

# %%
axial

# %% [markdown]
# Ids de piezas.

# %%
axial['medida']='axial'
radial['medida']='radial'
torsional['medida']='torsional'
cardanic['medida']='cardanic'

# %%
df=axial
df=df.append(radial)
df=df.append(torsional)
df=df.append(cardanic)

# %%
df.replace(df['pieza_id'].unique(),value=range(1,len(df['pieza_id'].unique())+1),inplace=True)

# %%
#Volver a separar.
axial_df=df[df['medida']=='axial'] 
radial_df=df[df['medida']=='radial']
torsional_df=df[df['medida']=='torsional']
cardanic_df=df[df['medida']=='cardanic']
for df in['axial_df','radial_df','torsional_df','cardanic_df']:
    if'medida'in globals()[df].columns:
        del globals()[df]['medida']

# %% [markdown]
# Calcular pendiente.

# %%
def calcular_pendiente(df,iteracion):
    if iteracion==0:
        return df.iloc[iteracion]['fuerza']/df.iloc[iteracion]['displacement']
    else:
        dif_fuerza=df.iloc[iteracion]['fuerza']-df.iloc[iteracion-1]['fuerza']
        dif_desplazamiento=df.iloc[iteracion]['displacement']-df.iloc[iteracion-1]['displacement']
        resul= dif_fuerza/dif_desplazamiento
        if resul!=np.inf:
            return resul

# %%
for df in['axial_df','radial_df','torsional_df','cardanic_df']:
    globals()[df]['pendiente']=0

# %%
#Axial.
df_axial=pd.DataFrame()
for pieza_unica in axial_df['pieza_id'].unique():
    df_pieza_axial=axial_df[axial_df['pieza_id']==pieza_unica].reset_index()
    for iteracion in range(1,len(df_pieza_axial)+1):
        df_pieza_axial['pendiente'][iteracion-1]=calcular_pendiente(df_pieza_axial,iteracion-1)
    df_axial=df_axial.append(df_pieza_axial)
    df_axial.reset_index()

# %%
#Radial.

df_radial=pd.DataFrame()
for pieza_unica in radial_df['pieza_id'].unique():
    df_pieza_radial=radial_df[radial_df['pieza_id']==pieza_unica].reset_index()
    for iteracion in range(1,len(df_pieza_radial)+1):
        #if calcular_pendiente(df_pieza_radial,iteracion-1)== np.Inf:
         #   print('pieza',pieza_unica)
          #  print(iteracion)
       # lista.append(calcular_pendiente(df_pieza_radial,iteracion-1))
        df_pieza_radial['pendiente'][iteracion-1]=calcular_pendiente(df_pieza_radial,iteracion-1)
    df_radial=df_radial.append(df_pieza_radial)
    df_radial.reset_index()


# %%
#Torsional.
df_torsional=pd.DataFrame()
for pieza_unica in torsional_df['pieza_id'].unique():
    df_pieza_torsional=torsional_df[torsional_df['pieza_id']==pieza_unica].reset_index()
    for iteracion in range(1,len(df_pieza_torsional)+1):
        df_pieza_torsional['pendiente'][iteracion-1]=calcular_pendiente(df_pieza_torsional,iteracion-1)
    df_torsional=df_torsional.append(df_pieza_torsional)
    df_torsional.reset_index()

# %%
#Cardánica.
df_cardanic=pd.DataFrame()
for pieza_unica in cardanic_df['pieza_id'].unique():
    df_pieza_cardanic=cardanic_df[cardanic_df['pieza_id']==pieza_unica].reset_index()
    for iteracion in range(1,len(df_pieza_cardanic)+1):
        df_pieza_cardanic['pendiente'][iteracion-1]=calcular_pendiente(df_pieza_cardanic,iteracion-1)
    df_cardanic=df_cardanic.append(df_pieza_cardanic)
    df_cardanic.reset_index()

# %%
df_cardanic.dropna(inplace=True)
df_cardanic.pendiente.isna().sum()

# %%
df_radial.dropna(inplace=True)
df_radial.pendiente.isna().sum()

# %%
df_torsional.dropna(inplace=True)
df_torsional.pendiente.isna().sum()

# %%
for df in['df_axial','df_radial','df_torsional','df_cardanic']:
    globals()[df]['diferencia']=0

# %%
#Axial.

df_axial2=pd.DataFrame()
for id in df_axial['pieza_id'].unique():
    df_pieza=df_axial[df_axial.pieza_id== id]
    for iteracion in range(1,len(df_pieza)+1):
        if (iteracion-1)==0:
            df_pieza['diferencia'][iteracion-1]= 0
        else:
            df_pieza['diferencia'][iteracion-1]=abs(df_pieza.iloc[iteracion-1]['pendiente']-df_pieza.iloc[iteracion-2]['pendiente'])
        #print(df_pieza['diferencia'][iteracion-1])
    df_axial2=df_axial2.append(df_pieza)
    df_axial2.reset_index()
df_axial2.head(5)
        
            


# %%
#Radial.

df_radial2=pd.DataFrame()
for id in df_radial['pieza_id'].unique():
    df_pieza=df_radial[df_radial.pieza_id== id]
    for iteracion in range(1,len(df_pieza)+1):
        if (iteracion-1)==0:
            df_pieza['diferencia'][iteracion-1]= 0
        else:
            df_pieza['diferencia'][iteracion-1]=abs(df_pieza.iloc[iteracion-1]['pendiente']-df_pieza.iloc[iteracion-2]['pendiente'])
        #print(df_pieza['diferencia'][iteracion-1])
    df_radial2=df_radial2.append(df_pieza)
    df_radial2.reset_index()
df_radial2.head(5)
        

# %%
#Cardanic.

df_cardanic2=pd.DataFrame()
for id in df_cardanic['pieza_id'].unique():
    df_pieza=df_cardanic[df_cardanic.pieza_id== id]
    for iteracion in range(1,len(df_pieza)+1):
        if (iteracion-1)==0:
            df_pieza['diferencia'][iteracion-1]= 0
        else:
            df_pieza['diferencia'][iteracion-1]=abs(df_pieza.iloc[iteracion-1]['pendiente']-df_pieza.iloc[iteracion-2]['pendiente'])
        #print(df_pieza['diferencia'][iteracion-1])
    df_cardanic2=df_cardanic2.append(df_pieza)
    df_cardanic2.reset_index()
df_cardanic2.head(5)

# %%
#Torsional.

df_torsional2=pd.DataFrame()
for id in df_torsional['pieza_id'].unique():
    df_pieza=df_torsional[df_torsional.pieza_id== id]
    for iteracion in range(1,len(df_pieza)+1):
        if (iteracion-1)==0:
            df_pieza['diferencia'][iteracion-1]= 0
        else:
            df_pieza['diferencia'][iteracion-1]=abs(df_pieza.iloc[iteracion-1]['pendiente']-df_pieza.iloc[iteracion-2]['pendiente'])
        #print(df_pieza['diferencia'][iteracion-1])
    df_torsional2=df_torsional2.append(df_pieza)
    df_torsional2.reset_index()
df_torsional2.head(5)

# %%
df_torsional2.pendiente.describe()

# %%
df_torsional2

# %% [markdown]
# ### Visualización de los datos

# %%
# Line plot Axial
fig1 = px.line(
    df_axial2,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig1.update_layout(
        title = 'Desplazamiento por fuerza (Axial)'
    )

fig1.show()

# %%
# Line plot Torsional
fig2 = px.line(
    df_torsional2,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig2.update_layout(
        title = 'Desplazamiento por fuerza (Torsional)'
    )

fig2.show()

# %%
# Line plot Radial
fig3 = px.line(
    df_radial2,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig3.update_layout(
        title = 'Desplazamiento por fuerza (Radial)'
    )

fig3.show()

# %%
# Line plot Cardanic
fig4 = px.line(
    df_cardanic2,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig4.update_layout(
        title = 'Desplazamiento por fuerza (Cardanic)'
    )

fig4.show()

# %% [markdown]
# ### Definir el umbral

# %%
#Radial.

radial2_descriptivos=pd.DataFrame()
for id in df_radial2['pieza_id'].unique():
    df_pieza=df_radial2[df_radial2.pieza_id== id] 
    for iteracion in range(1,len(df_pieza)+1):
        descrive = df_pieza['diferencia'].describe()
        radial2_descriptivos=radial2_descriptivos.append(descrive)
        radial2_descriptivos.reset_index()

# %%
radial2_descriptivos.mean()

# %%
#Cardanic.

cardanic2_descriptivos=pd.DataFrame()
for id in df_cardanic2['pieza_id'].unique():
    df_pieza=df_cardanic2[df_cardanic2.pieza_id== id]
    for iteracion in range(1,len(df_pieza)+1):
        descrive = df_pieza['diferencia'].describe()
        cardanic2_descriptivos=cardanic2_descriptivos.append(descrive)
        cardanic2_descriptivos.reset_index()

# %%
cardanic2_descriptivos.mean()

# %%
#Torsional.

torsional2_descriptivos=pd.DataFrame()
for id in df_torsional2['pieza_id'].unique():
    df_pieza=df_torsional2[df_torsional2.pieza_id== id]
    descrive = df_pieza['diferencia'].describe()
    torsional2_descriptivos=torsional2_descriptivos.append(descrive)
    torsional2_descriptivos.reset_index()

# %%
torsional2_descriptivos.mean()

# %%
np.percentile(torsional2_descriptivos, 25)

# %% [markdown]
# ### Borrado de filas

# %%
df_torsional2.describe()

# %%
#Torsional.

df_torsional3=pd.DataFrame()
for id in df_torsional2.pieza_id.unique():
    df_pieza=df_torsional2[df_torsional2.pieza_id== id]
    descrip=df_pieza.describe()['diferencia']
    condicion=False
    for index,row in df_pieza.iterrows():
        if condicion==False:
            if row['diferencia']>df_pieza['diferencia'].quantile(0.65):
                df_pieza.drop(index,inplace=True)
                condicion=True
        else:
            df_pieza.drop(index,inplace=True)
    df_torsional3=df_torsional3.append(df_pieza) 

# %%
# Line plot Torsional
fig1 = px.line(
    df_torsional3,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig1.update_layout(
        title = 'Desplazamiento por fuerza lineal (Torsional)'
    )

fig1.show()

# %%
# Axial.

df_axial3=pd.DataFrame()
for id in df_axial2.pieza_id.unique():
    df_pieza=df_axial2[df_axial2.pieza_id== id]
    descrip=df_pieza.describe()['diferencia']
    condicion=False
    for index,row in df_pieza.iterrows():
        if condicion==False:
            if row['diferencia']>df_pieza['diferencia'].quantile(0.8):
                df_pieza.drop(index,inplace=True)
                condicion=True
        else:
            df_pieza.drop(index,inplace=True)
    df_axial3=df_axial3.append(df_pieza) 

# %%
# Line plot (Axial)
fig2 = px.line(
    df_axial3,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig2.update_layout(
        title = 'Desplazamiento por fuerza lineal (Axial)'
    )

fig2.show()

# %%
# Radial.

df_radial3=pd.DataFrame()
for id in df_radial2.pieza_id.unique():
    df_pieza=df_radial2[df_radial2.pieza_id== id]
    descrip=df_pieza.describe()['diferencia']
    condicion=False
    for index,row in df_pieza.iterrows():
        if condicion==False:
            if row['diferencia']>df_pieza['diferencia'].quantile(0.99):
                df_pieza.drop(index,inplace=True)
                condicion=True
        else:
            df_pieza.drop(index,inplace=True)
    df_radial3=df_radial3.append(df_pieza) 

# %%
# Line plot Radial
fig3 = px.line(
    df_radial3,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig3.update_layout(
        title = 'Desplazamiento por fuerza lineal (Radial)'
    )

fig3.show()

# %%
# Cardanica.

df_cardanic3=pd.DataFrame()
for id in df_cardanic2.pieza_id.unique():
    df_pieza=df_cardanic2[df_cardanic2.pieza_id== id]
    descrip=df_pieza.describe()['diferencia']
    condicion=False
    for index,row in df_pieza.iterrows():
        if condicion==False:
            if row['diferencia']>df_pieza['diferencia'].quantile(0.99):
                df_pieza.drop(index,inplace=True)
                condicion=True
        else:
            df_pieza.drop(index,inplace=True)
    df_cardanic3=df_cardanic3.append(df_pieza) 

# %%
df_cardanic2.diferencia.describe()

# %%
len(df_cardanic3)

# %%
# Line plot Cardanica
fig4 = px.line(
    df_cardanic3,
    x = 'displacement',
    y = 'fuerza',
    color = 'pieza_id'
)

fig4.update_layout(
        title = 'Desplazamiento por fuerza lineal (Cardanica)'
    )

fig4.show()

# %%
df_axial3.to_csv("../datos_transformados/df_axial_lineal.csv")
df_radial3.to_csv("../datos_transformados/df_radial_lineal.csv")
df_cardanic3.to_csv("../datos_transformados/df_cardanic_lineal.csv")
df_torsional3.to_csv("../datos_transformados/df_torsional_lineal.csv")

# %%



