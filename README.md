# qiime-autopipeline
This Pipeline can be used by beginners with zero bioinformatics background. By inputting one command it will finish all the analysis automatically, generating the feature table, diversity analysis and taxa-bar-plots. 
1. Before starting
   1) Put all the fastq.gz files in one folder.
   2) Create a meta data file in the same folder. Recommend to use tab delimited txt format. It should contains at least two columns, the first column should be SampleID (or similar).
      Sample names in the meta data file should match with the fastq.gz (name before the index, example "WW1_WW1_UDP0297-UDP0300_L001_R1_001.fastq.gz", put "WW1_WW1" in the meta data file). 
   3) If it is the first time using the primer, train classifier is needed. Please download the silva seq and taxa files from the link below, and put them in the same folder above.
      If it is not the first time, a trained classifier file shoude put in the same folder.
2. Run the script
   1) Install qiime2 and activate qiime2.
   2) Install rarefy plugin.
      pip install git+https://github.com/yxia0125/q2-repeat-rarefy.git
   3) Run the script. See help by:
      python3 qiime-autopipeline --help

      --path               Requied, full path that the fastq.gz files were saved
      --cutpf              Requied, Forward primer sequence for cutadaptor
      --cutpr              Requied, Reverse primer sequence for cutadaptor
      --truncf             Requied, trunc length for Read1 in DADA2
      --truncr             Requied, trunc length for Read2 in DADA2
      --meta               Requied, name of the meta file
      --train_classifier   Requied, Yes or No, whether to train classifier
      --remove_mito_chlo   Optional, Yes or No, default no, whether to remove mitochondria and chloroplast
    
    
       Example:
       python3 QIIME-workingnew.py --path=/home/test  --cutpf=CCTACGGGNGGCWGCAG --cutpr=GACTACHVGGGTATCTAATCC --truncf=260 --truncr=230 --meta=meta.txt  --train_classifier=yes --remove_mito_chlo=yes

   4) If train_classifier is needed, the script will ask for the name of silva seq and name of silva tax. If train_classifier is not needed, thescript will ask for the name of trained taxa file.
