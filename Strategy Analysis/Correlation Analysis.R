# Calculating correlations between variables
correlation_matrix <- cor(Dataset[, c("Close", "Volume", "RSI_14")])

# Viewing correlation matrix
print(correlation_matrix)
