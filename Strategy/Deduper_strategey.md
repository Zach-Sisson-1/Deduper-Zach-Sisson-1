# De-Duplicating (Deduping) PCR reads

## Goal: The utility of this script will be to address the issue of PCR duplicates in RNA-seq workflows. PCR duplicates can be the result of a bias in PCR amplification and if unfiltered, can lead to downstream expression bias. The script is designed for use after sequencing alignment, and will input a SAM file of uniqely mapped, single-end reads, along with a list of Unique Molcular Indexes (UMIs) of length 8, and ouput the SAM file, retaining only a single copy of each set of PCR duplicates. 
____
## Input = SAM file, List of UMIs of length 8

## Algorithm Steps:

Open and Read in set of Umi's as a sorted list (Umi_list)

Initiliaze Umi Dictionary where keys = unique Umi, and values = another empty dictionary 

Open Output file
Open Input SAM file

Perform the following loop on SAM file:
	For line in file:
		Read in the next line

		If line starts with '@', print line directly to output, as its part of the header and restart the loop
		
		break up the line into variables UMI, Position, Flag, Rname, Cigar, etc, extracting components	
	
		
		Test whether or not UMI barcode is in the keys of UMI_dicionary, if so continue, else stop and restart loop (throw away entry)
		
		Correct the position value, accounting for any softclipping   #See functions, returns an integer
		Extract strand identity from bitflag                            ##See functions, returns integer value 0-1	
		

		Try calling the corrected position as a key in the UMI sub dictionary:
		
			If result == True:        ##Position was already seen, we will need to consider duplicate
				Search for the tuple (Rname, strand) within the UMI subdictionary, calling the position as the key.
				
				If results == True:    ## This must be a duplicate, throw out
					do nothing, restart loop        
				else:                   ##Not a duplicate, print and update
					Add the tuple of (Rname, strand) as a value of the Position key within the UMI subdirectory.
					Print entry to output file

			
			else:                      ##Position was not seen before, and therefore cannot be a duplicate
				assign entry variables Position, Rname, and Strand to UMI dictionary, adding to the subdictionaries for this given UMI where the corrected position value is the key, and the subvalue is a tuple in the form (Rname, strand). So the structure will be a dicionary (UMIS) of dictionaries (Positions) of tuples (Rname, strand).

				Print entry line to output file
		
5) Close file

## Output = Inputted SAM file, with only 1 copy of each PCR duplicate

***
## Functions

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
def Strand_reader(bitflag) -> int:

```Function inputs a Bitflag from a SAM file and outputs either 1 or '0, depending on the which strand the sequence was aligned to. 0=forward, 1=reverse```

	if ((bitflag & 16) == 16:   ##Indicating a map to the reverse strand
		return(1)       
	else:                  ##Assumes SAM file only contains mapped reads, i.e 'segment unmapped' flag can not be true or else this will break. 
		return(0)

Input: 16

Expected Output: 'reverse' 

Input: 0

Expected Output: 'forward' 

***
Key considerations:
- Throws away entries with Unmatching Umi's (treats them as duplicates) 
- Assumes SAM file only contains mapped reads, i.e 'segment unmapped' flag not present in any entry's bitflag. 
- Function accounts only for softclipping up to 9 nucleotides per sequence
- Algorithm search speed may be improved by switching order of Position and Chromosome search first. Positon search would yield fewer initial matches (faster for the dictionary tree search) but also requires a postion_correction function to be called at every entry. Will need to consider rearranging order of search. 