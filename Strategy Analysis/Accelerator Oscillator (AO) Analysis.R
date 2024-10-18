# Plotting AO and AO_SMA
plot(Dataset$Date, Dataset$AO, type = "l", xlab = "Date", ylab = "AO", main = "Accelerator Oscillator (AO)")
lines(Dataset$Date, Dataset$AO_SMA, col = "red")
legend("topright", legend = c("AO", "AO_SMA"), col = c("black", "red"), lty = 1)
