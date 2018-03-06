library(seqinr)
library(ape)
args <- commandArgs(trailingOnly=TRUE)


data = read.fasta(args[1])
splittit <- strsplit(args[1], "[.]")[[1]]

splittit[2] <-  "nonmissing"
splittit[3] <- "nex"

newstr <- paste(splittit, collapse=".")

print(newstr)

write.nexus.data(data, file=newstr, format="dna")

