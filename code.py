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


#Cleaning ACS database
files=["2007", "2008", "2009", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
for filename in files:
    ACS = pd.read_csv("ACS_"+filename+ ".csv", usecols=["GEO.id2", "HC01_EST_VC01", "HC02_EST_VC01", "HC03_EST_VC01", "HC04_EST_VC01"],
                      skiprows=[1])
    ACS = ACS.rename(columns={'GEO.id2': 'ID', 'HC01_EST_VC01': 'Population', 'HC02_EST_VC01': 'Labor Part.','HC03_EST_VC01': 'Employment', 'HC04_EST_VC01': 'Unemployment'})
    ACS.set_index('ID', inplace=True)
    ACS.to_csv('ACSclean' + filename + '.csv')

#merging ACS databases for all years
df_allyears = pd.DataFrame()
df_allyears = pd.read_csv("ACSclean2007.csv", index_col=None, header=0)
df_allyears["YEAR"] = 2007

for num in range (2008,2017):
    filename = "ACSclean" + str(num) + ".csv"
    df_oneyear = pd.read_csv(filename, index_col=None, header=0)
    df_oneyear["YEAR"] = num
    frames = [df_allyears, df_oneyear]
    df_allyears = pd.concat(frames)
df_allyears
df_allyears.to_csv('ACS_allyears.csv')

#Merging IPUMS databases for all years
df_allyears = pd.DataFrame()
df_allyears = pd.read_csv("IPUMSclean2007.csv", index_col=None, header=0)
df_allyears["Year_merge"] = 2007

for num in (2009,2011,2013,2015):
    filename = "IPUMSclean" + str(num) + ".csv"
    df_oneyear = pd.read_csv(filename, index_col=None, header=0)
    df_oneyear["Year_merge"] = num
    frames = [df_allyears, df_oneyear]
    df_allyears = pd.concat(frames)
df_allyears
df_allyears.to_csv('IPUMS_allyears.csv')

#MERGE
#definir las dos tablas
df_ACS = pd.read_csv("ACS_allyears.csv")
df_IPUMS = pd.read_csv("IPUMS_allyears.csv")
df_merged = df_ACS.merge(df_IPUMS, on = ['ID','YEAR'], how='inner')
df_merged.head()

#Analizando cómo se ven las dos tablas y buscando valores repetidos
df_ACS[df_ACS.ID == 1003] #arroja los valores iguales a 1003.
df_IPUMS[df_IPUMS.ID == 1003]

#limpiando columnas y generando el archivo merged
df_merged.drop(df_merged.columns[[0, 7, 8,
    9, 15]], axis=1, inplace=True)
df_merged.head()
df_merged.to_csv('ACSIPUMS_merged.csv')


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

df['lagprice'] = df['price'].shift(1)
df.shift(-1)

#Including and examining fixed effects across states
model.params
COUNTY_vals = {1 : 0.0}
for k, v in model.params.items():
    if "COUNTY" not in k: continue
    f = int(k.replace("C(COUNTY)[T.", "").replace("]", ""))
    COUNTY_vals[f] = float(v)
#Mapa de EU con migración o empleo
plot_county(COUNTY_vals["col"])

### Codigo para merge CSVs - VIEJO
df_allyears = pd.DataFrame()
list = []
for num in range (2007,2016):
    filename = "ACS_" + str(num) + ".csv"
    df_oneyear = pd.read_csv(filename, index_col=None, header=1)
    df_oneyear ["year"] = num
    list.append(df_oneyear)
df_allyears = pd.concat(list)




### Codigo para merge CSVs - ESTE SI SIRVE (para IPUMS le tenemos que quitar que genere una variable del año ¨year¨ segun yo es la linea que le puse el #)
df_allyears = pd.DataFrame()
df_allyears = pd.read_csv("ACSclean2007.csv", index_col=None, header=0)
df_allyears["Year"] = 2007

for num in range (2008,2017):
    filename = "ACSclean" + str(num) + ".csv"
    df_oneyear = pd.read_csv(filename, index_col=None, header=0)
 #   df_oneyear["Year"] = num
    frames = [df_allyears, df_oneyear]
    df_allyears = pd.concat(frames)
df_allyears
df_allyears.to_csv('ACS_allyears.csv')


##para limpiar archivos
files=["2007-08", "2009-10", "2011-12", "2013-14", "2015-16"]
for filename in files:
    df = pd.read_csv("IPUMS_"+ filename + '.csv', usecols=["YEAR", "STATEFIP", "COUNTYFIPS", "PERWT", "SEX", "AGE", "HISPAN", "CITIZEN", "MIGRATE1"])
    df2 = df[(df.CITIZEN == 3) & (df.MIGRATE1 == 4) & (df.HISPAN != 9) & (df.STATEFIP != 2) & (df.STATEFIP != 3)
                        & (df.STATEFIP != 7) & (df.STATEFIP != 14) & (df.STATEFIP != 15) & (df.STATEFIP != 43)
                        & (df.STATEFIP != 52) & (df.COUNTYFIPS > 0)]
    df2["HISPAN2"] = 0
    df2.loc[df2["HISPAN"] == 0,  "HISPAN2"] = 1
    df2["SEX2"] = 0
    df2.loc[df2["SEX"] == 2,  "SEX2"] = 1
    df3 = df2.groupby(["COUNTYFIPS", "STATEFIP", "YEAR"]).agg({'AGE': 'mean', 'SEX2': 'mean', 'HISPAN2': 'mean', 'MIGRATE1': 'count', 'PERWT': 'sum'}).reset_index()
    df3.COUNTYFIPS = df3.COUNTYFIPS.astype(str) #convert COUNTYFIPS to string
    df3.STATEFIP = df3.STATEFIP.astype(str)
    df3.dtypes
    df3['COUNTYFIPS'] = df3['COUNTYFIPS'].apply(lambda x: x.zfill(3))
    df3['STATEFIP'] = df3['STATEFIP'].apply(lambda x: x.zfill(2))
    df3["ID"] = df3["STATEFIP"] + df3["COUNTYFIPS"]
    df3.set_index('ID', inplace=True) #change the index to the new variable ID
    df3.to_csv('IPUMSclean_' + filename + '.csv')
    
#mapas
import geopandas as gdp
geo = gdp.read_file("cb_2016_us_county_500k.shp")
geo["ID"] = geo["STATEFP"] + geo["COUNTYFP"]
