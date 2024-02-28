# Plotting AO and AO_SMA
plot(OGDC$Date, OGDC$AO, type = "l", xlab = "Date", ylab = "AO", main = "Accelerator Oscillator (AO)")
lines(OGDC$Date, OGDC$AO_SMA, col = "red")
legend("topright", legend = c("AO", "AO_SMA"), col = c("black", "red"), lty = 1)
