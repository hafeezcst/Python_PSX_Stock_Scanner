# Plotting daily fluctuation over time
plot(OGDC$Date, OGDC$Daily_Fluctuation, type = "l", xlab = "Date", ylab = "Daily Fluctuation", main = "Daily Fluctuation Over Time")

# Calculating average true range (ATR)
ATR <- ATR(HLC(OGDC[, c("High", "Low", "Close")]), n = 14)
