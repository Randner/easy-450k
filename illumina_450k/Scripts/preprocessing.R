loaded_data <- readRDS(defaults$loaded_dataset_path)

normalized_dataset <- loaded_data %>>=%
       defaults$preprocessing_filter_samples_default %>>=%
       defaults$filter_probes_default  %>>=%
       defaults$normalize_default %>>=%
       defaults$filter_samples_default

saveRDS(normalized_dataset, file=defaults$preprocessed_dataset_path)
