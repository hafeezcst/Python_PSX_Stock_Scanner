# Calculating percentage change
Pct_Change <- diff(OGDC$Close) / lag(OGDC$Close, default = OGDC$Close[1]) * 100

# Plotting percentage change over time
plot(OGDC$Date[-1], Pct_Change, type = "l", xlab = "Date", ylab = "Percentage Change", main = "Percentage Change Over Time")
