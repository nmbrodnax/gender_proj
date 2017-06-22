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
personnel <- unique(personnel)

# convert first name data to character datatype, make uppercase
personnel$first_name <- toupper(as.character(personnel$first_name))

# create birth year min/max (assuming personnel are ages 18 to 100 at filing)
personnel$birth_min <- as.character(personnel$fy - 100)
personnel$birth_max <- as.character(personnel$fy - 17)

# make a list with one of each name, make uppercase
names <- toupper(unique(personnel$first_name))

# predict gender using each method (excluding genderize due to 1k name limit)
gender_ssa <- gender(names, method = "ssa") 
gender_ipums <- gender(names, method = "ipums")
gender_kant <- gender(names, method = "kantrowitz")

# combine all gender prediction results into a dataframe
gender_data <- merge(data.frame(names), gender_ssa[,c(1,4)],
                     by.x = "names", by.y = "name", all.x=TRUE)
gender_data <- merge(gender_data, gender_ipums[,c(1,4)],
                     by.x = "names", by.y = "name", all.x=TRUE)
gender_data <- merge(gender_data, gender_kant,
                     by.x = "names", by.y = "name", all.x=TRUE)
colnames(gender_data) <- c("first_name", "ssa", "ipums", "kantrowitz")

# choose gender based on most common result across methods
predicted_gender <- apply(gender_data[,c(2:4)], 1,
                          function(x) names(which.max(table(x))))

# add the new predicted gender column to the dataframe, convert NULL to NA 
gender_data <- cbind(gender_data, 
                     data.frame(gender=as.character(predicted_gender),
                                stringsAsFactors = FALSE))
gender_data$gender[gender_data$gender=="NULL"] <- NA

# print a tally of genders, create a list of names with NA or 'either'
print(tally(group_by(gender_data, gender)))
unmatched_names <- gender_data[which(gender_data$gender == 'either' |
                                       is.na(gender_data$gender)),]

# merge personnel and gender data by matching first names
personnel$first_name <- as.character(personnel$first_name)
gender_data$first_name <- as.character(gender_data$first_name)
personnel_gender_data <- merge(personnel, gender_data[,c(1,5)], 
                               by = "first_name", all.x = TRUE)
personnel_gender_data <- unique(personnel_gender_data)

# export personnel and unmatched name data to csv files
write.csv(personnel_gender_data, "gender_output.csv", row.names = FALSE)
write.csv(unmatched_names, "unmatched_names.csv", row.names = FALSE)
