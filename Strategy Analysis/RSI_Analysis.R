# Plotting RSI indicators over time
plot(Dataset$Date, Dataset$RSI_14, type = "l", xlab = "Date", ylab = "RSI_14", main = "RSI_14 Over Time")
lines(Dataset$Date, Dataset$RSI_Weekly, col = "blue")
legend("topright", legend = c("RSI_14", "RSI_Weekly"), col = c("black", "blue"), lty = 1)

