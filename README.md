# Migration and Employment

I. Research Question

In the last year, immigration has been at the center of political and economic debate in several countries. Some argue that immigrants snip jobs from American citizens, while others claim that many immigrants develop their own businesses and create jobs. We are interested in analyzing some of the effects that immigration to the United States has on specific socio-economic factors. The research question is: Does immigration in the United States increase employment in a state?

II. Summary



III. Literature Review

In general, the literature on migration comprises the impact of immigration on the employment and wages of the receiving country, the effect of remittances and brain drain in the country of origin, and the effect of social networks on emigration. Regarding the effects of immigration on growth and employment in the receiving country, the National Records Center estimated that in 1996 the immigration fiscal burden was 0.2 percent of GDP, while the immigration surplus was 0.1 percent. This represents a reduction of 0.1 of the annual income of U.S. residents. Probably the estimate has a margin of error so we cannot argue if the total impact of immigration on the U.S. economy is positive or negative (Hanson, 2007).

Moreover, Fairlie and Meyer (2003) use 1980 and 1990 U.S. Census microdata and find inconclusive results of the effects of immigrant self-employment on native self-employment. Őzden and Wagner (2014) in their study “Immigrant versus Natives? Displacement and Job Creation” find that immigration has a positive effect on the Malaysian labor market as the reduction of costs and the expansion of output compensate the displacement of some native workers. They estimate three fixed-effects models (industry-region-year): the effect of immigration on native employment, on native wages and on immigrant wages. Specifically, the results show that at the national level, a ten percent increase in immigrants (equal to a one percent increase in work force) results in an increase of 4.4% in native employment and 0.14% in native wages. 

Finally, there is also some literature on the impact of refugees on the local economy. Stevenson (2005) argues that refugees are able to make significant social, cultural and economic contributions to both the region they are settled in and to Australia as a whole. Jacobsen (2005) shows that refugees are mostly self‐employed and can create jobs and new markets for the host country. Omata & Kaplan (2013) found that 66% of interviewed refugees in Kampala, Uganda are running their own businesses (some have between 1 and 12 employees), and 51% of them are formal.

IV. Data

The datasets that we plan to use are:
1.    IPUMS- https://usa.ipums.org/usa-action/extract_requests/download- From this dataset we want to identify the people that are not U.S. citizens and that lived in a different country 1 or 5 years ago.
·     Migration status- where was the person living 1 and 5 years ago? (same state, another state, or another country)
·      Race (does not include Hispanic)
·      Hispanic
·      Age
·      Sex
·      Citizenship
2.    U.S. Department of Labor: Employment, Hours, and Earnings - State and Metro Area https://beta.bls.gov/dataQuery/find?fq=survey:[sm]&s=popularity:D. We want to obtain information on employment status for immigrants.
·      (Un)employment rates
·      Non-farm payrolls
The dataset will be panel data as we will have information for different states (depending on the information available) and years.

V. Descriptive Statistics



VI. Regression Analysis



Panel data allows to control for variables that do not change over time and that are unobservable for the same state such as cultural factors, as well as for variables that change over time, but not between entities such as national and international migration regulations or policies and the economic situation in the United States. Panel data, specifically the first differences and the fixed effects, allow us to eliminate or control by omitted variables, and, therefore, obtain unbiased estimates.

In this case, fixed effects were used since they are computationally more flexible. By including binary variables for each state, we are controlling for unobservable differences, and, therefore, estimating only the effect of immigration on employment. Each binary variable absorbs the particular effects of each state.

VII. Conclusions

The relationship between poverty and repatriation presents a problem of reverse causality which may bias the results. The question to be solved is whether immigration has an effect on employment in the United States. However, the causality can be the other way around, that is, employment in a certain state increases the number of people who immigrate to that state as it is more attractive to them.

It is recommended to perform an analysis with instrumental variables, for example, historical migratory flows by state.

VIII. References

Cağlar Őzden and Mathis Wagner (2014). Immigrant versus Natives? Displacement and Job Creation. The World Bank, Policy Research Working Paper 6900: 1-63.
Hanson, G. (2007). The Economic Logic of Illegal Immigration. Council on Foreign, Council Special Report No. 26.

Jacobsen, K. (2005). The Economic Life of Refugees. Bloomfield: Kumarian Press.

Omata, Naohiko and Josiah Kaplan (2013). Refugee livelihoods in Kampala, Nakivale and Kyangwali refugee settlements: Patterns of engagement with the private sector. Refugee Studies Centre, Oxford Department of International Development, University of Oxford.

Robert W. Fairlie and  Bruce D. Meyer (2003). The Effect of Immigration on Native Self‐Employment. Journal of Labor Economics, Vol. 21, No. 3, pp. 619-650.

Stevenson, R. (2005). Refugees and economic contributions, Hopes fulfilled or dreams shattered? From resettlement to settlement- Responding to the needs of new and emerging refugee communities conference, Background paper. Centre for Refugee Research. University of New South Wales.
