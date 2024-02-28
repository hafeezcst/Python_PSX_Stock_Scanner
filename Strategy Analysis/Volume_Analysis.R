# Plotting volume over time
plot(OGDC$Date, OGDC$Volume, type = "l", xlab = "Date", ylab = "Volume", main = "Volume Over Time")

# Calculating and plotting 20-day moving average of volume
Volume_MA_20 <- SMA(OGDC$Volume, n = 20)
lines(OGDC$Date, Volume_MA_20, col = "blue")
