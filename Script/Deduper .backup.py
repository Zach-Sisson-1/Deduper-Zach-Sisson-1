#!/usr/bin/env python

import argparse

'''This script is designed to remove PCR duplicates from a SAM file after alignment. If PCR duplicates are present in a SAM file, it can lead to bias in the analysis of differential expression. This script will retain only 1 copy of each PCR duplicate, retaining the first copy it encounters.'''


def get_args():
	parser = argparse.ArgumentParser(description="A script to deduplex SAM files i.e remove duplicated PCR samples. Inputs include SAM file, an optional list of Unique Molecular Indexes (UMI's) used, ")
	parser.add_argument("-u", "--umi_list", help = "An optional text file containing a list of Unique Molecular Indexes used", type=str, required=False, default='Random')
	parser.add_argument("-out", "--output_file", help = "path for output file", type=str, required=True)
	parser.add_argument("-sam", "--sam_file", help = "input SAM file", type=str, required=True)
	return parser.parse_args()

args = get_args()

#Functions used
def Position_corrector(position,cigar) -> int: #Function accounts for softcipping up to 99 nucleotides
    '''Function takes a position and a cigar string, and determines if any soft clipping occured at the 
		beginning of the sequence. If so, the function will return a corrected position, accounting for softclipping, 
		and the original position if no soft clipping occured.'''
    cigar_string = str(cigar)
    position = int(position)
    try: 
        cigar_string[0:3].index('S')
        clip_value = int(cigar_string[0:(cigar_string.index('S'))])
    except: #no soft clipping at beginning, return original position.
        clip_value = 0
    return(int(position)-clip_value)

def strand_reader(bitflag) -> int:
	'''Function takes a bitflag from a SAM file as an input, and returns either 1 or 0, 
	indicating the sequence mapped to either the forward or reverse strand. 0=forward, 1=reverse '''
	if ((bitflag & 16) == 16): 
		return(1)
	else:			#Assumes SAM file only contains mapped reads, i.e 'segment unmapped' flag can not be true or else this will break.
		return(0)

def barcode_puller(Qname) -> str:
	'''Function inputs a Qname from SAM file and outputs the sequence barcode'''
	index = (Qname.rfind(":")+1) #finds starting position of randomer in string
	return(str(Qname[index:]))



#Script if given a list of Umi's:
if args.umi_list != 'Random':
	Umi_list = []
	umi_length = 0
	with open(args.umi_list, "r") as umi_file:
		for line in umi_file:
			Umi_list.append(line.strip('\n').upper())
			umi_length = len(Umi_list[0])  #sets the variable for the length of umi used later for extraction of umi)

	#Initililize Dictionary of Dictionaries for logging unique values seen
	ref_dict = {}
	for umi in Umi_list:
		ref_dict[umi] = {}

	#Open output file for writing:
	output_file = open(args.output_file, 'w')

	#Open SAM file for parsing and begin parsing loop
	with open(args.sam_file, 'r') as sam_file:
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
				strand = strand_reader(bitflag)
				corrected_position = Position_corrector(position,cigar)
			
				try:  #Checks if umi in in list
					ref_dict[umi]
					try: #Checks if position has been seen before
						ref_dict[umi][corrected_position]
						try: #Checks if Chromosome has been seen before
							ref_dict[umi][corrected_position][Chromosome]
							if strand in ref_dict[umi][corrected_position][Chromosome]:  #checks  if strand has been seen before
								pass
							else: #new strand, update and print line
								output_file.write(line) 
								ref_dict[umi][corrected_position][Chromosome].append(strand)
						except: #new chromosome, update and print line
							output_file.write(line) 
							ref_dict[umi][corrected_position][Chromosome] = []
							ref_dict[umi][corrected_position][Chromosome].append(strand)
					except:  #new position, update and print line
						output_file.write(line) 
						ref_dict[umi][corrected_position] = {}
						ref_dict[umi][corrected_position][Chromosome]=[]
						ref_dict[umi][corrected_position][Chromosome].append(strand)
				except:  #Umi not in list, ignore entry
					pass

	output_file.close()

#Script if Randomers are used:
else:
	#Initililize Dictionary of Dictionaries for logging unique values seen
	ref_dict = {}

	#Open output file for writing:
	output_file = open(args.output_file, 'w')

	#Open SAM file for parsing and begin parsing loop
	with open(args.sam_file, 'r') as sam_file:
		for line in sam_file:
			if line[0] == '@': #if line is a header line
				output_file.write(line)
			else:  #line is not a header, must be an entry. 
				#break up line into components
				line_split = line.split('\t')
				Qname = line_split[0]
				barcode = barcode_puller(Qname)#pulls out the UMI from the Qname
				Chromosome = str(line_split[2])
				position = int(line_split[3])
				cigar =  str(line_split[5])
				bitflag = int(line_split[1])
				strand = strand_reader(bitflag)
				corrected_position = Position_corrector(position,cigar)
			
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

