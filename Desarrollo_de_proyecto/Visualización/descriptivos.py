# %%
import pandas as pd
import numpy as np
import plotly.express as px 
from plotly import graph_objects as go


# %%
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
display(df_axial)

# %% [markdown]
# ### AXIAL

# %%
fig1 = px.histogram(
        df_axial,
        x = "stiffness"
    )
fig1.update_layout(
    title = 'Histograma de rigidez (axial)',
    xaxis_title = 'Rigidez',
    yaxis_title = 'Cantidad de rigidez'
)
fig1.show()

# %%
fig2 = px.box(
    df_axial,
    x = 'extH',
    y = 'displacement'
)
fig2.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida extH (axial)',
    xaxis_title = 'Medida extH',
    yaxis_title = 'Desplazamiento'
)
fig2.show()

# %%
fig3 = px.box(
    df_axial,
    x = 'jointRad',
    y = 'displacement'
)
fig3.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida jointRad (axial)',
    xaxis_title = 'Medida distRad',
    yaxis_title = 'Desplazamiento'
)
fig3.show()

# %%
fig4 = px.bar(
    df_axial,
    x = 'extRad',
    y = 'distRad'
)

fig4.update_layout(
    title = 'Medida extRad en función de la medida distRad (axial)',
    xaxis_title = 'Medida extRad',
    yaxis_title = 'Medida distRad'
)
fig4.show()

# %% [markdown]
# ### RADIAL

# %%
fig5 = px.histogram(
        df_radial,
        x = "stiffness"
    )
fig5.update_layout(
    title = 'Histograma de rigidez (radial)',
    xaxis_title = 'Rigidez',
    yaxis_title = 'Cantidad de rigidez'
)
fig5.show()

# %%
fig6 = px.box(
    df_radial,
    x = 'extH',
    y = 'displacement'
)
fig6.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida extH (radial)',
    xaxis_title = 'Medida extH',
    yaxis_title = 'Desplazamiento'
)
fig6.show()

# %%
fig7 = px.box(
    df_radial,
    x = 'jointRad',
    y = 'displacement'
)
fig7.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida jointRad (radial)',
    xaxis_title = 'Medida distRad',
    yaxis_title = 'Desplazamiento'
)
fig7.show()

# %%
fig8 = px.bar(
    df_radial,
    x = 'extRad',
    y = 'distRad'
)

fig8.update_layout(
    title = 'Medida extRad en función de la medida distRad (radial)',
    xaxis_title = 'Medida extRad',
    yaxis_title = 'Medida distRad'
)
fig8.show()

# %% [markdown]
# ### TORSIONAL

# %%
fig9 = px.histogram(
        df_torsional,
        x = "stiffness"
    )
fig9.update_layout(
    title = 'Histograma de rigidez (torsional)',
    xaxis_title = 'Rigidez',
    yaxis_title = 'Cantidad de rigidez'
)
fig9.show()

# %%
fig10 = px.box(
    df_torsional,
    x = 'extH',
    y = 'displacement'
)
fig10.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida extH (torsional)',
    xaxis_title = 'Medida extH',
    yaxis_title = 'Desplazamiento'
)
fig10.show()

# %%
fig11 = px.box(
    df_radial,
    x = 'jointRad',
    y = 'displacement'
)
fig11.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida jointRad (torsional)',
    xaxis_title = 'Medida distRad',
    yaxis_title = 'Desplazamiento'
)
fig11.show()

# %%
fig12 = px.bar(
    df_radial,
    x = 'extRad',
    y = 'distRad'
)

fig12.update_layout(
    title = 'Medida extRad en función de la medida distRad (torsional)',
    xaxis_title = 'Medida extRad',
    yaxis_title = 'Medida distRad'
)
fig12.show()

# %% [markdown]
# ### CARDANIC

# %%
fig13 = px.histogram(
        df_torsional,
        x = "stiffness"
    )
fig13.update_layout(
    title = 'Histograma de rigidez (cardanic)',
    xaxis_title = 'Rigidez',
    yaxis_title = 'Cantidad de rigidez'
)
fig13.show()

# %%
fig14 = px.box(
    df_torsional,
    x = 'extH',
    y = 'displacement'
)
fig14.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida extH (cardanic)',
    xaxis_title = 'Medida extH',
    yaxis_title = 'Desplazamiento'
)
fig14.show()

# %%
fig15 = px.box(
    df_radial,
    x = 'jointRad',
    y = 'displacement'
)
fig15.update_layout(
    title = 'Desplazamiento de la pieza en función de la medida jointRad (cardanic)',
    xaxis_title = 'Medida distRad',
    yaxis_title = 'Desplazamiento'
)
fig15.show()

# %%
fig16 = px.bar(
    df_radial,
    x = 'extRad',
    y = 'distRad'
)

fig16.update_layout(
    title = 'Medida extRad en función de la medida distRad (cardanic)',
    xaxis_title = 'Medida extRad',
    yaxis_title = 'Medida distRad'
)
fig16.show()

# %%



