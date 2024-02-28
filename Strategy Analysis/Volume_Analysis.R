# Plotting volume over time
plot(Dataset$Date, Dataset$Volume, type = "l", xlab = "Date", ylab = "Volume", main = "Volume Over Time")

# Calculating and plotting 20-day moving average of volume
Volume_MA_20 <- SMA(Dataset$Volume, n = 20)
lines(Dataset$Date, Volume_MA_20, col = "blue")
