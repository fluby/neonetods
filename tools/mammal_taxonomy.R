##read in data
setwd("C:/Users/kthibault/Dropbox/NEON/Mammals/Taxonomy/")
url <- 'http://www.departments.bucknell.edu/biology/resources/msw3/export.asp'
data <- download.file(url, 'msw3_tax.csv', mode = 'wb')
mswdata <- read.csv('msw3_tax.csv', header = TRUE)
neondata <- read.csv('mammal_codes_neonStatus.csv', header = TRUE)

##generate NEON mammal list
both <- merge(neondata, mswdata, by.x = c('genus','specificEpithet', 'infraspecificEpithet'), by.y = c('Genus','Species','Subspecies'), all.x = TRUE, sort = TRUE, suffixes = c('', 'msw'))

nameAccordingTo <- rep('Don E. Wilson & DeeAnn M. Reeder (editors). 2005. Mammal Species of the World. A Taxonomic and Geographic Reference (3rd ed), Johns Hopkins University Press, 2,142 pp.', length(both$taxonID))
nameAccordingToID <- rep("Wilson&Reeder2005", length(both$taxonID))

startUseDate <- rep('2012-05-01', length(both$taxonID))
startUseDate <- as.Date(startUseDate, "%Y-%m-%d")
endUseDate <- ''
speciesGroup <- ''
taxonomicStatus <- rep('accepted', length(both$taxonID))

##convert Order from all caps to Title case
order <- tolower(both$Order)
substring(order, 1, 1) <- toupper(substring(order, 1, 1))

a <- grep( "*comments*", both$Subgenus)
both$Subgenus[a] <- ""

commonname <- gsub("[^A-Za-z ]", "", as.character(both$CommonName))

mammal_accepted_names_list <- data.frame(as.character(both$taxonID), 
                                    as.character(both$taxonID), 
                                    as.Date(startUseDate, "%Y-%m-%d"),  
                                    endUseDate, 
                                    as.character(both$kingdom), 
                                    as.character(both$phylum), 
                                    as.character(both$class), 
                                    order, 
                                    as.character(both$Family), 
                                    as.character(both$Subfamily), 
                                    as.character(both$Tribe), 
                                    as.character(both$genus), 
                                    as.character(both$Subgenus), 
                                    as.character(speciesGroup), 
                                    as.character(both$specificEpithet), 
                                    as.character(both$infraspecificEpithet), 
                                    as.character(both$scientificName), 
                                    as.character(both$Author), 
                                    as.character(both$taxonRank), 
                                    commonname, 
                                    nameAccordingTo, 
                                    nameAccordingToID, 
                                    taxonomicStatus, 
                                    as.character(both$neonStatus))

names(mammal_accepted_names_list) <- c("taxonID",
                                       "acceptedTaxonID", 
                                       "startUseDate", 
                                       "endUseDate", 
                                       "kingdom", 
                                       "phylum", 
                                       "class", 
                                       "order",
                                       "family", 
                                       "subfamily", 
                                       "tribe", 
                                       "genus", 
                                       "subgenus", 
                                       "speciesGroup", 
                                       "specificEpithet",
                                       "infraspecificEpithet",
                                       "scientificName",
                                       "scientificNameAuthorship", 
                                       "taxonRank",
                                       "vernacularName",
                                       "nameAccordingTo",
                                       "nameAccordingtoID", 
                                       "taxonomicStatus", 
                                       "protocolCategory")


for (i in 1:nrow(mammal_accepted_names_list)){
  if (mammal_accepted_names_list$specificEpithet[i] == "sp.")
    {
    genusa <- mammal_accepted_names_list$genus[i]
    mammal_accepted_names_list$order[i] <- 
      mammal_accepted_names_list$order[mammal_accepted_names_list$genus == genusa][1]
    mammal_accepted_names_list$family[i] <-
      mammal_accepted_names_list$family[mammal_accepted_names_list$genus == genusa][1]
    mammal_accepted_names_list$subfamily[i] <-
      mammal_accepted_names_list$subfamily[mammal_accepted_names_list$genus == genusa][1]
    mammal_accepted_names_list$tribe[i] <-
      mammal_accepted_names_list$tribe[mammal_accepted_names_list$genus == genusa][1]
  }
}

write.csv(mammal_accepted_names_list, 'mammal_taxon_list.csv', na = "", row.names = FALSE)
