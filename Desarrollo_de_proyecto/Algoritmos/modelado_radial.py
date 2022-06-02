# %% [markdown]
# Carga de datos.

# %%
import pandas as pd
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
df_radial = consulta_sql('SELECT * FROM radial')

# %% [markdown]
# Preproceso.

# %%
for col in['pendiente','diferencia','Unnamed: 0','fuerza','pieza_id','index']:
    if col in df_radial.columns:
        del df_radial[col]

# %%
x_radial=df_radial.iloc[:,:-1]
y_radial=df_radial.iloc[:,-1]

# %% [markdown]
# Selección de Vars.

# %%
from sklearn.tree import DecisionTreeRegressor
import numpy as np
importance_tree_radial=DecisionTreeRegressor(random_state=0).fit(x_radial,y_radial)
importancias_radial=importance_tree_radial.feature_importances_
indices_importancias_radial=np.argsort(importancias_radial)[::-1]
for var in range(x_radial.shape[1]):
    print('Variable %d=%f'%(indices_importancias_radial[var],importancias_radial[indices_importancias_radial[var]]))

# %% [markdown]
# Split.

# %%
from sklearn.model_selection import train_test_split
x_radial_train,x_radial_test,y_radial_train,y_radial_test=train_test_split(x_radial,y_radial,random_state=0,shuffle=True)

# %% [markdown]
# Entrenar y evaluar modelos.

# %%
#Regresión lineal.
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
search_rl_radial=GridSearchCV(LinearRegression(),param_grid={'normalize':[True,False]}).fit(x_radial_train,y_radial_train)
print('Best Params:',search_rl_radial.best_params_)
rl_radial=search_rl_radial.best_estimator_
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error
print('Error medio:',mean_absolute_error(y_radial_test,rl_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,rl_radial.predict(x_radial_test))*100)

# %%
#Árbol de regresión.
search_ar_radial=GridSearchCV(DecisionTreeRegressor(random_state=0),
    param_grid={'criterion':['friedman_mse','poisson'],
        'max_features':['auto','sqrt','log2',None]}).fit(x_radial_train,y_radial_train)
print('Best Params:',search_ar_radial.best_params_)
ar_radial=search_ar_radial.best_estimator_
print('Error medio:',mean_absolute_error(y_radial_test,ar_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,ar_radial.predict(x_radial_test))*100)

# %%
#Regresor random forest.
from sklearn.ensemble import RandomForestRegressor
search_rfr_radial=GridSearchCV(RandomForestRegressor(random_state=0),
    param_grid={'n_estimators':[25,50,75],'max_features':['sqrt','log2','auto']}).fit(x_radial_train,y_radial_train)
print('Best Params:',search_rfr_radial.best_params_)
rfr_radial=search_rfr_radial.best_estimator_
print('Error medio:',mean_absolute_error(y_radial_test,rfr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,rfr_radial.predict(x_radial_test))*100)

# %%
#Regresor boosting AdaBoost.
from sklearn.ensemble import AdaBoostRegressor
search_abr_radial=GridSearchCV(AdaBoostRegressor(DecisionTreeRegressor(max_depth=None,random_state=0),random_state=0),
    param_grid={'n_estimators':[75,100,125],
        'learning_rate':[2,2.5,3],
        'loss':['linear','square','exponential']}).fit(x_radial_train,y_radial_train)
print('Best Params:',search_abr_radial.best_params_)
abr_radial=search_abr_radial.best_estimator_
print('Error medio:',mean_absolute_error(y_radial_test,abr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,abr_radial.predict(x_radial_test))*100)

# %%
#Regresor gradient boosting.
from sklearn.ensemble import GradientBoostingRegressor
search_gbr_radial=GridSearchCV(GradientBoostingRegressor(random_state=0),
    param_grid={'learning_rate':[.25,.5,.75],
        'subsample':[.75,1]}).fit(x_radial_train,y_radial_train)
print('Best Params:',search_gbr_radial.best_params_)
gbr_radial=search_gbr_radial.best_estimator_
print('Error medio:',mean_absolute_error(y_radial_test,gbr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,gbr_radial.predict(x_radial_test))*100)

# %%
#Regresor XGB.
from xgboost import XGBRegressor
xgbr_radial=XGBRegressor().fit(x_radial_train,y_radial_train)
print('Error medio:',mean_absolute_error(y_radial_test,xgbr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,xgbr_radial.predict(x_radial_test))*100)

# %%
#Regresor XGB con RF.
from xgboost import XGBRFRegressor
xgbrf_radial=XGBRFRegressor().fit(x_radial_train,y_radial_train)
print('Error medio:',mean_absolute_error(y_radial_test,xgbrf_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,xgbrf_radial.predict(x_radial_test))*100)

# %%
#Regresor LGBM.
from lightgbm import LGBMRegressor
lgbmr_radial=LGBMRegressor().fit(x_radial_train,y_radial_train)
print('Error medio:',mean_absolute_error(y_radial_test,lgbmr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,lgbmr_radial.predict(x_radial_test))*100)

# %%
#Regresor CatBoost.
from catboost import CatBoostRegressor
cbr_radial=CatBoostRegressor(verbose=0).fit(x_radial_train,y_radial_train)
print('Error medio:',mean_absolute_error(y_radial_test,cbr_radial.predict(x_radial_test)))
print('Error medio %:',mean_absolute_percentage_error(y_radial_test,cbr_radial.predict(x_radial_test))*100)
import pickle
pickle.dump(cbr_radial,open('modelo_radial.pkl','wb'))


