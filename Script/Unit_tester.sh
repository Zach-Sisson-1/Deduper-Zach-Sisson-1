#!/usr/bin/bash

#Wrapper Script for individual unit tests. Reports on success/failure based on hardcoded tests

path='/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/'

#Unit test checks. See individual unit tests for content

cd /home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Script

#Tests script for Randomers
./Deduper.py -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/using_randomer.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/using_randomer.txt.out'; 

if cmp -s "${path}using_randomer.txt.out" "${path}using_randomer.expected.txt"; then
	echo "The script succesfully deduped the 'Randomer' unit test"
else 
	echo "The script FAILED on the 'Randomer' unit test"
fi

#Tests script for given UMI list
./Deduper.py -u '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/Example_UMI_list.txt' -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/using_umi.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/using_umi.txt.out';

if cmp -s "${path}using_umi.txt.out" "${path}using_umi.expected.txt"; then
	echo "The script succesfully deduped the 'using_umi' unit test"
else 
	echo "The script FAILED on the 'using_umi' unit test"
fi

#Tests script for differing only by position
./Deduper.py -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/position_test.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/position_test.txt.out' ;

if cmp -s "${path}position_test.txt.out" "${path}position_test.expected.txt"; then
	echo "The script succesfully deduped the 'Position' unit test"
else 
	echo "The script FAILED on the 'Position' unit test"
fi

#Tests script for differing only by chromsome 
./Deduper.py -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/chromosome_test.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/chromosome_test.txt.out' ;

if cmp -s "${path}chromosome_test.txt.out" "${path}chromosome_test.expected.txt"; then
	echo "The script succesfully deduped the 'Chromosome' unit test"
else 
	echo "The script FAILED on the 'Chromosome' unit test"
fi

#Tests script for differing only by strand
./Deduper.py -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/strand_test.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/strand_test.txt.out' ;

if cmp -s "${path}strand_test.txt.out" "${path}strand_test.expected.txt"; then
	echo "The script succesfully deduped the 'strand' unit test"
else 
	echo "The script FAILED on the 'strand' unit test"
fi

#Tests script for no duplicates
./Deduper.py -f '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/no_duplicates.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/no_duplicates.txt.out' ;

if cmp -s "${path}no_duplicates.txt.out" "${path}no_duplicates.expected.txt"; then
	echo "The script succesfully deduped the 'no_duplicates' unit test"
else 
	echo "The script FAILED on the 'no_duplicates' unit test"
fi

#Tests script for all duplicates
./Deduper.py -sam '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/all_duplicates.txt' -out '/home/zsisson2/bgmp/bioinformatics/Fall_2021/Deduper/Strategy/Unit_tests/all_duplicates.txt.out' ;

if cmp -s "${path}all_duplicates.txt.out" "${path}all_duplicates.expected.txt"; then
	echo "The script succesfully deduped the 'all_duplicates' unit test"
else 
	echo "The script FAILED on the 'all_duplicates' unit test"
fi