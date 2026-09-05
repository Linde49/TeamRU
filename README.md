# TeamRU
Hackathon

The BusinessValuation Class is the main logic of our solution. 
It calculates the conservative future value of a business using this mathematical equation:
 _future business value = ((SDE_weighted) x (1 + g)^n x m_

 SDE_weighted is the total financial benefit a single owner-operator gets from a business. It calculates the sum of income made in a good financial period and a slow financial period (the extremes)
 _((Good Period Income x % of periods that are Good) + (Slow Period Income x % of periods that are Slow)) x number of periods per year_
 Good Period Income is the sum of all the income in a good financial period
 Slow Period Income is the sum of all the income in a slow financial period
 number of periods per year is based on how periods are split (i.e., if the period is based on weekly returns then _number of periods per year = 52_

 The growth compounding factor (1 + g)^n. It projects today's SDE to the future.
 _g = (today's income / yesterday's income) - 1_
 n is the number of years the SDE is being projected forward

 The multiplier converts the earnings into a single lump-sum
 The base multiplier is 1.50 and it is reduced or increase base on the risk
 _Multiplier = 1.50 - riskDeductions_
riskDeductions = 

 
 
