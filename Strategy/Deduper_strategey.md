# De-Duplicating (Deduping) PCR reads

## Goal: The utility of this script will be to address the issue of PCR duplicates in RNA-seq workflows. PCR duplicates can be the result of a bias in PCR amplification and if unfiltered, can lead to downstream expression bias. The script is designed for use after sequencing alignment, and will input a SAM file of uniqely mapped, single-end reads, along with a list of Unique Molcular Indexes (UMIs) of length 8, and ouput the SAM file, retaining only a single copy of each set of PCR duplicates. 
____
## Input = SAM file, List of UMIs of length 8

## Algorithm Steps:

Open and Read in set of Umi's as a sorted list (Umi_list)

Sort the SAM file via QName (check if this will push headers down below, if so, change sort method)

Readlines(), outputting directly to file until start of line != '@'

Read in first SAM entry:
	
	{Reference_Dict} = {'QNAME': val; 'FLAG': val, 'RNAME':val, POS: val, etc}   #where 'val' is corresponding info from first entry

	Check if Umi in Qname is in Umi_list by looking at last 8 char of Qname     
		if yes: do nothing
		if no: grab nextline entry and use as reference instead (repeat check until first entry contains a Qname with an UMI that is in the given list)


4) Perform the following loop on SAM file:
	
		if readline() exists:             
				Test = readline()           
				Test_Dict = {'QNAME': val; 'FLAG': val, 'RNAME':val, POS: val, etc}, where val are the values extracted from this entry 
				
				Duplicate_test({Reference_Dict},{Test_Dict})    ##Compare Dictionary values, see functions
					If output == True:        ##meaning duplicate
						pass
					If output == False:      ##meaning not a duplicate
						Reference_Dict >> 'output SAM'   ##print SAM entry dictionary values to output file
						Reference_Dict == Test_Dict    ##Set Ref dict values to be equal to the new (unique) entry 
		
		else:                                          ##If this is the final line in SAM file
				Reference_Dict >> 'output SAM'        ##print SAM entry dictionary values to output file as Reference_Dict can't be a duplicate

5) Close file

## Output = Inputted SAM file, with only 1 copy of each PCR duplicate

***
## Functions

def Duplicate_test(Ref_dict, Test_dict) -> boolean:

```Function will take two dictionaries as arugments, corresponding to SAM entries and determine if the two SAM entries are PCR duplicates. Function will stop and return FALSE whenever a condition is not met.```
	
	##First checks umi dissimilarity: 
	Ref_Umi = Last 8 characters of Qname in Ref_dict
	Test_Umi = Last 8 charactrs of Qname in Test_dict

	If Test_Umi not in Umi_list:
		Return True                 ##Treats this as a duplicate to be thrown away, as the Umi is not in the source list              
	elif Test_Umi != Ref_Umi:        ##Can't be a duplicate
		Return False
	
	else:    ###Next checks chromosome number (Rname)
		Ref_chrom = 'Rname' from Reference_Dict
		Test_chrom = 'Rname' from Test_Dict
		if Test_chrom != Ref_chrom:       ##Then it can't be a duplicate
			Return False
		
		else:  ###Next checks strand
			Ref_strand = Strand_reader(Ref[FLAG])    ##See functions, will return either 'forward', or 'reverse' given bitflag 
			Test_strand = Strand_reader(Test[FLAG])  
			if Test_strand != Ref_strand:     ##Then it can't be a duplicate
				Return False
		
			else:   ###Next checks position, and accounts for softclipping 
			Ref_position = Position_correcter(Ref[position],Ref[Cigar])    ##See functions, will return an integer position 
			Test_position = Position_corrector(Test[position],Test[Cigar])
			if Test_position != Ref_position:          ##Then it can't be a duplicate
				Return False
			else:                   ###All conditions have been met for the entry to be a PCR duplicate
				Return True


Input:{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M},{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M}

Expected Output: True    ##True duplicate     

Input:{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 15, 'CIGAR':64M},{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M}

Expected Output: False    ##Different Position

Input:{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 13, 'POS': 10, 'CIGAR':64M},{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M}

Expected Output: False    ##Different Chromosome

Input:{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CAGGGCTC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M},{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M}

Expected Output: False  ##Different UMI

Input:{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 0, 'RNAME': 11, 'POS': 10, 'CIGAR':64M},{'Qname': 'NS500451:154:HWKTMBGXX:1:11101:24260:1121:CTGTTCAC', 'FLAG': 16, 'RNAME': 11, 'POS': 10, 'CIGAR':64M}

Expected Output: False  ##Different Strand

***
def Position_correcter(position,cigar) -> int:

```Function inputs a start position integer and cigar string from a SAM file and outputs a position that is corrected for any softclipping that occured.```

	if 2nd character in cigar is an 'S':        ##Assumes soft clipping value is single digit i.e [1-9]
		clip_value = integer of cigar at position 0  
	else:
		clip_value = 0              ##Must not be soft clipped at start
	return(position - clip_value)  

Input: 13,'1S64M'

Expected Output: 12

Input: 13,'1S64M2S'

Expected Output: 12

Input: 13,'64M1S'

Expected Output: 13

Input: 13,'64M'

Expected Output: 13
***
def Strand_reader(bitflag) -> string:

```Function inputs a Bitflag from a SAM file and outputs either 'forward' or 'reverse', depending on the which strand the sequence was aligned to.```

	if ((bitflag & 16) == 16:  
		return('reverse')
	else:                  ##Assumes SAM file only contains mapped reads, i.e 'segment unmapped' flag can not be true or else this will break. 
		return('forward')

Input: 16

Expected Output: 'reverse' 

Input: 0

Expected Output: 'forward' 

***
Key considerations:
- Throws away entries with Unmatching Umi's (treats them as duplicates) 
- Are Qnames always equal between duplicates? (does not account for that if answer = true )
- Assumes SAM file only contains mapped reads, i.e 'segment unmapped' flag not present in any entry's bitflag. 
- Do I need to account for specifics of the cigar string other than the info relevant for soft clipping? Only starting position should matter..?
- does softclipping remove at most 3 nt?