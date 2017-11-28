#lectures/08-stats/statistics_examples.ipynb

##Import programs
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, linregress
import matplotlib.pyplot as plt
%matplotlib inline
import statsmodels.formula.api as smf
import sqlite3

##Import seaborn as it will affect how our plots look
import seaborn as sns
sns.set_style("whitegrid", rc={'axes.linewidth': 2.5})
sns.set_context('notebook', font_scale=1.45, rc={"lines.linewidth": 3, "figure.figsize" : (7, 3)})

##Import data from IPUMS
ipums_1516 = pd.read_csv("IPUMS_2015-16.csv", usecols=["YEAR", "STATEFIP", "COUNTYFIPS", "PERWT", "SEX", "AGE", "HISPAN", "CITIZEN", "MIGRATE1"])

#seleccionar personas que no son ciudadanos de eu y que hace 1 año vivían en otro país
#no seleccionar personas que no respondieron si eran hispanos o no (9)
#no se toman en cuenta los estados con códigos 2 (Alaska), 3, 7, 14, 15 (Hawaii), 43 (Puerto Rico), 52 (Virgin Islands)
#se eliminan las filas que tienen cero en COUNTYFIPS
ipums_1516_filter=ipums_1516[(ipums_1516.CITIZEN != 0) & (ipums_1516.CITIZEN != 1) & (ipums_1516.CITIZEN != 2) & (ipums_1516.MIGRATE1 == 4) &
                        (ipums_1516.HISPAN != 9) & (ipums_1516.STATEFIP != 2) & (ipums_1516.STATEFIP != 3)
                        & (ipums_1516.STATEFIP != 7) & (ipums_1516.STATEFIP != 14) & (ipums_1516.STATEFIP != 15) & (ipums_1516.STATEFIP != 43) 
                        & (ipums_1516.STATEFIP != 52) & (ipums_1516.COUNTYFIPS > 0)]

#renombrar variables, por ejemplo, de 1 y 2 a 0 y 1 para sexo. Más fácil para sacar propociones
ipums_1516_filter["HISPAN2"] = 0
ipums_1516_filter.loc[ipums_1516_filter["HISPAN"] == 0,  "HISPAN2"] = 1
ipums_1516_filter["SEX2"] = 0
ipums_1516_filter.loc[ipums_1516_filter["SEX"] == 2,  "SEX2"] = 1

#Agrupar por county, estado y año el promedio de AGE, SEX2, HISPAN2 y la cuenta de MIGRATE1
ipums_1516_final=ipums_1516_filter.groupby(["COUNTYFIPS", "STATEFIP", "YEAR"]).agg({'AGE': 'mean', 'SEX2': 'mean', 'HISPAN2': 'mean', 'MIGRATE1': 'count'}).reset_index()

ipums_1516_final.COUNTYFIPS = ipums_1516_final.COUNTYFIPS.astype(str) #convert COUNTYFIPS to string
ipums_1516_final.STATEFIP = ipums_1516_final.STATEFIP.astype(str) 
ipums_1516_final.dtypes
ipums_1516_final['COUNTYFIPS'] = ipums_1516_final['COUNTYFIPS'].apply(lambda x: x.zfill(3)) #add leading zeros to COUNTYFIPS
ipums_1516_final['STATEFIP'] = ipums_1516_final['STATEFIP'].apply(lambda x: x.zfill(2))
ipums_1516_final["ID"] = ipums_1516_final["STATEFIP"] + ipums_1516_final["COUNTYFIPS"] #combine STATEFIP and COUNTYFIPS in one colummn
#no sé si tengamos que agregar leading zeros a STATEFIP. Checar cómo esta el código en archivos de ACS
ipums_1516_final.set_index('ID', inplace=True) #change the index to the new variable ID

#guardar cada archivo
ipums_1516_final.to_csv('IPUMSclean_15-16.csv')

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

### Codigo para merge CSVs
df_allyears = pd.DataFrame()
list = []
for num in range (2007,2016):
    filename = "ACS_" + str(num) + ".csv"
    df_oneyear = pd.read_csv(filename, index_col=None, header=1)
    df_oneyear ["year"] = num
    list.append(df_oneyear)
df_allyears = pd.concat(list)



##para limpiar archivos
files=["2007-08", "2009-10", "2011-12", "2013-14", "2015-16"]
for filename in files:    
    df = pd.read_csv("IPUMS"+ filename + '.csv', usecols=["YEAR", "STATEFIP", "COUNTYFIPS", "PERWT", "SEX", "AGE", "HISPAN", "CITIZEN", "MIGRATE1"])
    df2 = df[(df.CITIZEN != 0) & (df.CITIZEN != 1) & (df.CITIZEN != 2) & (df.MIGRATE1 == 4) &
                        (df.HISPAN != 9) & (df.STATEFIP != 2) & (df.STATEFIP != 3)
                        & (df.STATEFIP != 7) & (df.STATEFIP != 14) & (df.STATEFIP != 15) & (df.STATEFIP != 43) 
                        & (df.STATEFIP != 52) & (df.COUNTYFIPS > 0)]
    df2["HISPAN2"] = 0
    df2.loc[df2["HISPAN"] == 0,  "HISPAN2"] = 1
    df2["SEX2"] = 0
    df2.loc[df2["SEX"] == 2,  "SEX2"] = 1
    df3 = df2.groupby(["COUNTYFIPS", "STATEFIP", "YEAR"]).agg({'AGE': 'mean', 'SEX2': 'mean', 'HISPAN2': 'mean', 'MIGRATE1': 'count'}).reset_index()
    df3.COUNTYFIPS = df3.COUNTYFIPS.astype(str) #convert COUNTYFIPS to string
    df3.STATEFIP = df3.STATEFIP.astype(str) 
    df3.dtypes
    df3['COUNTYFIPS'] = df3['COUNTYFIPS'].apply(lambda x: x.zfill(3))
    df3['STATEFIP'] = df3['STATEFIP'].apply(lambda x: x.zfill(2))
    df3["ID"] = df3["STATEFIP"] + df3["COUNTYFIPS"]
    df3.set_index('ID', inplace=True) #change the index to the new variable ID
    df3.to_csv('IPUMSclean' + filename + '.csv')
    
    
