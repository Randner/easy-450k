bmiq_dataset <- readRDS(defaults$bmiq_path)

##meth_matrix <- get_values(bmiq_dataset[[1]])
##annotation <- get_annotation(bmiq_dataset[[1]])

combat_results <- bmiq_dataset %>>=% defaults$combat_default
saveRDS(combat_results, file=defaults$combat_path)
