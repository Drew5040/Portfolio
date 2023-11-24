
# Andrew O'Drain
# Time Series: Forecasting Bitcoin Price

library(stats)
library(TSA)
library(leaps)
library(locfit)
library(astsa)
library(quantmod)
library(visdat)
library(ggplot2)
library(dplyr)
library(lubridate)
library(TSstudio)
library(simts)

getwd()
setwd('C:/Users/andre/Desktop/Temple/Fall 2022/Time Series/Project')

rm(list=ls())
options(scipen = 999)
ticker = c('BTC-USD' )
df = NULL

# PULL PRICES INTO DATA FRAME

for ( i in 1:length(ticker) ){
  # Initialize portfolio
  df2 = getSymbols( ticker[ i ], src = 'yahoo', auto.assign = FALSE, "1mo" )
  # Grabbed the adjusted close 
  df1 = df2[ ,6]
  # Bind returns to data frame
  time.series.btc = cbind( df, df1 )
  # Perform calculations
}  


df <- read.csv('just.price.csv')
time.series.btc <- ts(df, start = c(2014, 9),  deltat = 1/12)


# CHECK ATTRIBUTES, HEAD, TAIL, DIMENSIONS OF DATA: 1 x 4009 weekly data

print(time.series.btc)
head(time.series.btc)
tail(time.series.btc)
ncol(time.series.btc)
length(time.series.btc)
str(df)

# RENAME COLUMN


names(time.series.btc) <- c('BTC')
str(time.series.btc)

# CHECK FOR NA's THROUGH VISUALIZATION: 100% data is present

vis_dat(as.data.frame(df))
vis_miss(as.data.frame(df))
vis_dat(as.data.frame(df))
vis_miss(as.data.frame(df))

install.packages('TSstudio')

# EXPLORATORY ANALYSIS: PLOT AND VISUALIZE

month <- c("J", "A", "S", "O", "N", "D", "J", "F", "M", "A", "M", "J")
plot.ts(log(time.series.btc))
points(log(time.series.btc), pch = month)
plot(log(time.series.btc))



# If we look at the daily bitcoin chart that begins in September 17th 2014 it appears as though 
# the price has increased on a logarithmic scale. We can fit a quadratic model 
# The first price point starts at 457.33 and the last observation is at 17210.42. 




# Linear Model

linear.model <- lm(time.series.btc ~ time(time.series.btc))
summary(linear.model)

plot(ts( linear.model$fitted.values, freq = 12, start = c(2014 , 9)), ylab = 'Price', type = 'o',
     ylim = range( c(linear.model$fitted.values, time.series.btc))) 

lines(time.series.btc)



# Quadratic Model

timesq <- time(time.series.btc)^2

quadratic.model <- lm(log(time.series.btc) ~ time(time.series.btc) + timesq )
summary(quadratic.model)
            

plot(ts( quadratic.model$fitted.values, freq = 12, start = c(2014 , 9)), ylab = 'Price', type = 'o',
     ylim = range( c(quadratic.model$fitted.values, log(time.series.btc)))) 

lines(log(time.series.btc))



# Harmonic Model

harmonic.function <- harmonic(time.series.btc, m = 1)
harmonic.function


harmonic.model <- lm(time.series.btc ~ harmonic.function + time(time.series.btc))
summary(harmonic.model)
            
plot(ts( harmonic.model$fitted.values, freq = 12, start = c(2014 , 9)), ylab = 'Price', type = 'o',
     ylim = range( c(fitted(harmonic.model), time.series.btc))) 

lines(time.series.btc)

        
# Residual Analysis: Deterministic Trends

        
plot( y = rstudent(linear.model), x = as.vector(time(time.series.btc)), xlab = 'Time',
      ylab ='Standardized Residuals', type = 'o', col = 'blue', lwd = 2)
abline(h = 0, lwd = 2)       
        

plot( y = rstudent(quadratic.model), x = as.vector(time(time.series.btc)), xlab = 'Time',
      ylab ='Standardized Residuals', type = 'o', col = 'blue', lwd = 2)
abline(h = 0, lwd = 2)       

plot( y = rstudent(linear.model), x = as.vector(time(time.series.btc)), xlab = 'Time',
      ylab ='Standardized Residuals', type = 'o', col = 'blue', lwd = 2)
abline(h = 0, lwd = 2)       


# Independence

runs(rstandard(linear.model))
runs(rstandard(quadratic.model))
runs(rstandard(harmonic.model))


# Since our p-value of the runs test is .000000904, we can reject the null hypothesis
# and conclude the series was not produced in a random manner


# Normality

hist(rstandard(linear.model), xlab = 'Standardized Residuals', main = '')
qqnorm(rstandard(linear.model), main = '')
qqline(rstandard(linear.model))
shapiro.test(rstandard(linear.model))

hist(rstandard(quadratic.model), xlab = 'Standardized Residuals', main = '')
qqnorm(rstandard(quadratic.model), main = '')
qqline(rstandard(quadratic.model))
shapiro.test(rstandard(quadratic.model))

hist(rstandard(harmonic.model), xlab = 'Standardized Residuals', main = '')
qqnorm(rstandard(harmonic.model), main = '')
qqline(rstandard(harmonic.model))
shapiro.test(rstandard(harmonic.model))

# The standardized residuals are not normally distributed according to our histogram
# the qq-plot, and finally the Shapiro-Wilk test. We reject the null hypothesis
# with a p-value of .03 and conclude that the data is not normal. This is probably due 
# to the extreme outlier's toward the end of the data set.


# Auto-Correlation

par(mfrow = c(3, 1))
print(acf(rstudent(linear.model), main = 'Auto-Correlation', lag.max = 50))
print(acf(rstudent(linear.model), lag = 10))


print(acf(rstudent(quadratic.model), main = 'Auto-Correlation'), lag.max = 50)
print(acf(rstudent(quadratic.model), lag = 10))


print(acf(rstudent(harmonic.model), main = 'Auto-Correlation'), lag.max = 50)
print(acf(rstudent(harmonic.model), lag = 10))

# If we look at Lag(1) and lag(2) 
# we can see a very high correlation, .60 and .35, approximately and respectively.
# By lag(3) the correlation dips into insignificance. 
# Therefore, we can say that the series is correlated with itself


# Choosing the Best Out of Three Deterministic Models

AIC(linear.model)
# 2144.02

AIC(quadratic.model) 
# 166.29

AIC(harmonic.model) 
# 2159.42

BIC(linear.model) 
# 2151.84

BIC(quadratic.model) 
# 176.71

BIC(harmonic.model)
# 2159.42


# Based on the AIC and the BIC of the quadratic.model we can conclude that it is the best fit. 
# Not only are the AIC and the BIC values significantly lower than the
# linear and quadratic model, the RSE is significantly lower in the quadratic model. 


# Begin exploratory analysis for AR, ARIMA, and MA models

# We have successfully identified a strong trend through visualization. Lets check if we can 
# provide more statistical evidence for the trend by performing the Mann-Kendall test

# Test whether the series has a global trend or not

library(Kendall)

MannKendall(time.series.btc)
print(time.series.btc)
# With a p-value =.000000000000000222 we reject the null hypothesis, and conclude there
# is a strong trend in the data. We have identified it to be a quadratic trend. 


# Stationarity: De-trending then differencing

Yt <- diff(log(time.series.btc), differences = 1)

plot(Yt, xlab = 'Trading Months Since 2014', ylab = 'Price ( USD )', lwd = 1,
     main = 'Bitcoin USD Price')

abline(h = 0, col = 'red', lwd = 2)


# Check for trend again

MannKendall(Yt)

# We have successfully de-trended our series with the first-order differencing


# Perform the ADF test for Stationarity

library(fUnitRoots)
adfTest(Yt)
adf.test(Yt)

# After taking the first order difference we have confirmed that it is trend-stationary
# We still have to check the stationarity of the variance because the ADF test only concludes
# the mean is stationary and not the variance


# Check ACF plots

sample.acf <- auto_corr(Yt, lag.max = 50, type = 'correlation' )
plot(sample.acf, main = 'Yt')

set.seed(123)
rw.simulation <- arima.sim(list(order = c(0, 1, 0)), n = 250)
plot(rw.simulation)

rw.diff.log <- diff(rw.simulation, differences = 1)
rw.diff.log
rw.diff.log[1] = 0.11
rw.diff.log

sample.rw.acf <- auto_corr(rw.diff.log, lag.max = 50, type = 'correlation')
plot(sample.rw.acf, main = 'Sim.Rwalk')

library(stats)
Box.test(Yt, lag = 1, type = 'Ljung-Box')

sd(log(time.series.btc))
sd(time.series.btc)
sd(Yt)


# AR(p) Models

plot(Yt, type = "o", col = 'orange', main = 'Bitcoin')
points(Yt, pch = 19, col = 'black' )

# 2.a)
# Method of Moments Coefficient Estimation

ar(Yt, order.max=3, aic=F, method='yw')

# 2.b)
# Least Squares Coefficient Estimation

ar(Yt, order.max=3, aic=F, method='ols')

# 2.c)
# Maximum Likelihood Coefficient Estimation

ar(Yt, order.max=3, aic=F, method='mle')
Yt
# Conclusion:

# MOM :   .5272 x  .1546     .1717
# OLS :   .5237    .1568 x   .1744 x
# MLE :   .5214    .1554     .1720

# The coefficients marked with an 'x' are the closest to the actual coefficients.
# For all intents and purposes, all three methods produced similar results.










