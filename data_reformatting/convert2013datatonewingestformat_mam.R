setwd("C:/Users/kthibault/Dropbox/NEON/Mammals/Data/NEON")
##TO DO: filter out training data

#read in data ingest format
newformat <- read.csv("mam_dataingest_2014_20140414_v1.csv", header = TRUE)

#to connect to dodobase 
library(RJDBC)
path_to_jar = "C:/Program Files/postgresql-8.4-703.jdbc4.jar"
drv <- JDBC("org.postgresql.Driver", path_to_jar)
conn <- dbConnect (drv, "jdbc:postgresql://fsumysql.ci.neon.local:5432/dodobase", "fsu", "fsurocks")

sqlStatement <- paste("SELECT * FROM mammals_neon.capture_data_2013", sep="")
data_2013 <- dbGetQuery(conn, sqlStatement)

sqlStatement <- paste("SELECT * FROM mammals_neon.trapping_data_2013", sep="")
trappingdata_2013 <- dbGetQuery(conn, sqlStatement)

#make sure all site codes are in uppercase
trappingdata_2013$siteid <- toupper(trappingdata_2013$siteid)
trappingdata_2013$plotid <- toupper(trappingdata_2013$plotid)
data_2013$siteid <- toupper(data_2013$siteid)
data_2013$plotid <- toupper(data_2013$plotid)

##convert dates to bout numbers
date1 <-sub("([[:digit:]]{4})$", "-\\1", trappingdata_2013$eventdate) 
date2 <-sub("([[:digit:]]{2})$", "-\\1", date1) 
date <- as.Date(date2)
bout <- format(date, "%m")
sitebout <- paste(trappingdata_2013$siteid, bout, sep = "")

##create perbout_in table
require(stringr)
usitebout <- unique(sitebout)
boutStartDate <- function(siteboutid) {
  trappingdata_2013$eventdate[sitebout == siteboutid]
}

startDate <- rep(NA, length(usitebout))
site <- rep(NA, length(usitebout))
for (i in 1:length(usitebout)) {
  startDate[i] <- min(boutStartDate(usitebout[i]))
  site[i] <- str_extract(usitebout[i], "^[A-Z]{4}")
}

s1 <- gsub("([0-9]{4})$", "-\\1", startDate)
start <- as.Date((gsub("([0-9]{2})$", "-\\1", s1)), format = "%Y-%m-%d")

samplingProtocol <- rep("NEON.DOC.000481vB", length(usitebout))
nameAccordingToID <- rep("NEON.DOC.XXXXXvA", length(usitebout))
remarks <- rep(NA, length(usitebout))

mam_perbout_in <- data.frame(site, start, samplingProtocol, nameAccordingToID, remarks)
names(mam_perbout_in) <- newformat$fieldName[newformat$table == "mam_perbout_in"]

##create pernight_in table
splitnames <- function(technames){
  strsplit(technames, split = ";")  
}

aMeasuredBy <- rep(NA, length(trappingdata_2013$handler))
bMeasuredBy <- rep(NA, length(trappingdata_2013$handler))
aRecordedBy <- rep(NA, length(trappingdata_2013$handler))
bRecordedBy <- rep(NA, length(trappingdata_2013$handler))

for (i in 1:length(trappingdata_2013$handler)) {
  temp <- splitnames(trappingdata_2013$handler[i])
  aMeasuredBy[i] <- temp[[1]][1]
  bMeasuredBy[i] <- str_trim(temp[[1]][2])
  temp2 <- splitnames(trappingdata_2013$recordedby[i])
  aRecordedBy[i] <- temp2[[1]][1]
  bRecordedBy[i] <- str_trim(temp2[[1]][2])
}

###add in leading zero to plot numbers if missing
plots <- sub("([_])([0-9])([0-9])$", '_0\\2\\3', trappingdata_2013$plotid)

mam_pernight_in <- data.frame(plots, date, trappingdata_2013$trapsset, trappingdata_2013$remarks,aMeasuredBy,  bMeasuredBy, aRecordedBy, bRecordedBy)
names(mam_pernight_in) <- newformat$fieldName[newformat$table == "mam_pernight_in"]

temp <- data.frame(unique(c(aMeasuredBy,  bMeasuredBy, aRecordedBy, bRecordedBy)))

##create capturedata_in table
date1 <-sub("([[:digit:]]{4})$", "-\\1", data_2013$eventdate) 
date2 <-sub("([[:digit:]]{2})$", "-\\1", date1) 
date <- as.Date(date2)

plots <- sub("([_])([0-9])([0-9])$", '_0\\2\\3', data_2013$plotid)

data_2013$idqcode <- str_replace(data_2013$idqcode, "N", "")
data_2013$idqcode <- str_replace(data_2013$idqcode, " ", "")
identificationQualifier <- str_replace(data_2013$idqcode, "CS", "cf. species")

mam_capturedata_in <- data.frame(date, plots, data_2013$trapcoordinate, data_2013$trapstatus, data_2013$taxonid, identificationQualifier, data_2013$sex, data_2013$lifestage, data_2013$testes, data_2013$nipples, data_2013$pregnant, data_2013$vagina, data_2013$hfl, data_2013$ear_length, data_2013$tail, data_2013$ttl, data_2013$wgt, data_2013$tagid, data_2013$tagreplaced, data_2013$fate, data_2013$blood, data_2013$fecal, data_2013$ear, data_2013$hair, data_2013$whisker, data_2013$remarks)
names(mam_capturedata_in) <- newformat$fieldName[newformat$table == "mam_capturedata_in"]

##write HARV data to csvs for working group
write.csv(subset(mam_perbout_in, mam_perbout_in$siteID == "HARV"), "mam_perbout_in_D01.csv", na = '', row.names = FALSE)
write.csv(mam_pernight_in, "mam_pernight_in_D01.csv", na = '', row.names = FALSE)
write.csv(mam_capturedata_in, "mam_capturedata_in_D01.csv", na = '', row.names = FALSE)
