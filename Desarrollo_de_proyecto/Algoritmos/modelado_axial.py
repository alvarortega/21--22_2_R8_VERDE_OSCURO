# %% [markdown]
# Carga de datos.

# %%
import pandas as pd
import mysql.connector
import pandas as pd

# %%
usuario = "root"
contrasena = "1234"
ruta = "127.0.0.1"
database_name= 'reto8_mod'

# %%
def consulta_sql(sql):
    conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
    resultado = pd.read_sql(sql, conn)
    conn.close()
    return resultado

# %%
df_axial = consulta_sql('SELECT * FROM axial')

# %% [markdown]
# Preproceso.

# %%
for col in['pendiente','diferencia','Unnamed: 0','fuerza','pieza_id','index']:
    if col in df_axial.columns:
        del df_axial[col]

# %%
x_axial=df_axial.iloc[:,:-1]
y_axial=df_axial.iloc[:,-1]

# %% [markdown]
# Selección de Vars.

# %%
from sklearn.tree import DecisionTreeRegressor
import numpy as np
importance_tree_axial=DecisionTreeRegressor(random_state=0).fit(x_axial,y_axial)
importancias_axial=importance_tree_axial.feature_importances_
indices_importancias_axial=np.argsort(importancias_axial)[::-1]
for var in range(x_axial.shape[1]):
    print('Variable %d=%f'%(indices_importancias_axial[var],importancias_axial[indices_importancias_axial[var]]))

# %% [markdown]
# Split.

# %%
from sklearn.model_selection import train_test_split
x_axial_train,x_axial_test,y_axial_train,y_axial_test=train_test_split(x_axial,y_axial,random_state=0,shuffle=True)

# %% [markdown]
# Entrenar y evaluar modelos.

# %%
#Regresión lineal.
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
search_rl_axial=GridSearchCV(LinearRegression(),param_grid={'normalize':[True,False]}).fit(x_axial_train,y_axial_train)
print('Best Params:',search_rl_axial.best_params_)
rl_axial=search_rl_axial.best_estimator_
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error
print('Error medio:',mean_absolute_error(y_axial_test,rl_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,rl_axial.predict(x_axial_test))*100)

# %%
#Árbol de regresión.
search_ar_axial=GridSearchCV(DecisionTreeRegressor(random_state=0),
    param_grid={'criterion':['friedman_mse','poisson'],
        'max_features':['auto','sqrt','log2',None]}).fit(x_axial_train,y_axial_train)
print('Best Params:',search_ar_axial.best_params_)
ar_axial=search_ar_axial.best_estimator_
print('Error medio:',mean_absolute_error(y_axial_test,ar_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,ar_axial.predict(x_axial_test))*100)

# %%
#Regresor random forest.
from sklearn.ensemble import RandomForestRegressor
search_rfr_axial=GridSearchCV(RandomForestRegressor(random_state=0),
    param_grid={'n_estimators':[10,30,50],'max_features':['sqrt','log2','auto']}).fit(x_axial_train,y_axial_train)
print('Best Params:',search_rfr_axial.best_params_)
rfr_axial=search_rfr_axial.best_estimator_
print('Error medio:',mean_absolute_error(y_axial_test,rfr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,rfr_axial.predict(x_axial_test))*100)

# %%
#Regresor boosting AdaBoost.
from sklearn.ensemble import AdaBoostRegressor
search_abr_axial=GridSearchCV(AdaBoostRegressor(DecisionTreeRegressor(max_depth=None,random_state=0),random_state=0),
    param_grid={'n_estimators':[25,50,75],
        'learning_rate':[1.5,2,2.5],
        'loss':['linear','square','exponential']}).fit(x_axial_train,y_axial_train)
print('Best Params:',search_abr_axial.best_params_)
abr_axial=search_abr_axial.best_estimator_
print('Error medio:',mean_absolute_error(y_axial_test,abr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,abr_axial.predict(x_axial_test))*100)

# %%
#Regresor gradient boosting.
from sklearn.ensemble import GradientBoostingRegressor
search_gbr_axial=GridSearchCV(GradientBoostingRegressor(random_state=0),
    param_grid={'learning_rate':[.25,.5,.75],
        'subsample':[.25,.5,.75]}).fit(x_axial_train,y_axial_train)
print('Best Params:',search_gbr_axial.best_params_)
gbr_axial=search_gbr_axial.best_estimator_
print('Error medio:',mean_absolute_error(y_axial_test,gbr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,gbr_axial.predict(x_axial_test))*100)

# %%
#Regresor XGB.
from xgboost import XGBRegressor
xgbr_axial=XGBRegressor().fit(x_axial_train,y_axial_train)
print('Error medio:',mean_absolute_error(y_axial_test,xgbr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,xgbr_axial.predict(x_axial_test))*100)
import pickle
pickle.dump(xgbr_axial,open('modelo_axial.pkl','wb'))

# %%
#Regresor XGB con RF.
from xgboost import XGBRFRegressor
xgbrf_axial=XGBRFRegressor().fit(x_axial_train,y_axial_train)
print('Error medio:',mean_absolute_error(y_axial_test,xgbrf_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,xgbrf_axial.predict(x_axial_test))*100)

# %%
#Regresor LGBM.
from lightgbm import LGBMRegressor
lgbmr_axial=LGBMRegressor().fit(x_axial_train,y_axial_train)
print('Error medio:',mean_absolute_error(y_axial_test,lgbmr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,lgbmr_axial.predict(x_axial_test))*100)

# %%
#Regresor CatBoost.
from catboost import CatBoostRegressor
cbr_axial=CatBoostRegressor(verbose=0).fit(x_axial_train,y_axial_train)
print('Error medio:',mean_absolute_error(y_axial_test,cbr_axial.predict(x_axial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_axial_test,cbr_axial.predict(x_axial_test))*100)

# %%
x_axial_test


