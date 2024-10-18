# Plotting closing prices over time
plot(Dataset$Date, Dataset$Close, type = "l", xlab = "Date", ylab = "Close Price", main = "Closing Prices Over Time")

# Calculating and plotting moving averages
MA_30 <- (Dataset$MA_30/2)
lines(Dataset$Date, MA_30, col = "red")
legend("topright", legend = c("Close", "MA_30"), col = c("black", "red"), lty = 1)




