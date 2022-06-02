# %%
# Importamos librerías Dash.
import jupyter_dash as dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html
import dash_bootstrap_components as dbc 
import matplotlib.pyplot as plt 


# Importamos Plotly Express para realizar graficos.
import plotly.express as px 
from plotly import graph_objects as go

# Importamos Pandas para cargar y tratar datos.
import pandas as pd
import numpy as np
import base64
import mysql.connector

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
df = consulta_sql('SELECT * FROM total')

# %%
external_stylesheets = [dbc.themes.LUX]

# # Creamos la aplicacion Dash y especificamos CSS.
app = dash.JupyterDash(
    __name__, 
    external_stylesheets = external_stylesheets
)



markdown_text = """
## CIKAUTXO

Esto es un cuadro de mando que permite conocer mejor los datos de las *piezas* que genera **Cikautxo**. 
Para más información, puede visitar la página web de [CIKAUTXO](https://www.cikautxo.es/).

Los gráficos varían en función de la selección de características de las piezas de las que se quiera ver información.

Para obetener infromación sobre las distintas piezas, puedes seleccionar la rigidez y varios rangos de las medidas de las piezas. 
"""

markdown_text1 = """
## Análisis exhaustivo de cada pieza

Selecciona el *id de la pieza* de la que quieras obtener información. Puedes comparar varias piezas entre sí seleccionando varios id a la vez.

"""

markdown_text2 = """
## Análisis exhaustivo de cada rigidez

Selecciona la *rigidez* de la que quieras obtener informació. Puedes comparar varias rigideces entre sí seleccionando varias a la vez.

"""



colors = {
    'background': '#002e60',
    'background2': '#FFC745',
    'text': 'white'
}

app.layout=html.Div(
    children=[
        html.Div(
            style={'backgroundColor': colors['background']},
            className = "row",
            children = [            

                html.Br(),
                html.H1(
                    children = "Dashboard interactivo Cikautxo",
                    style = {
                        "textAlign": "center",
                        'color': colors['text'],
                        'font-weight': 'bold'
                    }
                ),
                html.Br(),
                html.H5(
                    children = "Información sobre las piezas",
                    style = {
                        "textAlign": "center",
                        'color': colors['text']
                    }
                )
            ]
        ),
        dcc.Tabs(
            [
            dcc.Tab(
                style = {'backgroundColor':'#ffb703', 'color':'black', 'borderTop': '10px solid #002e60', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'}, 
                selected_style= {'backgroundColor':'#002e60', 'color':'white', 'borderTop': '10px solid #ffb703', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'},
                label = "Información general",
                children = [
                    html.Br(),
                    html.Div(
                        className = "row",
                        children = [
                            dcc.Markdown(children = markdown_text)
                        ]
                        
                    ),
                    
                    html.Div(
                        className = "row",
                        children = [                            
                            html.Div(
                                children = [
                                    html.H6("Rigidez de la pieza",
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    dcc.Dropdown(
                                        id = "dropdown-medida",
                                        options = [{
                                            "label": str(name),
                                            "value": name
                                        } for name  in list(np.sort(df["medida"].unique()))],
                                        value = [],
                                        placeholder = "Selecciona la rigidez de la pieza",
                                        multi = True
                                    ),
                                    html.Br( 
                                    ),
                                    html.Br(),
                                    
                                    html.H6("Rango medida 'extRad'",
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    html.Div(
                                        children = [
                                            dcc.Markdown(id = "markdown-extRad")
                                        ]
                                    ),
                                    dcc.RangeSlider(
                                        id = "range-extRad",
                                        min =28,
                                        max = df["extRad"].max(),
                                        step = 3,
                                        value = [28, df["extRad"].max()]
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.H6("Rango medida 'distRad'",
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    
                                    html.Div(
                                        children = [
                                            dcc.Markdown(id = "markdown-distRad")
                                        ]
                                    ),
                                    dcc.RangeSlider(
                                        id = "range-distRad",
                                        min = df["distRad"].min(),
                                        max = df["distRad"].max(),
                                        step = 3,
                                        value = [df["distRad"].min(), df["distRad"].max()]
                                    ),
                                ],
                                className = "two columns"
                            ),
                            html.Div(
                                children = [
                                    dcc.Graph(id = "hist-extRad"),
                                ],
                                className = "four columns"
                            ),
                            html.Div(
                                children = [
                                    dcc.Graph(id = "hist-distRad")
                                ],
                                className = "four columns"
                            ),
                            html.Div(
                                children = [
                                    dcc.Graph(id = "box-desplazamiento")
                                ],
                                className = "four columns"
                            ),
                            html.Div(
                                children = [
                                    dcc.Graph(id = "graf-med")
                                ],
                                className = "four columns"
                            ),
                        ]
                    )
                ]
            ),

               dcc.Tab(
                style = {'backgroundColor':'#ffb703', 'color':'black', 'borderTop': '10px solid #002e60', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'}, 
                selected_style= {'backgroundColor':'#002e60', 'color':'white', 'borderTop': '10px solid #ffb703', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'},
                label = "Piezas",
                children = [
                    html.Br(),
                    html.Div(
                        className = "row",
                        children = [
                            dcc.Markdown(children = markdown_text1)
                        ]
                        
                    ),
                    
                    html.Br(),
                    html.Div(
                        children = [
                            html.H6("Id de la pieza", 
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                            dcc.Dropdown(
                                id = "dropdown-id",
                                options = [{
                                    "label": str(name),
                                    "value": name
                                } for name  in list(np.sort(df["pieza_id"].unique()))],
                                value = [],
                                placeholder = "Selecciona el id de la pieza",
                                multi = True
                            ),
                            html.Br(),
                            html.Br(),
                            
                            html.H6("Medida de la pieza", 
                                style = {
                                        'color': 'red',
                                        'font-size': 20
                                }),
                            dcc.RadioItems(
                                id = "radio-medida",
                                options = [{
                                    "label": str(name),
                                    "value": name
                                } for name  in list(np.sort(df["medida"].unique()))]
                            )
                            
                        ],
                        className = "three columns"
                    ),
                    html.Div(
                        children = [
                            html.Div(
                                children = [
                                    dcc.Graph(id = "box-pieza")
                                ],
                                className = "nine columns"
                            )
                        ]
                    ),
                    html.Div(
                        children = [
                            html.Div(
                                children = [
                                    dcc.Graph(id = "line-fuerza")
                                ],
                                className = "nine columns"
                            )
                        ]
                    ), 
                    
                ]
            ),

            dcc.Tab(
                style = {'backgroundColor':'#ffb703', 'color':'black', 'borderTop': '10px solid #002e60', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'}, 
                selected_style= {'backgroundColor':'#002e60', 'color':'white', 'borderTop': '10px solid #ffb703', 'font-family':'Stencil Std, fantasy', 'font-size': '25px'},
                label = "Rigidez",
                children = [
                    
                    html.Div(
                        className = "row",
                        children = [
                            html.Br(),
                            html.Div(
                                className = "row",
                                children = [
                                    dcc.Markdown(children = markdown_text2)
                                ]
                                
                            ),
                            
                            html.Div(
                                children = [
                                    html.Br(),
                                    html.H6("Rigidez de la pieza",
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    dcc.Dropdown(
                                        id = "dropdown-medidas_pieza",
                                        options = [{
                                            "label": str(name),
                                            "value": name
                                        } for name  in list(np.sort(df["medida"].unique()))],
                                        value = [],
                                        placeholder = "Selecciona la medida de la pieza",
                                        multi = True
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    
                                    html.H6("Fuerza de la pieza", 
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    html.Div(
                                        className = "two rows",
                                        children = [
                                            dcc.Markdown(id = "markdown-fuerza")
                                        ]
                                    ), 
                                    dcc.RangeSlider(
                                        id = "range-fuerza",
                                        min = df["fuerza"].min(),
                                        max = df["fuerza"].max(),
                                        value = [df["fuerza"].min(), df["fuerza"].max()]
                                    ), 
                                    html.Br(),
                                    html.Br(),
                                    html.H6("Rigidez de la pieza", 
                                    style = {
                                         'color': 'red',
                                         'font-size': 20
                                    }),
                                    dcc.RangeSlider(
                                        id = "range-rigidez",
                                        min = df["stiffness"].min(),
                                        max = df["stiffness"].max(),
                                        value = [df["stiffness"].min(), df["stiffness"].max()]
                                    ), 
                                    
                                ],
                                className = "four columns"
                            ),
                            html.Div(
                                children = [
                                    dcc.Graph(id = "scatter-desplaz_fuerza")
                                ],
                                className = "eight columns"
                            ), 
                            html.Div(
                                children = [
                                    dcc.Graph(id = "bar-meds")
                                ],
                                className = "eight columns"
                            ), 
                            html.Div(
                                children = [
                                    dcc.Graph(id = "pie-id_med")
                                ],
                                className = "eight columns"
                            )
                        ]
                    )
                ]
            ) 
 
                
            ]
        )
        ]
    )

@app.callback(
    Output(
        component_id = "hist-extRad", 
        component_property = "figure"
    ),
    Output(
        component_id = "hist-distRad", 
        component_property = "figure"
    ),
    Output(
        component_id = "graf-med", 
        component_property = "figure"
    ),
    Output(
        component_id = "box-desplazamiento", 
        component_property = "figure"
    ),
    Output(
        component_id = "markdown-extRad",
        component_property = "children"
    ),
    Output(
        component_id = "markdown-distRad",
        component_property = "children"
    ),
    Input(
        component_id = "dropdown-medida",
        component_property = "value"
    ),
    Input(
        component_id = "range-extRad",
        component_property = "value"
    ),
    Input(
        component_id = "range-distRad",
        component_property = "value"
    )
)

def update_figure(selected_medida, selected_extRad, selected_distRad):
    dff = df[df["medida"].isin(selected_medida)]
    dff = dff[dff["extRad"].between(*selected_extRad)]
    dff = dff[dff["distRad"].between(*selected_distRad)]


    df0 = pd.DataFrame()
    df0["fuerza"] = dff.groupby("medida")["fuerza"].mean()
    df0["stiffness"] = dff.groupby("medida")["stiffness"].mean()

    df0


    # Creamos la figura.  (hist-rigidez)
    fig1 = px.histogram(
        dff,
        x = "stiffness",
        color = "medida",
        labels = {
            "medida": "Medida",
            "stiffness": "Rigidez"
        }
    )


    # Actualizamos el layout.
    fig1.update_layout(
        title = "",
        xaxis_title = "Rigidez",
        yaxis_title = "Número de piezas",
        bargap = 0.1
    )

    # Creamos la figura.  (hist-fuerza)
    fig2 = px.histogram(
        dff,
        x = "fuerza",
        color = "medida",
        labels = {
            "medida": "Medida",
            "fuerza": "Fuerza"
        }
    )

    # Actualizamos el layout.
    fig2.update_layout(
        title = "",
        xaxis_title = "Fuerza",
        yaxis_title = "Número de piezas",
        bargap = 0.1
    )


    # Creamos la figura. (box-desplazamiento)
    fig3 = px.box(
        dff, 
        x = "medida", 
        y = "displacement", 
        color = 'medida',
        points = "all", 
        labels = {
            "medida": "Medida",
            "displacement": "Desplazamiento"
        }
    )

    # Actualizamos el layout.
    fig3.update_layout(
        title = "Desplazamiento de las piezas según su medida",
        xaxis_title = "Medida",
        yaxis_title = "Desplazamiento de la pieza"
    )

    #Figura
    # fig4 = px.funnel(df0, x= 'fuerza', y= df0.index, color = df0.index)

    fig4 = go.Figure()

    fig4.add_trace(go.Funnel(
        name = 'Fuerza',
        y = df0.index,
        x = df0['fuerza'],
        textinfo = "value+percent initial"))

    fig4.add_trace(go.Funnel(
        name = "Rigidez",
        orientation = "h",
        y = df0.index,
        x = df0['stiffness'],
        textposition = "inside",
        textinfo = "value+percent previous"))
    
    fig4.update_layout(
        title = 'Porcentaje de rigidez y fuerza'
    )



    # Actualizamos el texto Markdown
    text_extRad = """
    El **rango de medida extRad** está entre {0:.0f} y {1:.0f}.
    """.format(*selected_extRad)

     # Actualizamos el texto Markdown
    text_distRad = """
    El **rango de medida extRad** está entre {0:.0f} y {1:.0f}.
    """.format(*selected_distRad)

    return fig1, fig2, fig3, fig4, text_extRad, text_distRad




@app.callback(
    Output(
        component_id = "box-pieza", 
        component_property = "figure"
    ),
    
    Output(
        component_id = "line-fuerza", 
        component_property = "figure"
    ),
    Input(
        component_id = "dropdown-id",
        component_property = "value"
    ),
    Input(
        component_id = "radio-medida",
        component_property = "value"
    )
)

def update_figure(selected_id, selected_medida):
    df1 = df[df["pieza_id"].isin(selected_id)]
    df1 = df1[df1["medida"] == selected_medida]
    


    # Figura
    fig5 = px.box(
        df1,
        x = 'pieza_id',
        y = 'stiffness',
        points = 'all',
        color = 'pieza_id',
        labels= {
            'pieza_id': 'Id de la pieza',
            'stiffness' : 'Rigidez'
        }
    )

    # Actualizamos el layout
    fig5.update_layout(
        title = 'Rigidez por pieza',
        xaxis_title = 'Id de la pieza',
        yaxis_title = 'Rigidez'
    )

     # Line plot
    fig7 = px.line(
        df1,
        x = 'displacement',
        y = 'fuerza',
        color = 'pieza_id'
    )
    
    fig7.update_layout(
        title = 'Desplazamiento en función de la fuerza de la pieza',
        xaxis_title = 'Desplazamiento',
        yaxis_title = 'Fuerza'
    )

    

    return fig5, fig7




@app.callback(
    Output(
        component_id = "scatter-desplaz_fuerza", 
        component_property = "figure"
    ),
    Output(
        component_id = "bar-meds", 
        component_property = "figure"
    ),
    Output(
        component_id = "pie-id_med",
        component_property = "figure"
    ),
    Output(
        component_id = "markdown-fuerza",
        component_property = "children"
    ),
    
    Input(
        component_id = "dropdown-medidas_pieza",
        component_property = "value"
    ),
    Input(
        component_id = "range-fuerza",
        component_property = "value"
    ),
    Input(
        component_id = "range-rigidez",
        component_property = "value"
    )
)
def update_figure(selected_medidas_pieza, selected_fuerza, selected_rigidez):
    df2 = df[df["medida"].isin(selected_medidas_pieza)]
    df2 = df2[df2["fuerza"].between(*selected_fuerza)]
    df2 = df2[df2["stiffness"].between(*selected_rigidez)]

    df3 = pd.DataFrame()
    df3['num_pieza'] = df2.groupby('medida')['pieza_id'].count()
    df3


    fig6 = px.scatter(df2, x="stiffness", y="fuerza",
	         color="medida")

    fig6.update_layout(
        title = "Relación entre la rigidez y el desplazamiento de las piezas"

    )

   

    fig9 = px.bar(df2, x="extRad", y="jointRad",
	          color="medida")

    fig9.update_layout(
        title = 'Medidas de extRad y distRad de cada pieza',
        xaxis_title = 'Medida extRad',
        yaxis_title = 'Medida jointRad'
    )
    #Bar plot
    # fig8 = px.bar(
    #     df3,
    #     x = df3.index,
    #     y = 'num_pieza',
    #     color = df3.index
    # )

    fig8 = px.pie(df3, values='num_pieza', names= df3.index, hole=.5, title='Número de piezas por medida')











     # Actualizamos el texto Markdown
    text_fuerza = """
    La **fuerza de la pieza** está entre {0:.0f} y {1:.0f}.
    """.format(*selected_fuerza)

    return fig6, fig9, fig8, text_fuerza
    


    
if __name__ == "__main__":
    app.run_server(mode = "external", debug = True, port = 8062)

# %%


# %%



