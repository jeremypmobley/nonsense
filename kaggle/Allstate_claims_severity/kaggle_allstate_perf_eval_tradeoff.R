
# R script for Kaggle Allstate claims severity competition
# Author: Jeremy Mobley
# October 2016


library(randomForest)
library(Metrics)
library(ggplot2)



####################################
# load data
####################################
#setwd("C:/Users/Jeremy/Desktop/Kaggle/allstate2016")  # home
setwd("~/Desktop/kaggle/allstate_claims_severity")  # work

submit <- read.csv('sample_submission.csv')
raw_test <- read.csv('test.csv')
raw_train <- read.csv('train.csv')

####################################







####################################
# fix levels
####################################
train <- raw_train
train_ids <- train$id
train$id <- NULL
train$loss <- NULL

test <- raw_test
test$id <- NULL

train_test <- rbind(train, test)

for (f in names(train_test)) {
  if (class(train_test[[f]])=="character") {
    levels <- unique(train_test[[f]])
    train_test[[f]] <- as.integer(factor(train_test[[f]], levels=levels))
  }
}

train <- train_test[1:nrow(train),]
test <- train_test[(nrow(train)+1):nrow(train_test),]

# create train loss target variable
train_target <- raw_train$loss


####################################
# create feature_names variables
####################################

all_feature_names <- colnames(train)
remove_features <- c("loss", "id")

# create numeric features variable
num_features <- c()
for (feature in colnames(train)){
  if (is.numeric(train[,feature])){
    num_features <- c(num_features, feature)
  }
}

# create model_features variable
model_features_num <- num_features[!num_features %in% remove_features]

# model_features_all: all numeric features, all categorical features with same levels between train and test
model_features_all <- all_feature_names

# which features have values in test not in train?
#http://stats.stackexchange.com/questions/29446/random-forest-and-new-factor-levels-in-test-set
for(attr in all_feature_names)
{
  if (is.factor(train[[attr]]))
  {
    all.levels <- setdiff(levels(train[[attr]]), levels(test[[attr]]))
    if ( length(all.levels) != 0 ) {
      print(paste0(attr, ": ", length(levels(train[[attr]])), 
                   " train levels, ", length(levels(test[[attr]])), " in test"))
      model_features_all <- model_features_all[!model_features_all %in% attr]
      # update levels in test
      levels(test[[attr]]) <- union(levels(test[[attr]]), levels(train[[attr]]))
    }
  }
}

model_features_all <- model_features_all[!model_features_all %in% remove_features]

# remove features with too many levels
too_many_levels <- c("cat116", "cat113", "cat110", "cat109", "cat112")
model_features_all <- model_features_all[!model_features_all %in% too_many_levels]


# clean up working environment
rm(feature, remove_features, attr, all.levels, num_features, f, too_many_levels)
rm(train_test, raw_test, raw_train)



####################################
# Test effectiveness of k-fold with high k vs. performance of low k
# plot effectiveness vs. performance on dual axis across different levels of k

# performance - time it takes to train RF with X trees using Y features with k folds
# effectiveness - average MAE of train preds on RF with X trees using Y features with k folds

# 3 folds - train 3 models on 2/3 data, create preds for 1/3 data
# 5 folds - train 5 models on 4/5 data, create preds for 1/5
# 7 folds - train 7 models on 6/7 data
####################################







####################################
# Resampling appraoch

set.seed(123)

# Loop through resample_results df, create new sample, fit model on sample, calc mae
num_samples_list <- seq(from = 1000, to = 3000, by = 1000)
num_trees_list <- seq(from = 50, to = 150, by = 50)
resample_results <- expand.grid(num_samples=num_samples_list, num_trees=num_trees_list, time=0, mae=0)

for (rep in 1:nrow(resample_results)){
  start_time <- Sys.time()
  num_records <- resample_results$num_samples[rep]
  samp_idx <- sample(1:nrow(train), size = num_records)
  model <- randomForest(train[samp_idx, model_features_all], train_target[samp_idx], 
                        ntree = resample_results$num_trees[rep])
  train_preds <- predict(model, train[-samp_idx,])
  resample_results$mae[rep] <- mae(train_preds, train_target[-samp_idx])
  resample_results$time[rep] <- as.numeric(difftime(Sys.time(), start_time, units = "mins"))
  print(paste0("Loop ", rep, " complete"))
}
print(paste0("Total time ", 
             round(as.numeric(difftime(Sys.time(), start_time, units = "mins")),1), " minutes"))
cat("\n\nDONE\n\n\n\n")
system(command = "say R Code is DONE")


####################################
# Plot performance results

# Overlapping time and mae per samples trained chart
plot(resample_results$num_samples, resample_results$mae, type="l", col="blue")
par(new=TRUE)
plot(resample_results$num_samples, resample_results$time, type="l", col="red", axes=FALSE, xlab=NA, ylab=NA)
axis(side=4)
mtext(side=4, line = 2, 'text')

####################################

# ggplot2 plotting

resample_results$num_trees <- as.factor(resample_results$num_trees)

ggplot(data=resample_results,
       aes(x=num_samples, y=mae, colour=num_trees)) + geom_line() +
  xlab("Number of Samples") + ylab("MAE") + 
  ggtitle("Model evaluation performance by number of samples")

ggplot(data=resample_results,
       aes(x=num_samples, y=time, colour=num_trees)) + geom_line() +
  xlab("Number of Samples") + ylab("Time to train model (min)") + 
  ggtitle("Model training performance by number of samples")


####################################





# look at stability in resampling
# number of resamples plotted against standard deviation of mae


####################################
# Resampling with repeats

set.seed(123)
num_trees <- 100


num_samples_list <- seq(from = 3000, to = 3000, by = 2000)
num_repeats_list <- seq(from = 1, to = 3, by = 2)
resample_results <- expand.grid(num_samples=num_samples_list, 
                                num_repeats=num_repeats_list, 
                                time=0, avg_mae=0)

# Loop through resample_results df, (create new sample, fit model on sample, calc mae) * num_repeats
for (rep in 1:nrow(resample_results)){
  start_time <- Sys.time()
  num_records <- resample_results$num_samples[rep]
  repeat_results <- c()
  for (loop_repeat in 1:resample_results$num_repeats[rep]){
    samp_idx <- sample(1:nrow(train), size = num_records)
    model <- randomForest(train[samp_idx, model_features_all], train_target[samp_idx], ntree = num_trees)
    train_preds <- predict(model, train[-samp_idx,])
    repeat_results <- c(repeat_results,mae(train_preds, train_target[-samp_idx]))
  }
  resample_results$avg_mae[rep] <- mean(repeat_results)
  resample_results$time[rep] <- round(as.numeric(difftime(Sys.time(), start_time, units = "mins")),1)
  print(paste0("Loop ", rep, " complete"))
}
print(paste0("Total time ", 
             round(as.numeric(difftime(Sys.time(), start_time, units = "mins")),1), 
             " minutes"))
cat("\n\nDONE\n\n\n\n")
system(command = "say JEREMY")
system(command = "say Your Code is DONE")

# 5000 samples with model_features_all takes 3 minutes to train RF with 100 trees and all other defaults

####################################
















####################################

# kfold CV

# REVERSE kfold CV to start, for performance
# train on 1/5, test on 4/5
# no leakage but not nearly as robust as true kfold


# create fold index for CV
set.seed(123)
num_folds <- 5
sample_5fold_idx <- sample(seq(num_folds), size = nrow(train), replace=TRUE)


# create models for each fold, using specified feature set
start_time <- Sys.time()
fold_maes <- c()
num_trees <- 10
feature_set <- model_features3
for (fold in seq(num_folds)){
  # create model on fold
  model <- randomForest(train[sample_5fold_idx==fold, feature_set], 
                        train$loss[sample_5fold_idx==fold], 
                        ntree = num_trees)
  # create preds on hold-out fold
  preds <- predict(model, train[sample_5fold_idx!=fold,])
  # calc MAE on hold-out fold
  mae <- mae(preds, train$loss[sample_5fold_idx!=fold])
  #print(paste0("Fold ", fold, " MAE: ", mae))  # print out the MAE for each fold
  #print(Sys.time() - start_time)  # print out the time for each fold
  fold_maes <- c(fold_maes,mae)
}
print(Sys.time() - start_time)
mean(fold_maes)

#rm(fold, start_time, mae, model, preds)  # clean up environment










# Extending this timing analysis to local parallel processing

####################################

# set up parallel back-end
library(doParallel)
getDoParWorkers()
registerDoParallel(cores=detectCores())
getDoParWorkers()
######

sample_repeats <- 8
num_samples <- 10000
num_trees <- 100
start_time <- Sys.time()
newresults <- foreach(k = seq(sample_repeats), .combine=rbind, .packages = c("randomForest")) %dopar% {
  
  # create sample index
  set.seed(k)
  samp_idx <- sample(1:nrow(train), size = num_samples)
  
  # create model on sample  
  model <- randomForest(train[samp_idx, model_features_all], train_target[samp_idx], ntree = num_trees)
  
  # create preds on train hold-out
  train_preds <- predict(model, train[-samp_idx,])
  
  # return mae on hold-out
  #loop_mae <- data.frame(mae=mae(train_preds, train_target[-samp_idx]))
  #loop_mae
  
  # return hold_out preds with ids
  loop_hold_out_preds <- data.frame(id = train_ids[-samp_idx], pred = train_preds)
  loop_hold_out_preds
  
  # create, return test preds
  #test_preds <- data.frame(preds=predict(model, test), id=submit$id)
  #test_preds
}
stop_time <- Sys.time()
system(command = "say JEREMY, Your Code is DONE")
system(command = paste0("say Processing took ", 
                        round(as.numeric(difftime(stop_time, start_time, units = "mins")),1), " minutes"))


# for return mae from each thread
mean(newresults$mae)
hist(newresults$mae, breaks=nrow(newresults))

# for returning hold-out preds
avg_preds <- aggregate(x = newresults$pred, by = list(newresults$id), FUN=mean)
mae(avg_preds$x, train_target)

# for returning test_preds
avg_test_preds <- aggregate(x = newresults$preds, by = list(newresults$id), FUN=mean)
submit$loss <- avg_test_preds$x
setwd("~/Desktop/kaggle/allstate_claims_severity/submissions")  # work
write.csv(submit, '8bags100tree_rf_vars_submit.csv', quote=FALSE, row.names = FALSE)

####################################

# average of 8 repeats of 100 trees with 5k samples = 1278 on leaderboard
# using model_features_all - all but 5 variables




