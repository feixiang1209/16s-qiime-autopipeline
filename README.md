# 16s-qiime-autopipeline
This Pipeline can be used by beginners with zero bioinformatics background. By inputting one command it will finish all the analysis automatically, generating the feature table, diversity analysis and taxa-bar-plots, Phylogenetic tree, etc.

1. Before starting
   1) Put all the fastq.gz files in one folder.
   2) Create a meta data file in the same folder. Recommend to use tab delimited .txt format. It should contains at least two columns, the first column should be SampleID (or similar). 
      Sample names in the meta data file should match with the fastq.gz (name before the index, example "WW1_WW1_UDP0297-UDP0300_L001_R1_001.fastq.gz", put "WW1_WW1" in the meta data file).  The second          column should not consist of exactly one value.
   3) If it is the first time using the primer, train classifier is needed. Please download the silva seq and taxa files from the link below, and put them in the same folder above.
      If it is not the first time, a trained classifier file shoude put in the same folder.
2. Run the script
   1) Install qiime2 and activate qiime2.
   2) Install rarefy plugin.
      
      pip install git+https://github.com/yxia0125/q2-repeat-rarefy.git
   3) Run the script
      
      Example:
      
      python3 16s-qiime-qutopipeline.py --path=/home/test  --cutpf=CCTACGGGNGGCWGCAG --cutpr=GACTACHVGGGTATCTAATCC --truncf=260 --truncr=230 --meta=meta.txt  --train_classifier=yes --remove_mito_chlo=yes
      
      See help by:   python3 16s-qiime-qutopipeline.py --help

      --path               Requied, full path that the fastq.gz files were saved
      
      --cutpf              Requied, Forward primer sequence for cutadaptor
      
      --cutpr              Requied, Reverse primer sequence for cutadaptor
      
      --truncf             Requied, trunc length for Read1 in DADA2
      
      --truncr             Requied, trunc length for Read2 in DADA2
      
      --meta               Requied, name of the meta file
      
      --train_classifier   Requied, Yes or No, whether to train classifier
      
      --remove_mito_chlo   Optional, Yes or No, default no, whether to remove mitochondria and chloroplast      


   4) If train_classifier is needed, the script will ask for the name of silva seq and name of silva tax. If train_classifier is not needed, thescript will ask for the name of trained taxa file.
3. Result
   
   All the intermedite files will be saved in work folder. You will mainly need to check the output folder. Use below link to open .qzv files.
   https://view.qiime2.org/
   
   1) dada2_rep_seqs folder: You will find the rep_seqs in fasta format.
   2) dada2_stats folder: You will see a table with the denoising status. All the diversity analysis and normalize reads is based on the lowest reads from the non-chimeric numeric.
   3) feature_table folder: Contains the feature table.
   4) taxa-bar-plots.qzv: Bar plot of taxanomic.
   5) trained_classifier.qza: If train_classifier is enabled, this file will be here. You can use this file for future if using the same primer.
   6) rarefy_feature_table: Output after normalize the reads based on the lowest reads of the samples.
   7) filtered: Output of the result after removing the mitochondria and chloroplast. Only available if remove_mito_chlo is enabled.
   8) diversity: Diversity analysis, including alpha diversity and beta diversity.
