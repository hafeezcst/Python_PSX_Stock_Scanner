# Extracting month from date
OGDC$Month <- format(as.Date(OGDC$Date), "%m")

# Calculating average closing price for each month
average_monthly_close <- aggregate(Close ~ Month, data = OGDC, FUN = mean)

# Plotting average closing price by month
barplot(average_monthly_close$Close, names.arg = month.name[1:12], xlab = "Month", ylab = "Average Close Price", main = "Average Close Price by Month")
