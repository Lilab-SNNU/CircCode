# CircCode

### Introduction

CircCode is a Python3-base pipeline for translated circular RNA identification. It automatically tandem links sequence in series and processes a given ribosome profile data (including quality control, filtering and alignment). Finally, based on random forest and J48 classification, the final translated circular RNA was predicted. The user only needs to ***fill in the given configuration file*** and ***run the python scripts*** to get the predicted translated circular RNA.

![workflow](https://i.loli.net/2019/08/30/s2O7TcUiKSZYLMj.png)

---

### Requirement
#### Data:

- Genome sequence (fasta format)
- Candidate circRNA sequence (fasta/bed format)
- rRNA sequence (fasta format)
- Adapter sequence (fasta format)
- Ribosome profiling data (sra format)
- Coding and non-coding sequence (fasta format)
#### Software:

- bedtools (v.2.26.0+): (https://bedtools.readthedocs.io/en/latest/)
- bowtie (v.1.2.2+): (http://bowtie-bio.sourceforge.net/index.shtml)
- STAR (v.2.7.1+): (https://github.com/alexdobin/STAR)
- Python3 (v.3.6.5+): (https://www.python.org/)
- R language (v.3.4.4+): (https://www.r-project.org/)

#### python3 package:

- Biopython (v.1.72+): (https://pypi.org/project/biopython/)
- Pandas (v.0.23.3+): (https://pypi.org/project/pandas/)

#### R package:

- BASiNET: (https://github.com/cran/BASiNET)
- Biostrings: (http://www.bioconductor.org/packages/release/bioc/html/Biostrings.html)

#### Supported operating systems：
![](https://s2.ax1x.com/2019/08/30/mX31PK.th.jpg)

---
### Download
  Open the terminal and input:
  ```bash
  git clone https://github.com/PSSUN/CircCode.git
  ```
---
## Install required packages
  ```bash
  cd CircCode
  ./ Install.sh
  ```
  NOTE: This step is optional, If you have already met all the required packages in your environment, you don't need to do this step, you can run the python script directly.At the same time, you can also install the required installation packages to meet the software requirements.
---
### Usage

##### - You can run all CircCode pipeline by one script

1. Fill the config file (https://github.com/Sunpeisen/CircCode/blob/master/config.yaml), input full path of each required file.

2. Run bash script on command line  with your config file.

 ```bash
   sh one_step_script.sh config.yaml
 ```

##### - Or you can run CircCode step by step

  1. Fill the config file (https://github.com/Sunpeisen/CircCode/blob/master/config.yaml), input full path of each required file.

  2. Making virtual genomes

  ```python
   python3 make_virtual_genomes.py -y config.yaml
  ```
  3. Filter reads and compare to virtual genomes

  ```python
   python3 map_to_virtual_genomes.py -y config.yaml
  ```
  4. Find RPF-covered region on junction (RCRJ) and classification of RCRJ by sequence features

  ```python
   python3 find_RCRJ_and_classify.py -y config.yaml
  ```
  5. Find longest peptide of translated circRNA

 ```python
  python3 find_longest_pep.py -y config.yaml
 ```
---
### Run example

You can downlad the required sra file from [NCBI-SRA](https://www.ncbi.nlm.nih.gov/sra/SRR3495992), we also provide the other required files (includes genome.fa, genome.gtf etc.) in [example.tar.xz](https://github.com/PSSUN/CircCode/blob/master/example.tar.xz). Fill in the path of the corresponding file into the project corresponding to config.yaml. Then follow the steps mentioned above to run each script.

#### How to fill in the config.yaml file?

When opening the config file in text format, there are some lines that need to be filled in, they are:

 - genome_name： 
 
    Each fasta file has its own name. Similarly, this value represents the name of the virtual genome generated by CircCode. You can fill in any value here in text form (we strongly recommend using only English letters). Note that you only need to fill in the name here, no suffix is required, for example you should fill in 'textGenome' instead of 'textGenome.fa'.

 - genome_fasta:
 
   You need to fill in the absolute path of the corresponding species genome here (not the relative path!)
   
 - genome_gtf:
   
   You need to fill in the absolute path of the corresponding annotation file of species genome here (not the relative path!)
   
 - raw_reads:
 
   CircCode's identification of circRNAs with translational potential relies on the support of Ribo-Seq data, and you need to fill in the absolute path of the Ribo-Seq data in sra format. The sra data can be your own sequencing data or downloaded from the NCBI public database.This supports inputting multiple sra data and making predictions at the same time. It is allowed if you only provide one sra file for prediction.
   
  - ribosome_fasta:
  
    Here we need to provide rRNA data for the corresponding species in fasta format for filtering the Ribo-Seq data. Here you need to fill in the absolute path of this fasta file.
   
  - trimmomatic_jar:
  
    The absolute path to the trimmomatic_jar file, we have provided the trimmomatic_jar file in CircCode, you just need to fill in the absolute path of this file on your computer.
  
  - circrnas:
  
    The fasta file of the candidate circRNA, CircCode, is used to predict those circRNAs with translational potential from a given sequence of candidate circRNAs. This fasta file should contain all the candidate circRNAs and fill in the absolute path of this fasta file here.
  
  - riboseq_adapters:
    
    The absolute path of the adapters file for Ribo-Seq data.
    
  - coding_seq:
  
    The fasta file of the coding sequence in this species, if running on a small computer, in order to avoid memory overflow, this file should not be too large. Otherwise, you may get an error due to insufficient memory.
  
  - non_coding_seq:
  
    The fasta file of the non-coding sequence in this species, if running on a small computer, in order to avoid memory overflow, this file should not be too large. Otherwise, you may get an error due to insufficient memory.
  
  - result_file_location:
  
     Fill in the absolute path of a folder to hold the final run results.
  
  - tmp_file_location:
  
     Fill in the absolute path of a folder to hold the temporary files.
  
  - reads_type:
  
     The type of sequencing data, sequencing data is divided into single-ended and pairs-ended, corresponding, you need to fill in single or pair here
  
  - thread:
  
     The number of threads running, only the number in the input int format is supported here, for example: **1** or **2** or **3** or **4** or **5**...

**NOTE**：The test file is only used to test whether the software can run smoothly and does not represent the actual research results.


---
### Contact us

If you encounter any problems while using CircCode, please send an email (sps@snnu.edu.cn / glli@snnu.edu.cn) or submit the issues on GitHub (https://github.com/Sunpeisen/circCode/issues) and we will resolve it as soon as possible.
