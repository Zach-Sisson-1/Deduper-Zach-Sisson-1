#!/usr/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-20:00:00
#SBATCH --output=Deduper.%J.OUT
#SBATCH --error=Deduper.%j.err

SAM_file='/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper-Zach-Sisson-1/C1_SE_uniqAlign.sam'
Umi_list='/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper-Zach-Sisson-1/STL96.txt'
output_name="C1_SE_uniqAlign.deduped.sam"

conda activate bgmp_py39
/usr/bin/time -v ./Deduper.py -u $Umi_list -f $SAM_file -out $output_name