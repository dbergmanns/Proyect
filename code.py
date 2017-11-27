#lectures/08-stats/statistics_examples.ipynb
##[1] Import programs
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, linregress
import matplotlib.pyplot as plt
%matplotlib inline
import statsmodels.formula.api as smf
import sqlite3

##[2] import seaborn as it will affect how our plots look
import seaborn as sns
sns.set_style("whitegrid", rc={'axes.linewidth': 2.5})
sns.set_context('notebook', font_scale=1.45, rc={"lines.linewidth": 3, "figure.figsize" : (7, 3)})

#import data from IPUMS
ipums = pd.read_csv("usa_00019.csv", usecols=["YEAR", "STATEFIP", "COUNTYFIPS", "PERWT", "SEX", "AGE", "HISPAN", "CITIZEN", "MIGRATE1"])
ipums.head(10)

#seleccionar personas que no son ciudadanos de eu y que hace 1 año vivían en otro país
#no seleccionar personas que no respondieron si eran hispanos o no (9)
#no se toman en cuenta los estados con códigos 2, 3, 7, 14, 15, 43 (Puerto Rico), 52 (Virgin Islands)
#se eliminan las filas que tienen cero en COUNTYFIPS
#si al hacer head no aparece información es porque alguno de los filtros no aplica, por ejemplo, citizen=3 no existe en los datos
ipums_filtered=ipums[(ipums.CITIZEN == 3) & (ipums.CITIZEN == 4) & (ipums.CITIZEN == 5) & (ipums.MIGRATE1 == 4) &
                        (ipums.HISPAN == 0) & (ipums.HISPAN == 1) & (ipums.HISPAN == 2) &
                        (ipums.HISPAN == 3) & (ipums.HISPAN == 4) & (ipums.STATEFIP != 2) & (ipums.STATEFIP != 3)
                        & (ipums.STATEFIP != 7) & (ipums.STATEFIP != 14) & (ipums.STATEFIP != 15) & (ipums.STATEFIP != 43) 
                        & (ipums.STATEFIP != 52) & (ipums.COUNTYFIPS > 0)]
ipums.head(20)
#CREAR UNA VARIABLE QUE SEA LA SUMA DE STATE Y COUNTY PARA UNIR POR ESA LAS DOS BASES DE DATOS

#Agrupar por county, estado y año el promedio de AGE, SEX2, HISPAN2
#y la cuenta de MIGRATE1
#este comando es para sacar el promedio de una sola variable
ipums2=ipums_filtered.groupby(["COUNTYFIPS", "STATEFIP", "YEAR"]).AGE.mean().reset_index()
#encontré este comando en internet para sacar estadísitcas de más de dos variables, pero no sé cómo agregarle groupby
grouped.agg({
    'AGE': 'mean',
    'SEX': 'mean'})

#renombrar variables, por ejemplo, de 1 y 2 a 0 y 1 para sexo. Más fácil para sacar propociones
ipums["HISPAN2"] = 1
ipums.loc[ipums["HISPAN"] == 0,  "HISPAN2"] = 0
ipums["SEX2"] = 0
ipums.loc[ipums["SEX"] == 2,  "SEX2"] = 1

#HASTA AQUÍ YA TODO ESTÁ PROBADO

#Merge datasets. checar que los códigos de estado y condado sean iguales en la base de datos de IPUMS y ACS
ipums_labor = pd.merge(ipums, labor).set_index("") #also see [44]
#or
il_ex_temp = il_exercise.join(temp, how = "inner")

#Scatter plot with tendency line
ax = sns.regplot(x = "MIGRATE1", y = "UNEMPLOYMENT", data = ipums_labor, robust = True)
ax.set_xlabel("Number of migrants living abroad 1 year ago")
ax.set_ylabel("Unemployment rate")
plt.plot([0, 1], [2500, 2500], 'r-', lw=0.5)

#REGRESSION ANALYSIS. Logaritmos de unemployment y migración: si el número de migrantes aumenta en 1%,
#la tasa de desempleo aumenta o disminuye en x%
#checar que sí se aplica el PERWT
#probar regresión con efectos fijos por año y estado
#log de migrantes en t y t-1(creo que el comando es shift, lo vimos en la última clase)
formula = "np.log(UNEMPLOYMENT) ~ np.log(MIGRATE1) + AGE + SEX + NHISPANIC + C(COUNTY) + C(YEAR)"
ols = smf.wls(formula = formula, data = ipums_labor, weights = ipums_labor["PERWT"])
model = ols.fit()
model.summary()

#Including and examining fixed effects across states
model.params
COUNTY_vals = {1 : 0.0}
for k, v in model.params.items():
    if "COUNTY" not in k: continue
    f = int(k.replace("C(COUNTY)[T.", "").replace("]", ""))
    COUNTY_vals[f] = float(v)
#Mapa de EU con migración o empleo
plot_county(COUNTY_vals["col"])
