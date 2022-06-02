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
df_torsional = consulta_sql('SELECT * FROM torsional')

# %% [markdown]
# Preproceso.

# %%
for col in['pendiente','diferencia','Unnamed: 0','fuerza','pieza_id','index']:
    if col in df_torsional.columns:
        del df_torsional[col]

# %%
x_torsional=df_torsional.iloc[:,:-1]
y_torsional=df_torsional.iloc[:,-1]

# %% [markdown]
# Selección de Vars.

# %%
from sklearn.tree import DecisionTreeRegressor
import numpy as np
importance_tree_torsional=DecisionTreeRegressor(random_state=0).fit(x_torsional,y_torsional)
importancias_torsional=importance_tree_torsional.feature_importances_
indices_importancias_torsional=np.argsort(importancias_torsional)[::-1]
for var in range(x_torsional.shape[1]):
    print('Variable %d=%f'%(indices_importancias_torsional[var],importancias_torsional[indices_importancias_torsional[var]]))

# %% [markdown]
# Split.

# %%
from sklearn.model_selection import train_test_split
x_torsional_train,x_torsional_test,y_torsional_train,y_torsional_test=train_test_split(x_torsional,y_torsional,random_state=0,shuffle=True)

# %% [markdown]
# Entrenar y evaluar modelos.

# %%
#Regresión lineal.
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
search_rl_torsional=GridSearchCV(LinearRegression(),param_grid={'normalize':[True,False]}).fit(x_torsional_train,y_torsional_train)
print('Best Params:',search_rl_torsional.best_params_)
rl_torsional=search_rl_torsional.best_estimator_
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error
print('Error medio:',mean_absolute_error(y_torsional_test,search_rl_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,rl_torsional.predict(x_torsional_test))*100)

# %%
#Árbol de regresión.
search_abr_torsional=GridSearchCV(DecisionTreeRegressor(random_state=0),
    param_grid={'criterion':['friedman_mse','poisson'],
        'max_features':['auto','sqrt','log2',None]}).fit(x_torsional_train,y_torsional_train)
print('Best Params:',search_abr_torsional.best_params_)
abr_torsional=search_abr_torsional.best_estimator_
print('Error medio:',mean_absolute_error(y_torsional_test,abr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,abr_torsional.predict(x_torsional_test))*100)

# %%
#Regresor random forest.
from sklearn.ensemble import RandomForestRegressor
search_rfr_torsional=GridSearchCV(RandomForestRegressor(random_state=0),
    param_grid={'n_estimators':[750,1000,1250]}).fit(x_torsional_train,y_torsional_train)
print('Best Params:',search_rfr_torsional.best_params_)
rfr_torsional=search_rfr_torsional.best_estimator_
print('Error medio absoluto:',mean_absolute_error(y_torsional_test,rfr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,rfr_torsional.predict(x_torsional_test))*100)

# %%
#AdaBoost regressor.
from sklearn.ensemble import AdaBoostRegressor
search_abr_torsional=GridSearchCV(AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=None,random_state=0),random_state=0),
    param_grid={'n_estimators':[125,150,175]}).fit(x_torsional_train,y_torsional_train)
print('Best Params:',search_abr_torsional.best_params_)
abr_torsional=search_abr_torsional.best_estimator_
print('Error medio absoluto:',mean_absolute_error(y_torsional_test,abr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,abr_torsional.predict(x_torsional_test))*100)

# %%
#Regresor gradient boosting.
from sklearn.ensemble import GradientBoostingRegressor
search_gbr_torsional=GridSearchCV(GradientBoostingRegressor(random_state=0),
    param_grid={'learning_rate':[.15,.2,.25],
        'subsample':[.20,.35,.5]}).fit(x_torsional_train,y_torsional_train)
print('Best Params:',search_gbr_torsional.best_params_)
gbr_torsional=search_gbr_torsional.best_estimator_
print('Error medio:',mean_absolute_error(y_torsional_test,gbr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,gbr_torsional.predict(x_torsional_test))*100)

# %%
#Regresor XGB.
from xgboost import XGBRegressor
xgbr_torsional=XGBRegressor().fit(x_torsional_train,y_torsional_train)
print('Error medio:',mean_absolute_error(y_torsional_test,xgbr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,xgbr_torsional.predict(x_torsional_test))*100)
import pickle
pickle.dump(xgbr_torsional,open('modelo_torsional.pkl','wb'))

# %%
#Regresor XGB con RF.
from xgboost import XGBRFRegressor
xgbrf_torsional=XGBRFRegressor().fit(x_torsional_train,y_torsional_train)
print('Error medio:',mean_absolute_error(y_torsional_test,xgbrf_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,xgbrf_torsional.predict(x_torsional_test))*100)

# %%
#Regresor LGBM.
from lightgbm import LGBMRegressor
lgbmr_torsional=LGBMRegressor().fit(x_torsional_train,y_torsional_train)
print('Error medio:',mean_absolute_error(y_torsional_test,lgbmr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,lgbmr_torsional.predict(x_torsional_test))*100)

# %%
#Regresor CatBoost.
from catboost import CatBoostRegressor
cbr_torsional=CatBoostRegressor(verbose=0).fit(x_torsional_train,y_torsional_train)
print('Error medio:',mean_absolute_error(y_torsional_test,cbr_torsional.predict(x_torsional_test)))
print('Error medio %:',mean_absolute_percentage_error(y_torsional_test,cbr_torsional.predict(x_torsional_test))*100)


