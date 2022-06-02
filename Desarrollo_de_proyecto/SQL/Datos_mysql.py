# %%
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# %% [markdown]
# # IMPORTAR DATOS EN BRUTO

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_bruto'

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("DROP DATABASE IF EXISTS reto8_bruto") # Borrar base de datos
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("CREATE DATABASE IF NOT EXISTS reto8_bruto") # ejecutamos mediante el métido execute()
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
def consulta_sql(sql):
    conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
    cur = conn.cursor()
    cur.execute(sql) 
    conn.close()
    

# %%
sql='''CREATE TABLE IF NOT EXISTS axial (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS cardanica (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS radial (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS torsional (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT)'''
consulta_sql(sql)

# %%
df_axial=pd.read_csv('axialStiffness.csv')
df_radial=pd.read_csv('radialStiffness.csv')
df_cardanica=pd.read_csv('cardanicStiffness.csv')
df_torsional=pd.read_csv('torsionalStiffness.csv')

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_bruto")
con = engine.connect()
df_axial.to_sql(con=con, name='axial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_bruto")
con = engine.connect()
df_cardanica.to_sql(con=con, name='cardanica', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_bruto")
con = engine.connect()
df_torsional.to_sql(con=con, name='torsional', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_bruto")
con = engine.connect()
df_radial.to_sql(con=con, name='radial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %% [markdown]
# # IMPORTAR DATOS PREPROCESADOS

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_prep'

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("DROP DATABASE IF EXISTS reto8_prep") # Borrar base de datos
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("CREATE DATABASE IF NOT EXISTS reto8_prep") # ejecutamos mediante el métido execute()
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
sql='''CREATE TABLE IF NOT EXISTS axial (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (100))'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS cardanica (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (100))'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS radial ( extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (100))'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS torsional ( extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (100))'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS total (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (100), medida VARCHAR(15))'''
consulta_sql(sql)

# %%
df_axial=pd.read_csv('df_axial.csv')
df_radial=pd.read_csv('df_radial.csv')
df_cardanica=pd.read_csv('df_cardanic.csv')
df_torsional=pd.read_csv('df_torsional.csv')
df_total=pd.read_csv('df_completo.csv')

# %%
df_axial=df_axial.drop(['Unnamed: 0'],axis=1)
df_radial=df_radial.drop(['Unnamed: 0'],axis=1)
df_cardanica=df_cardanica.drop(['Unnamed: 0'],axis=1)
df_torsional=df_torsional.drop(['Unnamed: 0'],axis=1)
df_total=df_total.drop(['Unnamed: 0'],axis=1)

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_prep")
con = engine.connect()
df_axial.to_sql(con=con, name='axial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_prep")
con = engine.connect()
df_cardanica.to_sql(con=con, name='cardanica', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_prep")
con = engine.connect()
df_torsional.to_sql(con=con, name='torsional', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_prep")
con = engine.connect()
df_radial.to_sql(con=con, name='radial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_prep")
con = engine.connect()
df_total.to_sql(con=con, name='total', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %% [markdown]
# # IMPORTAR DATOS FILTRADOS PARA LOS MODELOS

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_mod'

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("DROP DATABASE IF EXISTS reto8_mod") # Borrar base de datos
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta)
cur = conn.cursor() # creamos un cursor que utilizaremos para ejecutar sentencias SQL
cur.execute("CREATE DATABASE IF NOT EXISTS reto8_mod") # ejecutamos mediante el métido execute()
conn.commit() 
# CREATE ocurre sí o sí, realmente no hace falta commit en MySQL
conn.close()

# %%
sql='''CREATE TABLE IF NOT EXISTS axial ( extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (10), pendiente FLOAT, diferencia FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS cardanica (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (10), pendiente FLOAT, diferencia FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS radial (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (10), pendiente FLOAT, diferencia FLOAT)'''
consulta_sql(sql)

# %%
sql='''CREATE TABLE IF NOT EXISTS torsional (extRad FLOAT,intRad FLOAT,jointRad FLOAT,distRad FLOAT,extH FLOAT,radH FLOAT,intH FLOAT,calibration INT,displacement FLOAT,stiffness FLOAT, fuerza FLOAT, pieza_id VARCHAR (10), pendiente FLOAT, diferencia FLOAT)'''
consulta_sql(sql)

# %%
df_axial=pd.read_csv('df_axial_lineal.csv')
df_radial=pd.read_csv('df_radial_lineal.csv')
df_cardanica=pd.read_csv('df_cardanic_lineal.csv')
df_torsional=pd.read_csv('df_torsional_lineal.csv')

# %%
df_axial=df_axial.drop(['index'],axis=1)
df_radial=df_radial.drop(['index'],axis=1)
df_cardanica=df_cardanica.drop(['index'],axis=1)
df_torsional=df_torsional.drop(['index'],axis=1)

# %%
df_axial=df_axial.drop(['Unnamed: 0'],axis=1)
df_radial=df_radial.drop(['Unnamed: 0'],axis=1)
df_cardanica=df_cardanica.drop(['Unnamed: 0'],axis=1)
df_torsional=df_torsional.drop(['Unnamed: 0'],axis=1)

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_mod")
con = engine.connect()
df_axial.to_sql(con=con, name='axial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_mod")
con = engine.connect()
df_cardanica.to_sql(con=con, name='cardanica', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_mod")
con = engine.connect()
df_torsional.to_sql(con=con, name='torsional', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%
engine = create_engine("mysql://root:1234@localhost/reto8_mod")
con = engine.connect()
df_radial.to_sql(con=con, name='radial', if_exists='append', chunksize=10000, index = False)  # append para insetar los valores
con.close()

# %%


# %%



