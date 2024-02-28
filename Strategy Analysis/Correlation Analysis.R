# Calculating correlations between variables
correlation_matrix <- cor(OGDC[, c("Close", "Volume", "RSI_14")])

# Viewing correlation matrix
print(correlation_matrix)


