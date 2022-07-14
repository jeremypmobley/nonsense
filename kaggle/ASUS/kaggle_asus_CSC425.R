

#Kaggle ASUS competition
#http://www.kaggle.com/c/pakdd-cup-2014/

#you must be a kaggle user to download the data but the signup process is quick and painless



#Load Data
repairtrain <- read.csv(file="C:\\Users\\jmobley3\\Downloads\\repairtrain.csv")
#saletrain <- read.csv(file="C:\\Users\\jmobley3\\Downloads\\saletrain.csv")
#outputtargetidmapping <- read.csv(file="C:\\Users\\jmobley3\\Downloads\\output_targetid_mapping.csv")
#samplesub <- read.csv(file="C:\\Users\\jmobley3\\Downloads\\samplesubmission.csv")



#create new variables
repairtrain$mod_comp <- paste(repairtrain$module_category,repairtrain$component_category, sep="_")
repairtrain$repair_yearguy <- as.numeric(substr(repairtrain$year.month.repair., 0, 4))
repairtrain$repair_monthguy <- as.numeric(substr(repairtrain$year.month.repair., 6, 7))
repairtrain$repair_monthguy <- ifelse(repairtrain$repair_monthguy<10, paste("0", repairtrain$repair_monthguy, sep=''), repairtrain$repair_monthguy)
repairtrain$repair_date <- paste(repairtrain$repair_yearguy, "-", repairtrain$repair_monthguy, "-", "01", sep='')



#create data set of total repairs by month by mod
totalmodrepairs <- aggregate(repairtrain$number_repair, by=list(repairtrain$module_category, repairtrain$repair_date), FUN=sum)
names(totalmodrepairs) <- c("mod", "date", "totalrepairs")
totalmodrepairs <- totalmodrepairs[order(totalmodrepairs$date),]
totalmodrepairs$date <- as.Date(totalmodrepairs$date)


#plot total repairs by mod over time
par(mfrow=c(1,1))
xrange <- range(totalmodrepairs$date)
yrange <- range(totalmodrepairs$totalrepairs)
colors <- rainbow(9)
plot(xrange, yrange, type='n', xlab="Time", ylab="Total Repairs", main="Total Repairs by Mod over time")
for (i in 1:9){
  looptotalmodrepairs <- subset(totalmodrepairs, mod==paste("M",i,sep=''))
  lines(looptotalmodrepairs$date, looptotalmodrepairs$totalrepairs, type='o', col=colors[i])}
legend(xrange[1], yrange[2], legend=1:9, cex=0.7, col=colors, lty=1)




#create data set of total repairs by mod_comp by month
totalmodcomprepairs <- aggregate(repairtrain$number_repair, by=list(repairtrain$mod_comp, repairtrain$repair_date), FUN=sum)
names(totalmodcomprepairs) <- c("mod_comp", "date", "totalrepairs")
totalmodcomprepairs <- totalmodcomprepairs[order(totalmodcomprepairs$mod_comp, totalmodcomprepairs$date),]
totalmodcomprepairs$date <- as.Date(totalmodcomprepairs$date)




#create a time series for one mod_comp
startguy <- as.Date("2006-01-01")
fulldates <- data.frame(date=seq(startguy, by='1 month', length=48), value=1:48)
m2_p24 <- totalmodcomprepairs[totalmodcomprepairs$mod_comp=="M2_P24",]
m2_p24_df <- merge(fulldates, m2_p24, all.x=TRUE)
m2_p24_df[which(is.na(m2_p24_df$totalrepairs)),"totalrepairs"] <- 0
m2_p24_ts <- ts(m2_p24_df$totalrepairs, frequency=12, start=c(2006,1))

#view time plot
plot(m2_p24_ts)

#view acf
acf(m2_p24_ts, lag.max=25)








#create auto-arima model
library(forecast)
m1 <- auto.arima(m2_p24_ts, seasonal=FALSE)

#create predictions from the model
m1forecasts <-  forecast(m1, h=17)
m1_preds <- m1forecasts$mean


#show plot time plot with predictions
preds <- NULL
for (j in 1:17){
  loopnewrowguy <- data.frame(forecastmonth=j,m1_preds[j])
  preds <- rbind(preds, loopnewrowguy)}
names(preds) <- c("forecastmonth", "preds")
preds$preds <- ifelse(preds$preds<0, 0, preds$preds)

rawdata <- data.frame(totalrepairs = m2_p24_df$totalrepairs)
predsdata <- data.frame(preds = preds[,"preds"])
names(predsdata) <- c("totalrepairs")
combined <- rbind(rawdata, predsdata)

plot(combined$totalrepairs, type='o', col=ifelse(as.numeric(rownames(combined))>(length(combined$totalrepairs)-17),"red","black"))



























