# Plotting daily fluctuation over time
plot(Dataset$Date, Dataset$Daily_Fluctuation, type = "l", xlab = "Date", ylab = "Daily Fluctuation", main = "Daily Fluctuation Over Time")

# Calculating average true range (ATR)
ATR <- ATR(HLC(Dataset[, c("High", "Low", "Close")]), n = 14)
