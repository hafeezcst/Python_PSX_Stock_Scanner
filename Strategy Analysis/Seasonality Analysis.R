# Extracting month from date
Dataset$Month <- format(as.Date(Dataset$Date), "%m")

# Calculating average closing price for each month
average_monthly_close <- aggregate(Close ~ Month, data = Dataset, FUN = mean)

# Plotting average closing price by month
barplot(average_monthly_close$Close, names.arg = month.name[1:12], xlab = "Month", ylab = "Average Close Price", main = "Average Close Price by Month")
