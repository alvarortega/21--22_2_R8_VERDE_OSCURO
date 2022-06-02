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
database_name= 'reto8_bruto'

# %%
def consulta_sql(sql):
    conn = mysql.connector.connect(user=usuario, password=contrasena, host=ruta, database = database_name)
    resultado = pd.read_sql(sql, conn)
    conn.close()
    return resultado

# %%
df_cardanic = consulta_sql('SELECT * FROM cardanica')

# %% [markdown]
# Preproceso.

# %%
for col in['pendiente','diferencia','Unnamed: 0','fuerza','pieza_id','index']:
    if col in df_cardanic.columns:
        del df_cardanic[col]

# %%
x_cardanic=df_cardanic.iloc[:,:-1]
y_cardanic=df_cardanic.iloc[:,-1]

# %% [markdown]
# Selección de Vars.

# %%
from sklearn.tree import DecisionTreeRegressor
import numpy as np
importance_tree_cardanic=DecisionTreeRegressor(random_state=0).fit(x_cardanic,y_cardanic)
importancias_cardanic=importance_tree_cardanic.feature_importances_
indices_importancias_cardanic=np.argsort(importancias_cardanic)[::-1]
for var in range(x_cardanic.shape[1]):
    print('Variable %d=%f'%(indices_importancias_cardanic[var],importancias_cardanic[indices_importancias_cardanic[var]]))

# %% [markdown]
# Split.

# %%
from sklearn.model_selection import train_test_split
x_cardanic_train,x_cardanic_test,y_cardanic_train,y_cardanic_test=train_test_split(x_cardanic,y_cardanic,random_state=0,shuffle=True)

# %% [markdown]
# Entrenar y evaluar modelos.

# %%
#Regresión lineal.
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
search_rl_cardanic=GridSearchCV(LinearRegression(),param_grid={'normalize':[True,False]}).fit(x_cardanic_train,y_cardanic_train)
print('Best Params:',search_rl_cardanic.best_params_)
rl_cardanic=search_rl_cardanic.best_estimator_
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error
print('Error medio absoluto:',mean_absolute_error(y_cardanic_test,rl_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,rl_cardanic.predict(x_cardanic_test))*100)

# %%
#Árbol de regresión.
search_ar_cardanic=GridSearchCV(DecisionTreeRegressor(random_state=0),
    param_grid={'criterion':['friedman_mse','poisson'],
        'max_features':['auto','sqrt','log2',None]}).fit(x_cardanic_train,y_cardanic_train)
print('Best Params:',search_ar_cardanic.best_params_)
ar_cardanic=search_ar_cardanic.best_estimator_
print('Error medio absoluto:',mean_absolute_error(y_cardanic_test,ar_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,ar_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor random forest.
from sklearn.ensemble import RandomForestRegressor
search_rfr_cardanic=GridSearchCV(RandomForestRegressor(random_state=0),
    param_grid={'n_estimators':[500,1000,1500],'max_features':['sqrt','log2','auto']}).fit(x_cardanic_train,y_cardanic_train)
print('Best Params:',search_rfr_cardanic.best_params_)
rfr_cardanic=search_rfr_cardanic.best_estimator_
print('Error medio absoluto:',mean_absolute_error(y_cardanic_test,rfr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,rfr_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor boosting AdaBoost.
from sklearn.ensemble import AdaBoostRegressor
search_abr_cardanic=GridSearchCV(AdaBoostRegressor(DecisionTreeRegressor(max_depth=None,random_state=0),random_state=0),
    param_grid={'n_estimators':[75,100,125],
        'learning_rate':[2,2.5,3],
        'loss':['linear','square','exponential']}).fit(x_cardanic_train,y_cardanic_train)
print('Best Params:',search_abr_cardanic.best_params_)
abr_cardanic=search_abr_cardanic.best_estimator_
print('Error medio:',mean_absolute_error(y_cardanic_test,abr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,abr_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor gradient boosting.
from sklearn.ensemble import GradientBoostingRegressor
search_gbr_cardanic=GridSearchCV(GradientBoostingRegressor(random_state=0),
    param_grid={'learning_rate':[.15,.3,.45],
        'subsample':[.75,1]}).fit(x_cardanic_train,y_cardanic_train)
print('Best Params:',search_gbr_cardanic.best_params_)
gbr_cardanic=search_gbr_cardanic.best_estimator_
print('Error medio:',mean_absolute_error(y_cardanic_test,gbr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,gbr_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor XGB.
from xgboost import XGBRegressor
xgbr_cardanic=XGBRegressor().fit(x_cardanic_train,y_cardanic_train)
print('Error medio:',mean_absolute_error(y_cardanic_test,xgbr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,xgbr_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor XGB con RF.
from xgboost import XGBRFRegressor
xgbrf_cardanic=XGBRFRegressor().fit(x_cardanic_train,y_cardanic_train)
print('Error medio:',mean_absolute_error(y_cardanic_test,xgbrf_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,xgbrf_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor LGBM.
from lightgbm import LGBMRegressor
lgbmr_cardanic=LGBMRegressor().fit(x_cardanic_train,y_cardanic_train)
print('Error medio:',mean_absolute_error(y_cardanic_test,lgbmr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,lgbmr_cardanic.predict(x_cardanic_test))*100)

# %%
#Regresor CatBoost.
from catboost import CatBoostRegressor
cbr_cardanic=CatBoostRegressor(verbose=0).fit(x_cardanic_train,y_cardanic_train)
print('Error medio:',mean_absolute_error(y_cardanic_test,cbr_cardanic.predict(x_cardanic_test)))
print('Error medio %:',mean_absolute_percentage_error(y_cardanic_test,cbr_cardanic.predict(x_cardanic_test))*100)
import pickle
pickle.dump(cbr_cardanic,open('modelo_cardanic.pkl','wb'))


