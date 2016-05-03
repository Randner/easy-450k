combat_results <- readRDS(defaults$combat_path)
pca_res <- prcomp(get_values(combat_results[[1]]))

## get phenotypes
#
# defaults$combat_phenotypes_table
# defaults$combat_batch_name
# defaults$combat_id_column_name
# defaults$combat_numeric_names
# defaults$combat_categorical_names

## calculate correlation coefficients between top 10 principal components
## and other things
res <- t(apply(pca_res$rotation, 2, function(pca) {
    #nums <- adply(defaults$combat_numeric_names, 1, function(name) cor.test(as.numeric(get(name, defaults$combat_phenotypes_table)), pca)$p.value, .id=NULL)
    nums <- sapply(defaults$combat_numeric_names, function(name) cor.test(as.numeric(get(name, defaults$combat_phenotypes_table)), pca)$p.value)
    cats <- sapply(defaults$combat_categorical_names, function(name) kruskal.test(pca, as.factor(get(name, defaults$combat_phenotypes_table)))$p.value)
    c(nums, cats)
}))
write.table(res, file=defaults$pca_cor_report, sep="\t", quote=F, row.names=T, col.names=NA)
