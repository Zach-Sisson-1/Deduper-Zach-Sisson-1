#!/usr/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0-20:00:00
#SBATCH --output=Deduper.%J.OUT
#SBATCH --error=Deduper.%j.err

SAM_file='/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/test.sam'
Umi_list='/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/STL96.txt'
output_name="Test.deduped"

/usr/bin/time -v Deduper.py -umi $Umi_list -sam $SAM_file -out $output_name