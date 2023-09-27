# 16s-qiime-autopipeline
# AUTHOR: Xiang Zhao
# Department: Bioscience Core Lab, King Abdullah University of Science and Technology
# Email:  xiang.zhao@kaust.edu.sa

This script is designed for beginners with no bioinformatics background and automatically performs the entire analysis pipeline through the input of a single command. The output of the pipeline includes feature tables and taxa bar-plots (options for normalized and non-normalized read counts and mitochondrial and chloroplast sequence removal), rep_seqs file, diversity analysis (alpha and beta diversity), phylogenetic trees (rooted and unrooted), rarefaction curve and a trained classifier file.
1.	Before you start
   
i.	Put all the fastq.gz files in one folder.

ii.	Create a metadata file in the same folder. It is recommended to use tab delimited .txt format. The file should contain at least two columns. The first column should be dedicated to the sample ID (label the column SampleID, or similar). Sample IDs in the metadata file must match with the fastq.gz file names (name before the index, e.g., "WW1_WW1_UDP0297-UDP0300_L001_R1_001.fastq.gz", "WW1_WW1" is the sample ID that must match the sample ID entry in the metadata file). At least one entry in the second column must be unique. For further details on metadata requirements, please refer to the Qiime tutorial at https://docs.qiime2.org/2022.11/tutorials/metadata/

iii.	If it is the first time using the primer set, the classifier must be trained. Please download the silva seq and taxa files from the link below and place them in the same folder as the files above. If it is not the first time, an existing trained classifier file must be placed in the same folder.
https://kaust-my.sharepoint.com/:f:/g/personal/zhaox0b_kaust_edu_sa/EtkYH84FycpPkdRjF1Wwe1EBGVj-bGasFfXEk2b_zobz-A?e=rhOWof

2.	Running the script
   
i.	Install miniconda, qiime2(only needed for the first time) and activate qiime2, following the instructions in the links below:

           https://educe-ubc.github.io/conda.html
  	
           https://educe-ubc.github.io/qiime2.html
  	
ii.	Install the rarefy plugin(only needed for the first time):

           pip install git+https://github.com/yxia0125/q2-repeat-rarefy.git
           
iii.	Run the script.

Example:
python3 16s-qiime-qutopipeline.py --path=/home/test --cutpf=CCTACGGGNGGCWGCAG --cutpr=GACTACHVGGGTATCTAATCC --truncf=260 --truncr=230 --meta=meta.txt --train_classifier=yes --remove_mito_chlo=yes
See help by: python3 16s-qiime-qutopipeline.py --help
--path: Required, full path where the fastq.gz files were saved
--cutpf: Required, Forward primer sequence for cutadaptor
--cutpr: Required, Reverse primer sequence for cutadaptor
--truncf: Required, length to which Read1 should be trimmed to in DADA2
--truncr: Required, length to which Read2 should be trimmed to in DADA2
--meta: Required, name of the meta file
--train_classifier: Required, Yes or No, depending on whether to the classifier needs to be trained
--remove_mito_chlo: Optional, Yes or No, default is no; if YES, choose whether mitochondrial sequences, chloroplast sequences or both should be removed
iv.	If train_classifier is needed, the script will ask for the names of the silva seq and silva tax files. If train_classifier is not needed, the script will ask for the name of the existing trained taxa file.
5.	Results
All the intermediate files will be saved in the “work” folder. The files-of-interest can mainly be found in the “output” folder. Use the following link to open .qzv files: https://view.qiime2.org/
i.	dada2_rep_seqs folder: Contains the rep_seqs file in fasta format.
ii.	dada2_stats folder: Contains a table with the denoising status. The diversity analysis and read normalization are based on the lowest read count from the “non-chimeric numeric” column in the table.
iii.	feature_table folder: Contains the feature table.
iv.	taxa-bar-plots.qzv: Contains relative abundance bar plots at various taxonomic levels.
v.	trained_classifier.qza: If train_classifier was enabled, this file will be here. You can use this file in the future for datasets that were generated with the same primers.
vi.	rarefy_feature_table: Output after read normalization to the sample with the lowest read count.
vii.	filtered: Output of the results after removal of mitochondrial and chloroplast sequences. Only available if remove_mito_chlo was enabled.
viii.	diversity: Diversity analysis, including alpha diversity and beta diversity.




