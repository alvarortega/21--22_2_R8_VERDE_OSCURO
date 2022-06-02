# %%
import mysql.connector
from sqlalchemy import create_engine
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
conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
cur = conn.cursor()
cur.execute("SHOW TABLES") 
print(cur.fetchall())
conn.close()

# %% [markdown]
# ## CONSULTAS CON LOS DATOS EN BRUTO

# %%
consulta_sql('''SELECT * FROM AXIAL
    ORDER BY stiffness
    LIMIT 5 ''')



# %%
consulta_sql('''SELECT * FROM torsional
    ORDER BY stiffness
    LIMIT 5 ''')

# %%
consulta_sql('''SELECT * FROM cardanica
    ORDER BY stiffness
    LIMIT 5 ''')

# %%
consulta_sql('''SELECT * FROM radial
    ORDER BY stiffness
    LIMIT 5 ''')

# %%
df_axial=pd.read_csv('axialStiffness.csv')

# %%
consulta_sql(f'''SELECT * FROM axial
    WHERE displacement >= {df_axial['displacement'].quantile(0.9)}
    ORDER BY stiffness
    LIMIT 5 ''')

# %% [markdown]
# ## CONSULTAS CON LOS DATOS PREPROCESADOS

# %%
database_name= 'reto8_prep'

# %%
sql = '''SELECT pieza_id, AVG(fuerza) as media_fuerza, COUNT(*) as num 
         FROM axial
         GROUP BY pieza_id
         ORDER BY pieza_id'''
consulta_sql(sql)
         

# %%
sql = '''SELECT pieza_id, AVG(fuerza) as media_fuerza, COUNT(*) as num 
         FROM cardanica
         GROUP BY pieza_id
         ORDER BY pieza_id'''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(fuerza) as media_fuerza, COUNT(*) as num 
         FROM torsional
         GROUP BY pieza_id
         ORDER BY pieza_id'''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(fuerza) as media_fuerza, COUNT(*) as num 
         FROM radial
         GROUP BY pieza_id
         ORDER BY pieza_id'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(displacement) as media_desplazamiento 
         FROM radial
         GROUP BY fuerza
         ORDER BY fuerza'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(displacement) as media_desplazamiento 
         FROM axial
         GROUP BY fuerza
         ORDER BY fuerza'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(displacement) as media_desplazamiento 
         FROM torsional
         GROUP BY fuerza
         ORDER BY fuerza'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(displacement) as media_desplazamiento 
         FROM cardanica
         GROUP BY fuerza
         ORDER BY fuerza'''
consulta_sql(sql)

# %%
sql = 'SELECT DISTINCT(pieza_id) FROM axial WHERE 	distRad <23.8'
consulta_sql(sql)

# %% [markdown]
# ## CONSULTAS CON LOS DATOS PARA LOS MODELOS

# %%
database_name= 'reto8_mod'

# %%
sql = 'SELECT displacement, fuerza, pendiente FROM axial  WHERE  pieza_id=45  ORDER BY pendiente'
consulta_sql(sql)

# %%
sql = 'SELECT displacement, fuerza, pendiente FROM radial  WHERE  pieza_id=52  ORDER BY pendiente'
consulta_sql(sql)

# %%
sql = 'SELECT displacement, fuerza, pendiente FROM torsional  WHERE  pieza_id=98  ORDER BY pendiente'
consulta_sql(sql)

# %%
sql = 'SELECT displacement, fuerza, pendiente FROM cardanica  WHERE  pieza_id=13  ORDER BY pendiente'
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(pendiente) as media_pendiente
         FROM cardanica
         GROUP BY fuerza
         ORDER BY fuerza DESC
         LIMIT 7'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(pendiente) as media_pendiente
         FROM axial
         GROUP BY fuerza
         ORDER BY fuerza DESC
         LIMIT 7'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(pendiente) as media_pendiente
         FROM torsional
         GROUP BY fuerza
         ORDER BY fuerza DESC
         LIMIT 7'''
consulta_sql(sql)

# %%
sql='''SELECT fuerza, AVG(pendiente) as media_pendiente
         FROM radial
         GROUP BY fuerza
         ORDER BY fuerza DESC
         LIMIT 7'''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(pendiente) as media_pendiente, AVG(displacement) as media_desplazamiento
         FROM cardanica
         GROUP BY pieza_id
         ORDER BY media_pendiente '''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(pendiente) as media_pendiente, AVG(displacement) as media_desplazamiento
         FROM axial
         GROUP BY pieza_id
         ORDER BY media_pendiente '''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(pendiente) as media_pendiente, AVG(displacement) as media_desplazamiento
         FROM radial
         GROUP BY pieza_id
         ORDER BY media_pendiente '''
consulta_sql(sql)

# %%
sql = '''SELECT pieza_id, AVG(pendiente) as media_pendiente, AVG(displacement) as media_desplazamiento
         FROM torsional
         GROUP BY pieza_id
         ORDER BY media_pendiente '''
consulta_sql(sql)

# %%



