# Plotting closing prices over time
plot(OGDC$Date, OGDC$Close, type = "l", xlab = "Date", ylab = "Close Price", main = "Closing Prices Over Time")

# Calculating and plotting moving averages
MA_30 <- (OGDC$MA_30/2)
lines(OGDC$Date, MA_30, col = "red")
legend("topright", legend = c("Close", "MA_30"), col = c("black", "red"), lty = 1)




