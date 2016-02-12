#install.packages("jsonlite")
require(jsonlite)
#install.packages('gdata')
require(gdata)

#read in the raw pairs
pairs = fromJSON("pairs.json")

#read in the features from debug.xlsx
df = read.xls('debug.xlsx', sheet = 'datadays', header = T)

######examples for bret
features = names(pairs) #vec of feature names


##anova
####remember get(i)
l = list()
for (i in features) {
    print('--------')
    print(i)
    #l[[i]] = lm(get(i) ~ measurement_method, data = df)
    l[[i]] = anova(lm(get(i) ~ measurement_method, data = df))
    print(l[[i]])
}


#str(l[[1]])
#print(anova(lm(peak_to_dusk_x_hrs ~ measurement_method, data = df)))


#####################
#get summaries of features
summ <- function(name) {
    d = df[,name]
    d = d[!is.na(d)]
    out = c(mean(d), sd(d))
    names(out) = c("mean", "sd")
    out
}
sapply(features, summ)

#####################
#boxplot everything in its own filename
genbox <- function(name) {
    d = df[,name]
    filename = paste(c(name,".pdf"), sep = "", collapse = "")
    pdf(filename)
    boxplot(d, main = name)
    dev.off()
}
sapply(features, genbox)

#####################
#sanity check for pairwise diffs
foo <- function(x) {
    x1 = max(x)
    x2 = min(x)
    min(x1 - x2, 24 + x2 - x1)
}
sanity <- function(name) {
    d = df[,name]
    d = as.numeric(d[!is.na(d)])
    sort(combn(d,2,foo))
}
pairs.fromraw = sapply(features,sanity)
pairs.fromjson = pairs

diff <- function(name){
    sum(abs(sort(pairs.fromraw[[name]]) - sort(pairs.fromjson[[name]])))
}
lapply(features, diff) #these should all be very small numbers


#####################
#boxplot in a a lattice 
boxplot.simple <- function(name){
    boxplot(df[,name],main = name)
}
par(mfrow=c(3,4))
sapply(features,boxplot.simple)
#dev.off


#####################
#make everything long instead of wide; this will require an aesthetic makeover -- talk to me if a plot like this will become useful. 
require(reshape2)
require(ggplot2)
#require(plyr)
df.long <- melt(df[,features])
ggplot(df.long, aes(x = variable, y = value)) + geom_boxplot()

##the long format also allows a simplification of a lot of the previous methods above. see, for example
ff <- function(df) {
    #do something to a sub data frame here that returns a simiilar dataframe. for example
    goodvalues = df$value[!is.na(df$value)]
    v = mean(goodvalues)
    n = df$variable[1]
    sd = sd(goodvalues)
    nas = sum(is.na(df$value))
    #recall foo is the function that does the pairdiffs -- we can do some work directly here with it if we wish
    diffmeas = mean(combn(goodvalues,2,foo))
    return(data.frame(name = n, value = v, sd = sd, nas = nas, diffmeas = diffmeas))
}
ddply(df.long, "variable", ff)


##############dplyr amazing
require(dplyr)

get.pairdiff <- function(v) {
    foo <- function(x) {
        x1 = max(x)
        x2 = min(x)
        min(x1 - x2, 24 + x2 - x1)
    }
    if (length(v) < 2) {
        return(NA)
    } else {
        mean(combn(v[!is.na(v)],2,foo))
    }
}

df.long <- melt(df, measure.vars = features, value.name = 'val', variable.name = 'var') #this is the long dataframe but with all of the auxiliary information attached. 
df.long %>%
    group_by(var) %>%
    select(val, antibodies) %>%
    summarise(
        no = length(val),
        val.m = mean(val, na.rm = T),
        val.sd = sd(val, na.rm = T),
        pd = get.pairdiff(val)
        )

test = df.long %>%
    group_by(var, measurement_method) %>%
    select(val) %>%
    do(data.frame(pd = get.pairdiff(.$val)))


