# gender.R
# Dula Gender Project
# NaLette Brodnax
# www.nalettebrodnax.com
# June 20, 2017

library(gender)
library(dplyr)
library(tidyr)

# load data
personnel <- read.csv("output.csv", header = TRUE)

# convert first name data to character datatype, make uppercase
personnel$first_name <- as.character(toupper(personnel$first_name))

# create birth year variables
personnel$birth_min <- as.character(personnel$fy - 100)
personnel$birth_max <- as.character(personnel$fy - 17)

# get gender values for each method
names <- unique(toupper(personnel$first_name))
gender_ssa <- gender(names, method = "ssa") 
gender_ipums <- gender(names, method = "ipums")
gender_kant <- gender(names, method = "kantrowitz")

# combine all method results into a data frame
gender_data <- merge(data.frame(names), gender_ssa[,c(1,4)],
                     by.x = "names", by.y = "name", all.x=TRUE)
gender_data <- merge(gender_data, gender_ipums[,c(1,4)],
                     by.x = "names", by.y = "name", all.x=TRUE)
gender_data <- merge(gender_data, gender_kant,
                     by.x = "names", by.y = "name", all.x=TRUE)
colnames(gender_data) <- c("name", "ssa", "ipums", "kantrowitz")

# predict gender based on most common result across methods
predicted_gender <- apply(gender_data[,c(2:4)], 1,
                          function(x) names(which.max(table(x))))
gender_data <- cbind(gender_data, 
                     data.frame(gender=as.character(predicted_gender),
                                stringsAsFactors = FALSE))
gender_data$gender[gender_data$gender=="NULL"] <- NA

# tally by gender
print(tally(group_by(gender_data, gender)))
unmatched_names <- gender_data[which(gender_data$gender == 'either' |
                                       is.na(gender_data$gender)),]

# merge personnel and gender data
personnel$first_name <- as.character(personnel$first_name)
data <- merge(personnel, gender_data[,c(1,5)], by.x = "first_name", 
              by.y = "name", all.x = TRUE)

# export data to csv
write.csv(data, "gender_output.csv", row.names = FALSE)
write.csv(unmatched_names, "unmatched_names.csv", row.names = FALSE)
