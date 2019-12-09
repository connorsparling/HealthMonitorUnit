import MIT_BIH_preprocess as preproc

segment_length = 100
filename = "Datasets/mitbih-database"
lead_placement = "MLII"
plot_type = None
downsample_amount = None
split_location = "center"
save_to_filename = "preprocessData/SectionData.csv"

preproc.preprocess(filename, lead_placement, split_location, downsample_amount, segment_length, plot_type, save_to_filename)