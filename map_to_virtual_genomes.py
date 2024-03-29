#/usr/bin/python3

import time
import subprocess
import argparse
import yaml
import pickle
import pandas as pd
import time
from multiprocessing import Pool


# make index of genome and ribo-seq reads
def make_index(thread, genome, ribosome, tmp_file_location, genome_fasta, name):
    ribo_name = str(ribosome).split('/')[-1].split('.')[0]
    genomename = str(genome).split('/')[-1].split('.')[0]
    ribo_name = str(ribosome).split('/')[-1].split('.')[0]

    print('STAR --runThreadN {} --runMode genomeGenerate --genomeDir {} --genomeFastaFiles {}'.format(thread,tmp_file_location+'/',genome))

    subprocess.call('./requiredSoft/STAR --runThreadN {} --runMode genomeGenerate --genomeDir {} --genomeFastaFiles {}'.format(thread,tmp_file_location+'/',genome),shell=True)

    subprocess.call('bowtie-build --threads {} {} {}/{}'
                    .format(thread, ribosome, tmp_file_location, ribo_name),
                    shell=True, stdout=False)

#    subprocess.call('bowtie-build --threads {} {} {}/{}'
#                    .format(thread, genome, tmp_file_location, name+'.fa'),
#                    shell=True, stdout=False)

    subprocess.call('bowtie-build --threads {} {} {}/{}'.format(thread, genome_fasta, tmp_file_location,genome_fasta.split('/')[-1]),shell=True)

    print('bowtie-build --threads {} {} {}/{}'.format(thread, genome_fasta, tmp_file_location, genome_fasta.split('/')[-1]))
    print('-' * 100)
    print(get_time(), 'Make index successfully!')
    print('-' * 100)

def deal_raw_data(genome, raw_read, ribosome, thread, trimmomatic, riboseq_adapters, tmp_file_location,genome_fasta):
    print(get_time(), 'Start cleaning rawreads...')
    read_name = raw_read.split('/')[-1].split('.')[-2]
    ribo_name = str(ribosome).split('/')[-1].split('.')[0]
    without_rrna_reads = read_name+'.clean.without.rRNA.fastq'
    unmaped_reads = read_name+'.clean.without.rRNA.unmapped.fastq'
    print(get_time(), 'Loading reads form:', raw_read)
    print('-' * 100)

    # Transform sra to fastq format
    subprocess.call('fastq-dump {} -O {}'
                    .format(raw_read, tmp_file_location),
                    shell=True)
    
    # Filter out low quality reads by Trimmomatic
    subprocess.call('java -jar {} SE -phred33 '
                    '{} {} ILLUMINACLIP:{}:2:30:10 '
                    'LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:16'
                    .format(trimmomatic, tmp_file_location+'/'+read_name+'.fastq', read_name+'.clean.fastq', riboseq_adapters), shell=True)
    
    # Map clean reads to ribosome sequence by bowtie
    subprocess.call('bowtie -p {} -norc --un {} {} {} > {}.map_to_rRNA.sam'
                    .format(thread, tmp_file_location+'/'+without_rrna_reads, tmp_file_location+'/'+ribo_name, read_name+'.clean.fastq', ribo_name),
                    shell=True)

    print('bowtie -p {} -norc --un {} {} {} > {}.map_to_genome.sam'.format(thread, tmp_file_location+'/'+unmaped_reads, tmp_file_location+'/'+genome_fasta.split('/')[-1], tmp_file_location+'/'+without_rrna_reads, ribo_name))

    subprocess.call('bowtie -p {} -norc --un {} {} {} > {}.map_to_genome.sam'.format(thread, tmp_file_location+'/'+unmaped_reads, tmp_file_location+'/'+genome_fasta.split('/')[-1], tmp_file_location+'/'+without_rrna_reads, ribo_name),shell=True)
    

    
      
    print('-' * 100)
    print(get_time(), 'Finished clean process.')
    print('-' * 100)
    global cleanreads
    cleanreads = tmp_file_location+'/'+unmaped_reads

    genome_name = str(genome).split('/')[-1].split('.')[0]
    print(get_time(), 'Start mapping...')
    print('command:')
    # Path to tophat2 result:
    tophat_result = tmp_file_location+'/'+read_name+'_tophat_result'
    

    

    subprocess.call('./requiredSoft/STAR --runThreadN {} --outSAMtype BAM SortedByCoordinate --alignIntronMax 10 --genomeDir {} --readFilesIn {} --outFileNamePrefix {}'.format(thread,tmp_file_location+'/',tmp_file_location+'/'+unmaped_reads,tmp_file_location+'/all_bam/'+read_name),shell=True)

#    print('bowtie -p {} -norc {} {} > {}'
#                    .format(thread, tmp_file_location+'/'+genome_name+'.fa', cleanreads, tmp_file_location+'/all_bam/'+read_name+'.sam'))
    
#    subprocess.call('bowtie -p {} -norc {} {} > {}'
#                    .format(thread, tmp_file_location+'/'+genome_name+'.fa', cleanreads, tmp_file_location+'/all_bam/'+read_name+'.sam'), shell=True)

#    subprocess.call('samtools view {} > {}'.format(tmp_file_location+'/all_bam/'+read_name+'.sam',tmp_file_location+'/all_bam/'+read_name+'_accepted_hits.bam'),shell=True)

    print(get_time(), 'Finished mapping')
    print(get_time(), 'Start analysing...')
    print('rename bam file')
    a=tophat_result+'/accepted_hits.bam'
    print(a)
    
#    subprocess.call('mv {} {}'.format(tophat_result+'/accepted_hits.bam',tophat_result+'/'+read_name+'_accepted_hits.bam'), shell=True)
#    subprocess.call('mv {} {}'.format(tophat_result+'/'+read_name+'_accepted_hits.bam', tmp_file_location+'/all_bam'), shell=True)
    print('-'*100)    
#    subprocess.call('samtools {} {}'.format(tmp_file_location+'/all_bam/total.bam',tmp_file_location+'/all_bam/*_accepted_hits.bam'), shell=True)
#    subprocess.call(
#        'bedtools bamtobed -bed12 -i {}/{}_tophat_result/accepted_hits.bam > {}/{}_tophat_result/bamtobed_result.bed'
#            .format(tmp_file_location, read_name, tmp_file_location, read_name),
#        shell=True)
#    subprocess.call(
#        'bedtools merge -i {}/{}_tophat_result/bamtobed_result.bed -c 1 -o count > {}/{}_merge_result'
#            .format(tmp_file_location, read_name, tmp_file_location, read_name),
#        shell=True)


def find_reads_on_junction(tmp_file_location):
    result = pd.DataFrame(columns=['a', 'b', 'c', 'd'])
    junction_file = tmp_file_location+'/junction'
    merge_result_file = tmp_file_location+'/merge_result'
    reads_jun = []
    merge_result = pd.read_csv(merge_result_file, sep='\t', low_memory=True, header=None)
    merge_result.columns = ['a', 'b', 'c', 'd']

    junction = pickle.load(open(junction_file, 'rb'))
    for i in junction:
        if merge_result.loc[(merge_result.b < i) & (i < merge_result.c)].empty:
            pass
        else:
            print(merge_result.loc[(merge_result.b < i) & (i < merge_result.c)])
            result = result.append(merge_result.loc[(merge_result.b < i) & (i < merge_result.c)])
            reads_jun.append(i)
    #print(result)
    try:
        pickle.dump(result, open('RCRJ_result', 'wb'))
        pickle.dump(reads_jun, open('reads_jun', 'wb'))
    except:
        print('Error while dumping RCRJ_result')
    result.to_csv(tmp_file_location+'/junction_result', sep='\t', header=0, index=False)


def remove_tmp_file():
    subprocess.call('mkdir -p reads', shell=True)
#    subprocess.call('mv *.clean.without.rRNA.fastq ./reads', shell=True)
    subprocess.call('mkdir -p result', shell=True)
#    subprocess.call('rm *.fastq', shell=True)


def get_time():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    strnow = '[{tim}]'.format(tim=now)
    return strnow


def filter_and_map_reads():
    start = time.time()
    make_index()
    deal_raw_data()
    remove_tmp_file()
    stop = time.time()
    print('-' * 100)
    print(get_time(), 'Finished all pipline')
    hours = int(int((stop - start) / 60) / 60)
    print(get_time(), 'Totally run', hours, 'hours')
    print('-' * 100)


def main():
    parse = argparse.ArgumentParser(description='This script helps to clean reads and map to genome')
    parse.add_argument('-y', dest="yaml", required=True)
    args = parse.parse_args()

    yamlfile  = args.yaml
    file      = open(yamlfile)
    fileload  = yaml.load(file)
    raw_reads = fileload['raw_reads']
    thread    = fileload['thread']
    ribosome  = fileload['ribosome_fasta']
    trimmomatic = fileload['trimmomatic_jar']
    riboseq_adapters = fileload['riboseq_adapters']
    tmp_file_location = fileload['tmp_file_location']
    genome_fasta = fileload['genome_fasta']
    name = fileload['genome_name']
    genome = '{}/{}.fa'.format(tmp_file_location, name)
    
    subprocess.call('mkdir -p {}'.format(tmp_file_location+'/all_bam'),shell=True)
    make_index(thread, genome, ribosome, tmp_file_location, genome_fasta, name)

    # use multiprocess to deal raw reads
    p = Pool(len(raw_reads))
    for raw_read in raw_reads:
        print(raw_read)
        p.apply_async(deal_raw_data, args=(genome, raw_read, ribosome, thread, trimmomatic,riboseq_adapters,tmp_file_location,genome_fasta))
    p.close()
    p.join()


    subprocess.call('samtools merge -f {} {}'.format(tmp_file_location+'/all_bam/total.bam',tmp_file_location+'/all_bam/*Aligned.sortedByCoord.out.bam'), shell=True)
    subprocess.call(
        'bedtools bamtobed -bed12 -i {} > {}/bamtobed_result.bed'
            .format(tmp_file_location+'/all_bam/total.bam', tmp_file_location),
        shell=True)
    subprocess.call(
        'bedtools merge -i {}/bamtobed_result.bed -c 1 -o count > {}/merge_result'
            .format(tmp_file_location, tmp_file_location),
        shell=True)

    find_reads_on_junction(tmp_file_location)
    remove_tmp_file()


if __name__ == '__main__':
    main()

