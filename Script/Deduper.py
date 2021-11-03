#!/usr/bin/env python

import argparse
import Bioinfo as bf

'''This script is designed to remove PCR duplicates from a SAM file after alignment. If PCR duplicates are present in a SAM file, it can lead to bias in the analysis of differential expression. This script will retain only 1 copy of each PCR duplicate, retaining the first copy it encounters.'''


def get_args():
	parser = argparse.ArgumentParser(description="A script designed to remove PCR duplicates from a SAM file after alignment. If PCR duplicates are present in a SAM file, it can lead to bias in the analysis of differential expression. This script will retain only 1 copy of each PCR duplicate, retaining the first copy it encounters. Script can handle SAM file with Randomers and UMI's used.")
	parser.add_argument("-u", "--umi_list", help = "An optional text file containing a list of Unique Molecular Indexes used", type=str, required=False, default='Random')
	parser.add_argument("-out", "--output_file", help = "path for output file", type=str, required=True)
	parser.add_argument("-f", "--sam_file", help = "input SAM file, must be sorted by chromosome", type=str, required=True)
	return parser.parse_args()

args = get_args()


#Script if given a list of Umi's:
if args.umi_list != 'Random':
	Umi_list = []
	umi_length = 0
	with open(args.umi_list, "r") as umi_file:
		for line in umi_file:
			Umi_list.append(line.strip('\n').upper())
			umi_length = len(Umi_list[0])  #sets the variable for the length of umi used later for extraction of umi


	#Open output file for writing:
	output_file = open(args.output_file, 'w')




	#Open SAM file for parsing and begin parsing loop
	with open(args.sam_file, 'r') as sam_file:						
		Working_chrom = 'none' #will update this to reset reference dictionary each time a new group of chromosomes is being evaluated.
		for line in sam_file:
			if line[0] == '@': #if line is a header line
				output_file.write(line)
			else:  #line is not a header, must be an entry. 
				#break up line into components
				line_split = line.split('\t')
				Qname = line_split[0]
				umi = str(Qname[-(umi_length):]) #pulls out the UMI from the Qname
				Chromosome = str(line_split[2])
				position = int(line_split[3])
				cigar =  str(line_split[5])
				bitflag = int(line_split[1])
				strand = bf.strand_reader(bitflag)
				corrected_position = bf.Position_corrector(position,cigar,strand)

				if Working_chrom == Chromosome: #Same section, keep updating the dictionary
					pass
				else: 
					#Initililize Dictionary of Dictionaries for logging unique values seen
					Working_chrom = Chromosome
					ref_dict = {}
					for u in Umi_list:
						ref_dict[u] = {}
					
				
				try:  #Checks if umi is in list
					ref_dict[umi]
					try: #Checks if position has been seen before
						ref_dict[umi][corrected_position]
						if strand in ref_dict[umi][corrected_position]: #checks  if strand has been seen before
							pass
						else: #new strand, update and print line
							output_file.write(line) 
							ref_dict[umi][corrected_position].append(strand)
					except:  #new position, update and print line
						output_file.write(line) 
						ref_dict[umi][corrected_position] = []
				except:  #Umi not in list, ignore entry
					pass
	
	output_file.close()

#Script if Randomers are used:
else:
				#Initililize Dictionary of Dictionaries for logging unique values seen
	#Open output file for writing:
	output_file = open(args.output_file, 'w')

	#Open SAM file for parsing and begin parsing loop
	with open(args.sam_file, 'r') as sam_file:
		Working_chrom = 'none'
		for line in sam_file:
			if line[0] == '@': #if line is a header line
				output_file.write(line)
			else:  #line is not a header, must be an entry. 
				#break up line into components
				line_split = line.split('\t')
				Qname = line_split[0]
				barcode = bf.barcode_puller(Qname)#pulls out the UMI from the Qname
				Chromosome = str(line_split[2])
				position = int(line_split[3])
				cigar =  str(line_split[5])
				bitflag = int(line_split[1])
				strand = bf.strand_reader(bitflag)
				corrected_position = bf.Position_corrector(position,cigar,strand)
			
				if Working_chrom == Chromosome: #Same section, keep updating the dictionary
					pass
				else: 
					#Initililize Dictionary of Dictionaries for logging unique values seen
					Working_chrom = Chromosome
					ref_dict = {}

				try:  #Checks if barcode has been seen before
					ref_dict[barcode]
					try: #Checks if position has been seen before
						ref_dict[barcode][corrected_position]
						try: #Checks if Chromosome has been seen before
							ref_dict[barcode][corrected_position][Chromosome]
							if strand in ref_dict[barcode][corrected_position][Chromosome]:  #checks  if strand has been seen before
								pass
							else: #new strand, update and print line
								output_file.write(line) 
								ref_dict[barcode][corrected_position][Chromosome].append(strand)
						except: #new chromosome, update and print line
							output_file.write(line) 
							ref_dict[barcode][corrected_position][Chromosome] = []
							ref_dict[barcode][corrected_position][Chromosome].append(strand)
					except:  #new position, update and print line
						output_file.write(line) 
						ref_dict[barcode][corrected_position] = {}
						ref_dict[barcode][corrected_position][Chromosome]=[]
						ref_dict[barcode][corrected_position][Chromosome].append(strand)
				except:  #new barcode, add it and print line
					output_file.write(line)
					ref_dict[barcode] = {}
					ref_dict[barcode][corrected_position] = {}
					ref_dict[barcode][corrected_position][Chromosome]=[]
					ref_dict[barcode][corrected_position][Chromosome].append(strand)
					      

	output_file.close()

