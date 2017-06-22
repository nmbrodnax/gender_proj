## Gender Project
This project involves predicting the genders of individuals who are members of non-profit boards.  I used Python to clean the data and R to predict gender via the gender package. 

### Step 1: Data Cleaning ([Python](https://www.python.org/))

All source data were derived from IRS 990 filings.    

#### Loading Data 

The input file *personnel.csv* includes the names, titles, and organization identifiers for each individual, as well as the source of the information.  The input file *orgs.csv* includes an organization identifier as well as each organization's name, IRS identifier, location, and financials.  **Neither source nor input files are included in the repository**.

#### Formatting Names

The full names of board members comprised a variety of formats, such as `Jane Doe`, `Doe, Jane`, `Dr. Jane Doe`, and `Jane Doe, Jr`. In order to predict gender for each person, I needed to extract the first name from each full name.  I developed four functions to split each full name into four components: salutation, first name, last name, and suffix.

#### Saving the Output

The [names.py](names.py) script, which includes the preceding function definitions, produces the output file *output.csv*.  The file includes the following fields:

 - `id`: organization identifier associated with board member (*personnel.csv*)
 - `ez_file`: 1 if the record came from a 990EZ filing, 0 otherwise (manually added to *personnel.csv*)
 - `name`: full name of board member (*personnel.csv*)
 - `title`: title of board member (*personnel.csv*)
 - `source_file`: PRE if the 990 form was filed before 2008, POST otherwise (manually added to *personnel.csv*)
 - `org_name`: name of organization (*orgs.csv*)
 - `fy`: fiscal year of 990 filing (*orgs.csv*)
 - `first_name`: derived from 'name'
 - `salutation`: derived from 'name'
 - `last name`: derived from 'name'
 - `suffix`: derived from 'name'


### Step 2: Gender Prediction ([R](https://www.r-project.org/))

#### Using the gender R Package

I am using the [gender](https://github.com/ropensci/gender) R package to predict gender on the basis of each individual's first name and year of birth.  After installing the package (`'install.packages("gender")`) you must also download the gender package data by calling the `install_genderdata_package()` function with no arguments.  This only needs to be done once.

Gender prediction requires two elements: the first name of the individual, and the method that should be used for prediction.  The `gender()` function requires a name or array of first names, while the `gender_df()` function requires a dataframe with a column of first names.  There are four available methods based on datasets and methodologies: ssa, ipums, kantrowitz, and genderize.  See the gender package [documentation](https://github.com/ropensci/gender) for more information about each method.

Optional function parameters include year of birth (or a range of years) and country.  Assuming that a majority of board members would be at least 18 years old and no older than 100 at the time of the 990 filing, I calculated birth year ranges for each personnel record.  I did not include country information.

#### Loading Data

All first names analyzed are included in the *output.csv* file.  Before running the analysis, I created a vector of unique names.  

#### Predicting Gender

The different methods provide different results, so I analyzed the names using three of the methods (ssa, ipums, and kantrowitz) and compared the results.  I was not able to analyze names using the [genderize](https://genderize.io/) method because the number of names (~7,000) exceeded the API call limit of 1,000 names per day.

#### Saving the Output

The [gender.R](gender.R) script produces two files: *gender_output.csv* and *unmatched_names.csv*.

The file *gender_output.csv* includes all the fields from *output.csv* as well as the following:

 - `birth_min`: calculated fy - 100
 - `birth_max`: calculated fy - 17
 - `gender`: predicted using the gender package

The file *unmatched_names.csv* file includes a list of first names that were categorized as 'NA' or 'either' rather than 'male' or 'female'. The file includes the following fields:

 - `first_name`: unique name from 'gender_output.csv'
 - `ssa`: gender predicted by the 'ssa' method
 - `ipums`: gender predicted by the 'ipums' method
 - `kantrowitz`: gender predicted by the 'kantrowitz' method
 - `gender`: the most common gender prediction among methods
