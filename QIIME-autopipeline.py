############################
# AUTHOR: Xiang Zhao
# Department: Bioscience Core Lab
# Email:  xiang.zhao@kaust.edu.sa
# This script uses qiime module to analysis amplicon sequencing result.
# This Pipeline, which works on either Ibex or workstation, can be used by beginners with zero bioinformatics background.
# By inputting one command it will finish all the analysis automatically, generating the feature table and taxa-bar-plots. 
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
parser.add_argument('--rarefy', type=str,required=False,default='No', help='Whether enable rarefy, Yes/YES/Y/yes/y or No/NO/N/no/n, default No')





args= parser.parse_args()





path=args.path
F_primer=args.cutpf
R_primer=args.cutpr
Trunc_F=args.truncf
Trunc_R=args.truncr
meta_file=args.meta
train_classifier=args.train_classifier
repeat_rarefy=args.rarefy

if repeat_rarefy="Yes" or repeat_rarefy="YES" or repeat_rarefy="yes" or repeat_rarefy="Y" or repeat_rarefy="y": 
    auto_rarefy=input("(Please choose if you want to auto rarefy step. Yes or No. If selecting Yes, the lowest reads after DADA2 will be selected.If selecting No, script will pause after DADA2 and wait for you to enter the Sampleing depth and repeated times.)  ")

    if auto_rarefy=="Yes" or auto_rarefy=="YES" or auto_rarefy=="yes" or auto_rarefy=="Y" or auto_rarefy=="y" :
        repeat_times=input("Please input repeat times for rarefy:")



    

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

##if data_format==".gz":
##    cmd_copy_data="rsync %s/*.fastq.gz %s" %(path,work)
##elif data_format==".fastq":
##    cmd_copy_data="rsync %s/*.fastq %s" %(path,work)

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

cmd_denoising="qiime dada2 denoise-paired --i-demultiplexed-seqs %s/trimmed-seqs.qza  --o-table %s/table.qza --o-representative-sequences %s/rep-seqs-dada2.qza --o-denoising-stats %s/dada2-stats.qza --p-trim-left-f 0 --p-trim-left-r 0 --p-trunc-len-f %s --p-trunc-len-r %s" %(work,work,work,work, Trunc_F, Trunc_R)



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


if (repeat_rarefy=="Yes" or repeat_rarefy=="YES" or repeat_rarefy=="Y" or repeat_rarefy=="y"or repeat_rarefy=="yes") and (auto_rarefy=="Yes" or auto_rarefy=="YES" or auto_rarefy=="yes" or auto_rarefy=="Y" or auto_rarefy=="y" ):
##    sampling_depth=input("Please input sampling depth:")    
##    repeat_times=input("Please input repeat times:")
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
                                  --o-rarefied-table %s/new_table.qza" %(work, sampling_depth, repeat_times, work)
    print(cmd_repeat_rarefy)
    os.system(cmd_repeat_rarefy)
elif (repeat_rarefy=="Yes" or repeat_rarefy=="YES" or repeat_rarefy=="Y" or repeat_rarefy=="y"or repeat_rarefy=="yes") and (auto_rarefy=="No" or auto_rarefy=="NO" or auto_rarefy=="N" or auto_rarefy=="no" or auto_rarefy=="n"):
    sampling_depth=input("Please input sampling depth:")    
    repeat_times=input("Please input repeat times:")
    
    
    cmd_repeat_rarefy="qiime repeat-rarefy repeat-rarefy --i-table %s/table.qza \
                                  --p-sampling-depth %s \
                                  --p-repeat-times %s \
                                  --o-rarefied-table %s/new_table.qza" %(work, sampling_depth, repeat_times, work)
    print(cmd_repeat_rarefy)
    os.system(cmd_repeat_rarefy)
elif repeat_rarefy=="No" or repeat_rarefy=="NO" or repeat_rarefy=="N" or repeat_rarefy=="n" or repeat_rarefy=="no":
    cmd_cp_table="cp %s/table.qza %s/new_table.qza" %(work, work)
    print(cmd_cp_table)
    os.system(cmd_cp_table)




### Train classifier

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

    
cmd_annotation="qiime taxa collapse --i-table %s/new_table.qza --i-taxonomy %s/taxonomy.qza --p-level 7 --o-collapsed-table %s/feature-table-class.qza" %(work, work, work)
print(cmd_annotation)
os.system(cmd_annotation)

if os.path.isfile("%s/feature-table-class.qza" %work) is False:
    print("Annotation error, please check")
    sys.exit()

feature_table_folder=output+"/feature_table"
cmd_taxa_tsv1="qiime tools export  --input-path %s/feature-table-class.qza   --output-path %s" %(work,feature_table_folder)
cmd_taxa_tsv2="biom convert -i %s/feature-table.biom -o %s/taxa_table.tsv --to-tsv " %(feature_table_folder, feature_table_folder)
print(cmd_taxa_tsv1)
print(cmd_taxa_tsv2)
os.system(cmd_taxa_tsv1)
os.system(cmd_taxa_tsv2)


#### Bar plot

cmd_bar="qiime taxa barplot --i-table %s/new_table.qza --i-taxonomy %s/taxonomy.qza --m-metadata-file %s/%s --o-visualization %s/taxa-bar-plots.qzv " %(work, work, path, meta_file, output)
print(cmd_bar)
os.system(cmd_bar)

if os.path.isfile("%s/taxa-bar-plots.qzv" %output) is False:
    print("Assign taxa error, please check")
    sys.exit()
else: print("Assign taxa done.")

cmd_remove="rm %s/*.fastq*" %work
print(cmd_remove)
os.system(cmd_remove)

print("rm %s/demux-paired-end.qza" %work)
os.system("rm %s/demux-paired-end.qza" %work)
print("Remove copied DATA done.")

print("All done.")



