# Calculating percentage change
Pct_Change <- diff(Dataset$Close) / lag(Dataset$Close, default = Dataset$Close[1]) * 100

# Plotting percentage change over time
plot(Dataset$Date[-1], Pct_Change, type = "l", xlab = "Date", ylab = "Percentage Change", main = "Percentage Change Over Time")
