# url <- 'http://help.ebird.org/customer/portal/kb_article_attachments/21637/original.xls?1381800781'
# data <- download.file(url, 'ebird_tax.xls', mode = 'wb')

##read in data
setwd("C:/Users/kthibault/Dropbox/NEON/Birds/Taxonomy/")
require(XLConnect)
wb <- loadWorkbook("eBird_taxonomy_1.54.xls")
ebirdtax <- readWorksheet(wb,1, header = TRUE)
aoudata <- read.csv('NACC_list_species.csv', header = TRUE)
alphacodes <- read.csv('LIST13_alphacodes.csv', header = TRUE)

###generate landbird list

NAlandbirds <- c('Columbiformes', 'Cuculiformes', 'Apodiformes', 'Coraciiformes', 'Piciformes', 'Passeriformes', 'Trogoniformes')
aoulandbirds <- subset(aoudata, aoudata$order %in% NAlandbirds)
aoulandbirdfamilies <- as.data.frame(sort(unique(aoulandbirds$family)))
colnames(aoulandbirdfamilies) <- c("family")
aoulandbirdgenera <- as.data.frame(sort(unique(aoulandbirds$genus)))
colnames(aoulandbirdgenera) <- c("genus")
aouother <- subset(aoudata, (aoudata$order %in% NAlandbirds) == "FALSE")

both <- merge(ebirdtax, alphacodes, by.x = 'SCI_NAME', by.y = 'SCINAME', all = TRUE, sort = TRUE, suffixes = c('ebird', 'alpha'))

require(stringr)
both$FAMILY <- str_extract(both$FAMILY, "[A-Za-z]*dae")

step1 <- subset(both, both$FAMILY %in% aoulandbirdfamilies$family)
genus <- str_extract(step1$SCI_NAME, "[A-Za-z]*")
step2 <- subset(step1, genus %in% aoulandbirdgenera$genus)
genus <- str_extract(step2$SCI_NAME, "[A-Za-z]*")
step2$SCI_NAME <- str_replace(step2$SCI_NAME, " x ", "_x_")

a <- str_split(step2$SCI_NAME, " ", n = 3)
genus <- sapply(a, "[", c(1))
specificEpithet <- sapply(a, "[", c(2))
infraspecificEpithet <- sapply(a, "[", c(3))
taxonID <- step2$SPEC
nameAccordingtoID <- "eBird_taxonomy_1.54; Pyle and DeSante 2014"
nameAccordingtoID <- rep(nameAccordingtoID, length(taxonID))
landbird <- "TRUE"
landbird <-rep(landbird, length(taxonID))

landbird_list <- cbind(step2$TAXON_ORDER, as.character(step2$SPEC), step2$ORDER1, step2$FAMILY, genus, specificEpithet, infraspecificEpithet, step2$SCI_NAME, step2$CATEGORY, step2$PRIMARY_COM_NAME, step2$SPECIES_CODE, as.character(step2$SPEC6), nameAccordingtoID, landbird)
landbird_list <- as.data.frame(landbird_list)
names(landbird_list) <- c("ebirdTaxonOrder","taxonID","orderName","family","genus","specificEpithet","infraspecificEpithet","scientificName","taxonRank","vernacularName","ebirdCode","SPEC6","nameAccordingtoID","landbird")

###generate other (non-landbird) list
aouother <- subset(aoudata, (aoudata$order %in% NAlandbirds) == "FALSE")
aouotherfamilies <- as.data.frame(sort(unique(aouother$family)))
colnames(aouotherfamilies) <- c("family")
aouothergenera <- as.data.frame(sort(unique(aouother$genus)))
colnames(aouothergenera) <- c("genus")

both$FAMILY <- str_extract(both$FAMILY, "[A-Za-z]*dae")

step1 <- subset(both, both$FAMILY %in% aouotherfamilies$family)
genus <- str_extract(step1$SCI_NAME, "[A-Za-z]*")
step2 <- subset(step1, genus %in% aouothergenera$genus)
genus <- str_extract(step2$SCI_NAME, "[A-Za-z]*")
step2$SCI_NAME <- str_replace(step2$SCI_NAME, " x ", "_x_")

a <- str_split(step2$SCI_NAME, " ", n = 3)
genus <- sapply(a, "[", c(1))
specificEpithet <- sapply(a, "[", c(2))
infraspecificEpithet <- sapply(a, "[", c(3))
taxonID <- step2$SPEC
nameAccordingtoID <- "eBird_taxonomy_1.54; Pyle and DeSante 2014"
nameAccordingtoID <- rep(nameAccordingtoID, length(taxonID))
landbird <- "FALSE"
landbird <-rep(landbird, length(taxonID))

nonlandbird_list <- cbind(step2$TAXON_ORDER, as.character(step2$SPEC), step2$ORDER1, step2$FAMILY, genus, specificEpithet, infraspecificEpithet, step2$SCI_NAME, step2$CATEGORY, step2$PRIMARY_COM_NAME, step2$SPECIES_CODE, as.character(step2$SPEC6), nameAccordingtoID, landbird)
nonlandbird_list <- as.data.frame(nonlandbird_list)
names(nonlandbird_list) <- c("ebirdTaxonOrder","taxonID","orderName","family","genus","specificEpithet","infraspecificEpithet","scientificName","taxonRank","vernacularName","ebirdCode","SPEC6","nameAccordingtoID","landbird")

all <- rbind(landbird_list, nonlandbird_list)
write.csv(all, 'bird_taxon_list.csv')
