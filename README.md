# Deduper

The utility of this script will be to address the issue of PCR duplicates in RNA-seq workflows. PCR duplicates can be the result of a bias in PCR amplification and if unfiltered, can lead to downstream expression bias. The script is designed for use after sequencing alignment, and will input a SAM file of uniqely mapped, single-end reads, along with a list of Unique Molcular Indexes (UMIs) of length 8, and ouput the SAM file, retaining only a single copy of each set of PCR duplicates.

Final script titled **Deduper.py**.
