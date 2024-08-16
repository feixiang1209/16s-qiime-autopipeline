############################
# AUTHOR: Xiang Zhao
# Department: Bioscience Core Lab, King Abdullah University of Science and technology
# Email:  xiang.zhao@kaust.edu.sa
# This script uses qiime module to analysis amplicon sequencing result.
# This Pipeline, can be used by beginners with zero bioinformatics background.
# By inputting one command it will finish all the analysis automatically, generating the feature table, diversity analysis and taxa-bar-plots, Phylogenetic tree, etc.
###############################


import os
import argparse
import sys



parser = argparse.ArgumentParser(description='cutadaptor_DAD2_assigntaxa')


parser.add_argument('--path', type=str,required=True,help='Requied, full path that the fastq or fastq.gz files were saved')
parser.add_argument('--cutpf', type=str,required=True,help='Requied, Forward primer sequence for cutadaptor')
parser.add_argument('--cutpr', type=str,required=True,help='Requied, Reverse primer sequence for cutadaptor')
parser.add_argument('--truncf', type=str,required=True,help='Requied, trunc length for Read1 in DADA2')
parser.add_argument('--truncr', type=str,required=True,help='Requied, trunc length for Read2 in DADA2')
parser.add_argument('--meta', type=str,required=True,help='Requied, name of the meta file')
parser.add_argument('--train_classifier', type=str,required=True,help='Requied, Yes or No, whether to train classifier')
parser.add_argument('--remove_mito_chlo', type=str,required=False, default='No', help='Yes or No, default no, whether to remove mitochondria and chloroplast')



args= parser.parse_args()



path=args.path
F_primer=args.cutpf
R_primer=args.cutpr
Trunc_F=args.truncf
Trunc_R=args.truncr
meta_file=args.meta
train_classifier=args.train_classifier
remove_mito_chlo=args.remove_mito_chlo


rarefy_repeat_times=100



    

if train_classifier=="Yes" or train_classifier=="YES" or train_classifier=="yes" or train_classifier=="Y" or train_classifier=="y":
    silvaseq=input("Please input the name of silva seq: ")
    silvatax=input("Please input the name of silva tax: ")
elif train_classifier=="No" or train_classifier=="NO" or train_classifier=="no" or train_classifier=="N" or train_classifier=="n":
    trained_classifier=input("Please input the name of trained classfier: ")

    

work=path+"/work"
output=path+"/output"


print("mkdir %s" %work)
os.system("mkdir %s" %work)

print("mkdir %s" %output)
os.system("mkdir %s" %output)

##Copy DATA


cmd_copy_data="rsync %s/*.fastq.gz %s" %(path,work)
print(cmd_copy_data)
os.system(cmd_copy_data)
print("Copy DATA done.")


##Import DATA


cmd_import_data= "qiime tools import  --type 'SampleData[PairedEndSequencesWithQuality]'   --input-path %s --input-format CasavaOneEightSingleLanePerSampleDirFmt   --output-path %s/demux-paired-end.qza" %(work, work)
print(cmd_import_data)
os.system(cmd_import_data)

if os.path.isfile("%s/demux-paired-end.qza" %work) is False:
    print("Import data error, please check")
    sys.exit()

    
else: print("Import DATA done.")



##Remove Primer
cmd_remove_primer="qiime cutadapt trim-paired   --i-demultiplexed-sequences %s/demux-paired-end.qza   --p-front-f %s   --p-front-r %s   --o-trimmed-sequences %s/trimmed-seqs.qza   --p-discard-untrimmed   --p-minimum-length 200   --p-error-rate 0.2 " %(work,F_primer,R_primer, work)

print(cmd_remove_primer)
os.system(cmd_remove_primer)

if os.path.isfile("%s/trimmed-seqs.qza" %work) is False:
    print("Cutadapt error, please check")
    sys.exit()
    
else: print("Remove primer done.")

##Denoising

cmd_denoising="qiime dada2 denoise-paired --i-demultiplexed-seqs %s/trimmed-seqs.qza  --o-table %s/table.qza --o-representative-sequences %s/rep-seqs-dada2.qza --o-denoising-stats %s/dada2-stats.qza --p-trim-left-f 0 --p-trim-left-r 0 --p-trunc-len-f %s --p-trunc-len-r %s --p-n-threads 0" %(work,work,work,work, Trunc_F, Trunc_R)



cmd_repseq_qzv="qiime feature-table tabulate-seqs --i-data %s/rep-seqs-dada2.qza --o-visualization %s/rep-seq.qzv" %(work,work)
cmd_dada2stats_qzv="qiime metadata tabulate --m-input-file %s/dada2-stats.qza --o-visualization %s/dada2-stats.qzv" %(work,work)
cmd_table_qzv="qiime feature-table summarize --i-table %s/table.qza --o-visualization %s/table.qzv --m-sample-metadata-file %s/%s" %(work,work,path,meta_file)
print(cmd_denoising)
os.system(cmd_denoising)
if os.path.isfile("%s/table.qza" %work) is False or os.path.isfile("%s/rep-seqs-dada2.qza" %work) is False or os.path.isfile("%s/dada2-stats.qza" %work) is False:
    print("DADA2 error, please check")
    sys.exit()
print(cmd_repseq_qzv)
os.system(cmd_repseq_qzv)
print(cmd_dada2stats_qzv)
os.system(cmd_dada2stats_qzv)
print(cmd_table_qzv)
os.system(cmd_table_qzv)
dada2_stats_folder=output+"/dada2_stats"
cmd_dada2_stats_tsv="qiime tools export  --input-path %s/dada2-stats.qza   --output-path %s" %(work,dada2_stats_folder)
print(cmd_dada2_stats_tsv)
os.system(cmd_dada2_stats_tsv)


rep_seq_folder=output+"/dada2_rep_seqs"
cmd_dada2_repseqs_fasta="qiime tools export  --input-path %s/rep-seqs-dada2.qza   --output-path %s" %(work,rep_seq_folder)
print(cmd_dada2_repseqs_fasta)
os.system(cmd_dada2_repseqs_fasta)


dada2_table_folder=output+"/dada2_table"
cmd_dada2_table="qiime tools export  --input-path %s/table.qza   --output-path %s" %(work,dada2_table_folder)
lst1=[]
for file in dada2_table_folder:
    if ".biom" in file: lst1.append(file)
for file in lst1:  
    cmd_dada2_table_tsv="biom convert -i %s/%s -o %s/table-dada2.tsv --to-tsv "%(dada2_table_folder, file, dada2_table_folder)
    print(cmd_dada2_table_tsv)
    #os.system(cmd_dada2_table_tsv)



print("Denoising done.")


################################################
## Filter feature table
###if filter_table=True:
##################################################    




###Nomalize reads

t=open("%s/stats.tsv"%dada2_stats_folder ,'r')
lst=[]
for line in t:        
    try:
        aa=int(line.split("	")[-2])
        lst.append(int(line.split("	")[-2]))
    except: None
min_reads=min(lst)
sampling_depth=str(min_reads)


cmd_repeat_rarefy="qiime repeat-rarefy repeat-rarefy --i-table %s/table.qza \
                              --p-sampling-depth %s \
                              --p-repeat-times %s \
                              --o-rarefied-table %s/rarefy_table.qza" %(work, sampling_depth, rarefy_repeat_times, work)
print(cmd_repeat_rarefy)
os.system(cmd_repeat_rarefy)




### Train classifierf

if train_classifier=="Yes" or train_classifier=="YES" or train_classifier=="yes" or train_classifier=="Y" or train_classifier=="y":
    
    cmd_extract_reads ="qiime feature-classifier extract-reads  --i-sequences %s/%s --p-f-primer %s  --p-r-primer %s  --p-trunc-len  0  --p-min-length 100  --p-max-length 600  --o-reads %s/ref-seqs.qza" %(path,silvaseq, F_primer,R_primer, work)
    cmd_train_classifier="qiime feature-classifier fit-classifier-naive-bayes   --i-reference-reads %s/ref-seqs.qza  --i-reference-taxonomy %s/%s  --o-classifier %s/trained_classifier.qza" %(work, path, silvatax, path)
    trained_classifier="trained_classifier.qza"
    cmd_cp_trained="cp %s/trained_classifier.qza %s/trained_classifier.qza" %(path, output)

    print(cmd_extract_reads)
    os.system(cmd_extract_reads)
    print(cmd_train_classifier)
    os.system(cmd_train_classifier)
    print(cmd_cp_trained)   
    os.system(cmd_cp_trained)




### Assign taxa
cmd_assign_taxa="qiime feature-classifier classify-sklearn --i-classifier %s/%s --i-reads %s/rep-seqs-dada2.qza --o-classification %s/taxonomy.qza"  %(path,trained_classifier,work,work)
print(cmd_assign_taxa)
os.system(cmd_assign_taxa)

if os.path.isfile("%s/taxonomy.qza" %work) is False:
    print("Assign taxa error, please check")
    sys.exit()

    


cmd_annotation="qiime taxa collapse --i-table %s/table.qza --i-taxonomy %s/taxonomy.qza --p-level 7 --o-collapsed-table %s/feature-table-class.qza" %(work, work, work)
print(cmd_annotation)
os.system(cmd_annotation)

if os.path.isfile("%s/feature-table-class.qza" %work) is False:
    print("Annotation error, please check")
    sys.exit()

feature_table_folder=output+"/feature_table"
cmd_taxa_tsv1="qiime tools export  --input-path %s/feature-table-class.qza   --output-path %s" %(work,feature_table_folder)
cmd_taxa_tsv2="biom convert -i %s/feature-table.biom -o %s/taxa_table.tsv --to-tsv " %(feature_table_folder, feature_table_folder)
print(cmd_taxa_tsv1)
os.system(cmd_taxa_tsv1)
print(cmd_taxa_tsv2)
os.system(cmd_taxa_tsv2)

## Bar plot

cmd_bar="qiime taxa barplot --i-table %s/table.qza --i-taxonomy %s/taxonomy.qza --m-metadata-file %s/%s --o-visualization %s/taxa-bar-plots.qzv " %(work, work, path, meta_file, output)
print(cmd_bar)
os.system(cmd_bar)

if os.path.isfile("%s/taxa-bar-plots.qzv" %output) is False:
    print("Assign taxa error, please check")
    sys.exit()
else: print("Assign taxa done.")



### Assign taxa for rarefy
    


cmd_rarefy_annotation="qiime taxa collapse --i-table %s/rarefy_table.qza --i-taxonomy %s/taxonomy.qza --p-level 7 --o-collapsed-table %s/rarefy_feature-table-class.qza" %(work, work, work)
print(cmd_rarefy_annotation)
os.system(cmd_rarefy_annotation)


rarefy_feature_table_folder=output+"/rarefy_feature_table"
cmd_rarefy_taxa_tsv1="qiime tools export  --input-path %s/rarefy_feature-table-class.qza   --output-path %s" %(work,rarefy_feature_table_folder)
cmd_rarefy_taxa_tsv2="biom convert -i %s/feature-table.biom -o %s/rarefy_taxa_table.tsv --to-tsv " %(rarefy_feature_table_folder, rarefy_feature_table_folder)
print(cmd_rarefy_taxa_tsv1)
os.system(cmd_rarefy_taxa_tsv1)
print(cmd_rarefy_taxa_tsv2)
os.system(cmd_rarefy_taxa_tsv2)


## Bar plot

cmd_rarefy_bar="qiime taxa barplot --i-table %s/rarefy_table.qza --i-taxonomy %s/taxonomy.qza --m-metadata-file %s/%s --o-visualization %s/rarefy_taxa-bar-plots.qzv " %(work, work, path, meta_file, rarefy_feature_table_folder)
print(cmd_rarefy_bar)
os.system(cmd_rarefy_bar)

if os.path.isfile("%s/rarefy_taxa-bar-plots.qzv" %rarefy_feature_table_folder) is False:
    print("Assign rarefy taxa error, please check")    
else: print("Assign rarefy taxa done.")







### Remove mitochondria and chloroplast

if remove_mito_chlo =="YES" or remove_mito_chlo =="Y" or remove_mito_chlo =="yes" or remove_mito_chlo =="y" or remove_mito_chlo =="Yes":
    cmd_mk_filter_folder="mkdir %s/filtered" %output
    filter_folder=output+"/filtered"
    print(cmd_mk_filter_folder)
    os.system(cmd_mk_filter_folder)

    cmd_filter_seq_mito_chlo="qiime taxa filter-seqs   --i-sequences %s/rep-seqs-dada2.qza   --i-taxonomy %s/taxonomy.qza   --p-exclude mitochondria,chloroplast  --o-filtered-sequences %s/sequences-no-mitochondria-no-chloroplast.qza"%(work,work,work)
    print(cmd_filter_seq_mito_chlo)
    os.system(cmd_filter_seq_mito_chlo)


    cmd_filter_seq_fasta="qiime tools export  --input-path %s/sequences-no-mitochondria-no-chloroplast.qza   --output-path %s" %(work,filter_folder)
    print(cmd_filter_seq_fasta)
    os.system(cmd_filter_seq_fasta)



    
    cmd_filter_table_mito_chlo="qiime taxa filter-table --i-table %s/table.qza --i-taxonomy %s/taxonomy.qza --p-exclude mitochondria,chloroplast --o-filtered-table %s/table-no-mitochondria-no-chloroplast.qza" %(work,work,work)
    print(cmd_filter_table_mito_chlo)
    os.system(cmd_filter_table_mito_chlo)


        

    cmd_no_mito_chlo_annotation="qiime taxa collapse --i-table %s/table-no-mitochondria-no-chloroplast.qza --i-taxonomy %s/taxonomy.qza --p-level 7 --o-collapsed-table %s/no-mito-chlo-feature-table-class.qza" %(work, work, work)
    print(cmd_no_mito_chlo_annotation)
    os.system(cmd_no_mito_chlo_annotation)



    filter_feature_table_folder=filter_folder+"/filter_feature_table"
    cmd_filter_taxa_tsv1="qiime tools export  --input-path %s/no-mito-chlo-feature-table-class.qza   --output-path %s" %(work,filter_feature_table_folder)
    cmd_filter_taxa_tsv2="biom convert -i %s/feature-table.biom -o %s/taxa_table.tsv --to-tsv " %(filter_feature_table_folder, filter_feature_table_folder)
    print(cmd_filter_taxa_tsv1)
    os.system(cmd_filter_taxa_tsv1)
    print(cmd_filter_taxa_tsv2)
    os.system(cmd_filter_taxa_tsv2)

    ## Bar plot

    cmd_filter_bar="qiime taxa barplot --i-table %s/table-no-mitochondria-no-chloroplast.qza --i-taxonomy %s/taxonomy.qza --m-metadata-file %s/%s --o-visualization %s/filter_taxa-bar-plots.qzv " %(work, work, path, meta_file, filter_folder)
    print(cmd_filter_bar)
    os.system(cmd_filter_bar)

    



### Phylogenetic tree

cmd_mafft_alignment ="qiime alignment mafft --i-sequences %s/rep-seqs-dada2.qza --o-alignment %s/aligned_rep_seqs" %(work,work)
print(cmd_mafft_alignment)
os.system(cmd_mafft_alignment)


cmd_mask_alignment ="qiime alignment mask --i-alignment %s/aligned_rep_seqs.qza --o-masked-alignment %s/masked_aligned_rep_seqs.qza" %(work,work)
print(cmd_mask_alignment)
os.system(cmd_mask_alignment)


cmd_unrooted_tree ="qiime phylogeny fasttree --i-alignment %s/masked_aligned_rep_seqs.qza --o-tree %s/unrooted_tree" %(work,work)
print(cmd_unrooted_tree)
os.system(cmd_unrooted_tree)


cmd_rooted_tree ="qiime phylogeny midpoint-root --i-tree %s/unrooted_tree.qza --o-rooted-tree %s/rooted_tree" %(work,work)
print(cmd_rooted_tree)
os.system(cmd_rooted_tree)


### Diversity Analysis

cmd_core_diversity="qiime diversity core-metrics-phylogenetic --i-phylogeny %s/rooted_tree.qza --i-table %s/table.qza --p-sampling-depth %s --m-metadata-file %s/%s --output-dir %s/core_metrics_results" %(work,work, sampling_depth,path, meta_file, work)
print(cmd_core_diversity)
os.system(cmd_core_diversity)

diversity_output=output+"/diversity"
alpha_diversity=diversity_output+"/alpha_diversity"
beta_diversity=diversity_output+"/beta_diversity"

cmd_mk_diversity_output="mkdir %s/diversity" %output
print(cmd_mk_diversity_output)
os.system(cmd_mk_diversity_output)
cmd_mk_alpha="mkdir %s/alpha_diversity" %diversity_output
print(cmd_mk_alpha)
os.system(cmd_mk_alpha)
cmd_mk_beta="mkdir %s/beta_diversity" %diversity_output
print(cmd_mk_beta)
os.system(cmd_mk_beta)

cmd_alpha_1="qiime diversity alpha-group-significance --i-alpha-diversity %s/core_metrics_results/faith_pd_vector.qza --m-metadata-file %s/%s --o-visualization %s/faith_pd_group_significance" %(work,path,meta_file, alpha_diversity)
cmd_alpha_2="qiime diversity alpha-group-significance  --i-alpha-diversity %s/core_metrics_results/evenness_vector.qza --m-metadata-file %s/%s  --o-visualization %s/evenness_group_significance" %(work,path,meta_file, alpha_diversity)
cmd_alpha_3="qiime diversity alpha-group-significance --i-alpha-diversity %s/core_metrics_results/shannon_vector.qza --m-metadata-file %s/%s --o-visualization %s/shannon_group_significance"%(work,path,meta_file, alpha_diversity)

print(cmd_alpha_1)
os.system(cmd_alpha_1)

print(cmd_alpha_2)
os.system(cmd_alpha_2)

print(cmd_alpha_3)
os.system(cmd_alpha_3)


cmd_beta_1="cp %s/core_metrics_results/unweighted_unifrac_emperor.qzv %s/unweighted_unifrac_emperor.qzv" %(work,beta_diversity)
cmd_beta_2="cp %s/core_metrics_results/bray_curtis_emperor.qzv %s/bray_curtis_emperor.qzv" %(work,beta_diversity)
cmd_beta_3="cp %s/core_metrics_results/jaccard_emperor.qzv %s/jaccard_emperor.qzv" %(work,beta_diversity)
cmd_beta_4="cp %s/core_metrics_results/weighted_unifrac_emperor.qzv %s/weighted_unifrac_emperor.qzv" %(work,beta_diversity)

print(cmd_beta_1)
os.system(cmd_beta_1)

print(cmd_beta_2)
os.system(cmd_beta_2)

print(cmd_beta_3)
os.system(cmd_beta_3)

print(cmd_beta_4)
os.system(cmd_beta_4)



### Alpha Rarefaction Plots

cmd_alpha_rarefaction="qiime diversity alpha-rarefaction --i-table %s/core_metrics_results/rarefied_table.qza --p-max-depth %s --m-metadata-file %s/%s --p-steps %s --o-visualization %s/alpha_rarefaction.qzv" %(work,sampling_depth,path, meta_file,rarefy_repeat_times, output)
print(cmd_alpha_rarefaction)
os.system(cmd_alpha_rarefaction)





cmd_remove="rm %s/*.fastq*" %work
print(cmd_remove)
os.system(cmd_remove)

print("rm %s/demux-paired-end.qza" %work)
os.system("rm %s/demux-paired-end.qza" %work)
print("Remove copied DATA done.")

print("All done.")



