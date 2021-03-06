# Immigration and Employment

## I. Research Question

In the last year, immigration has been at the center of political and economic debate in several countries. Some argue that immigrants snip jobs from American citizens, while others claim that many immigrants develop their own businesses and create jobs. We are interested in analyzing some of the effects that immigration to the United States has on specific socio-economic factors. The research question is: Does immigration in the United States increase employment per county?

## II. Literature Review

In general, the literature on migration comprises the impact of immigration on the employment and wages of the receiving country, the effect of remittances and brain drain in the country of origin, and the effect of social networks on emigration. Regarding the effects of immigration on growth and employment in the receiving country, the National Records Center estimated that in 1996 the immigration fiscal burden was 0.2 percent of GDP, while the immigration surplus was 0.1 percent. This represents a reduction of 0.1 of the annual income of U.S. residents. Probably the estimate has a margin of error so we cannot argue if the total impact of immigration on the U.S. economy is positive or negative (Hanson, 2007).

Moreover, Fairlie and Meyer (2003) use 1980 and 1990 U.S. Census microdata and find inconclusive results of the effects of immigrant self-employment on native self-employment. Őzden and Wagner (2014) in their study “Immigrant versus Natives? Displacement and Job Creation” find that immigration has a positive effect on the Malaysian labor market as the reduction of costs and the expansion of output compensate the displacement of some native workers. They estimate three fixed-effects models (industry-region-year): the effect of immigration on native employment, on native wages and on immigrant wages. Specifically, the results show that at the national level, a ten percent increase in immigrants (equal to a one percent increase in work force) results in an increase of 4.4% in native employment and 0.14% in native wages. 

Finally, there is also some literature on the impact of refugees on the local economy. Stevenson (2005) argues that refugees are able to make significant social, cultural and economic contributions to both the region they are settled in and to Australia as a whole. Jacobsen (2005) shows that refugees are mostly self‐employed and can create jobs and new markets for the host country. Omata & Kaplan (2013) found that 66% of interviewed refugees in Kampala, Uganda are running their own businesses (some have between 1 and 12 employees), and 51% of them are formal.

## III. Data

All analysis code for this project, including the code for cleaning the data, is included in a single jupyter notebook:

https://github.com/dbergmanns/Proyect/blob/master/Notebook4.ipynb

In order to obtain the number of immigrants living in the United States and the unemployment rate by county we used two different databases:

1. Integrated Public Use Microdata Surveys (IPUMS). We downloaded data by county from 2007 to 2016 in five different files (each with two years) as the files are too large to be downloaded in one single file. We identify people that are not U.S. citizens and that lived in a different country 1 year ago. In addition, we identify other variables that can be used as controls for our regression.
    - STATEFIP. Code for each state in the U.S.
    - COUNTYFIPS. Code for each county in the U.S.
    - MIGRATE1. Migration status. Where was the person living one year ago? (code=4)
    - CITIZEN. Citizenship status of respondents distinguishing between naturalized citizens and non-citizens (3)
    - HISPAN. If a person is hispanic (1, 2, 3 and 4) or not hispanic (0)
    - AGE
    - SEX

The datasets are available at: https://usa.ipums.org/usa-action/extract_requests/download

2. American Community Survey (ACS). Originally we were going to download the employment figures from the U.S. Department of Labor, however, we decided to do an analysis by county instead of by state. States such as California are very large so an analysis on immigration and employment at the state level may not be very illustrative. The U.S. Department of Labor does not have data at the county level so we decided to dowload employment figures from the ACS. We downloaded data by county from 2007 to 2016 in one CSV file for each year. Specifically, we downloaded the following variables:
    - FIPS county number. It includes the state and county code
    - Total population estimate
    - Labor force participation rate
    - Employment rate
    - Unemployment rate

The datasets are available at: https://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml

The final file with IPUMS and ACS datasets consists of panel data by county and year (2007-2016).

3. U.S. Census Bureau: coordinates for counties. This database will be used for elaborating the maps using geopandas.

The database is available at: https://www.census.gov/geo/maps-data/data/tiger-line.html

## IV. Descriptive Statistics

The code for the descriptive statistics and regression analysis is included in the same jupyter notebook:

 https://github.com/dbergmanns/Proyect/blob/master/Notebook4.ipynb

The bulk of the analysis is performed in python, pandas, geopandas, and statsmodels. 

Plottinng our variables of interest did not lead to any clear nor strong conclusions, hence we decided to run an OLS model regression. 

![screen shot 2017-12-01 at 6 33 52 pm](https://user-images.githubusercontent.com/32317863/33509336-3e59cb16-d6c6-11e7-9162-69d789863391.png)

The following maps show the number of immigrants and the unemployment rate by county in the US. Counties in California, Arizona, Texas and Florida have a high number of immigrants, between 88,000 and 7,000,000. Likewise, California and Arizona show a high unemployment rate (6.8 and 14.4).

![screen shot 2017-12-01 at 6 20 38 pm](https://user-images.githubusercontent.com/32317863/33509267-ad907530-d6c5-11e7-8f37-e9504800fea5.png)

![screen shot 2017-12-01 at 6 32 03 pm](https://user-images.githubusercontent.com/32317863/33509320-056e0d26-d6c6-11e7-964c-48a46161a6ee.png)


## V. Regression Analysis

We performed a weighted OLS regression to determine the impact of migration on employment/unemployment. We used the variables: Hispancs (percentage), age, and sex as control variables because we know that these variables may affect employment by themselves. In our first regresssion we found that as the number of immigrants increases, so does unemployment and this variable is significant at a 90% level. 

The relationship between immigration and employment presents a problem of reverse causality which may bias the results. The question to be solved is whether immigration has an effect on employment levels in the United States. However, the causality can be the other way around, that is, employment in a certain county or state increases the number of people who immigrate to that state as it is more attractive to them. 
To better address the issue of causality, we created a new variable (LAGMIGRATE). This variable represents a lag from the variable MIGRATE1 so that we can analyze the effect that immigrants that arrived a year earlier have had on employment/unemployment levels. 
After running a new weighted OLS regression that includes the lag variable, we found consistent results. The number of immigrants that arrived in a previous year increases unemployment. Particularly, for every immigrant that arrives, employment will decrease one percent the following year. And this is significant at a 99% level. We also observe a negative relationship between age and employment. There is a positive relationship between the number of males in the population and employment, though this is not significant.

## VI. Conclusions

We conclude that immigrants may have a negative impact on county employment levels. However, further analysis can be done utilizing data that measures businesses created by immigrants and their skill levels for our results to be concluisve. Additionally, having accees to data sets that are not samples could yield different results. It is recommended to perform an analysis with instrumental variables, for example, historical migratory flows by state to control for reverse causality. It is advisable to perform the same analysis using only unauthorized immigrants in the United States, instead of authorized and unauthorized immigrants as we used in this analysis.


## VIII. References

Cağlar Őzden and Mathis Wagner (2014). Immigrant versus Natives? Displacement and Job Creation. The World Bank, Policy Research Working Paper 6900: 1-63.
Hanson, G. (2007). The Economic Logic of Illegal Immigration. Council on Foreign, Council Special Report No. 26.

Jacobsen, K. (2005). The Economic Life of Refugees. Bloomfield: Kumarian Press.

Omata, Naohiko and Josiah Kaplan (2013). Refugee livelihoods in Kampala, Nakivale and Kyangwali refugee settlements: Patterns of engagement with the private sector. Refugee Studies Centre, Oxford Department of International Development, University of Oxford.

Robert W. Fairlie and  Bruce D. Meyer (2003). The Effect of Immigration on Native Self‐Employment. Journal of Labor Economics, Vol. 21, No. 3, pp. 619-650.

Stevenson, R. (2005). Refugees and economic contributions, Hopes fulfilled or dreams shattered? From resettlement to settlement- Responding to the needs of new and emerging refugee communities conference, Background paper. Centre for Refugee Research. University of New South Wales.
