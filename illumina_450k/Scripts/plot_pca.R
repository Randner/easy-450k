options(bitmapType='cairo')
combat_results <- readRDS(defaults$combat_path)

pca_res <- prcomp(t(get_values(combat_results[[1]])))
labels <- sampleNames.Dataset(combat_results[[1]])

tiff(defaults$pca_plot_after_combat)
ggplot(data=as.data.frame(pca_res$x),
       aes(x = PC1,
           y = PC2,
           label = labels)) +
       geom_text(size = 4, hjust=-0.3, vjust = 0.5, color = "black", angle = 10) +
       geom_point(size = 4) + xlim(-150, 150) + ylim(-100, 100) +
       theme_bw() +
       theme(axis.text = element_text(size = 16),
             axis.title = element_text(size = 18),
             legend.text = element_text(size = 20),
             axis.title.x = element_text(vjust = -1.4))
dev.off()
