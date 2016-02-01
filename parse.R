#install.packages("jsonlite")
require(jsonlite)
#install.packages('gdata')
require(gdata)

#read in the raw pairs
pairs = fromJSON("pairs.json")

#read in the features from debug.xlsx
df = read.xls('debug.xlsx', sheet = 'datadays', header = T)



