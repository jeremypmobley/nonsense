
# R script for Kaggle Allstate claims severity competition
# Author: Jeremy Mobley
# October 2016


library(randomForest)
library(Metrics)


####################################
# load data
####################################
#setwd("C:/Users/Jeremy/Desktop/Kaggle/allstate2016")  # home
setwd("~/Desktop/kaggle/allstate_claims_severity")  # work

submit <- read.csv('sample_submission.csv')
test <- read.csv('test.csv')
train <- read.csv('train.csv')

####################################





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

# clean up working environment
rm(feature, remove_features, attr, all.levels, num_features, model_features)







####################################
# Create single RF model on small subset of train, apply to test

# subset training data set to randomly selected records
set.seed(123)
num_records <- 1000
samp_idx <- sample(1:nrow(train), size = num_records)

# train RF model, subset by sample
num_trees <- 100
model <- randomForest(train[samp_idx, model_features_num], train$loss[samp_idx], ntree = num_trees)

# create preds
test_preds <- predict(model, test)
train_preds <- predict(model, train)

# calc MAE model evaluation metric
mae(train_preds, train$loss)

# look at variable importance
varImpPlot(model)
#model$importance

# create submission file
# update submit df with preds
#submit$loss <- test_preds
# write out result file
#setwd("~/Desktop/kaggle/allstate_claims_severity/submissions")  # work
#write.csv(submit, '100tree_rf_only_numeric_submit.csv', quote=FALSE, row.names = FALSE)
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
  mae <- calc_mae(preds, train$loss[sample_5fold_idx!=fold])
  #print(paste0("Fold ", fold, " MAE: ", mae))  # print out the MAE for each fold
  #print(Sys.time() - start_time)  # print out the time for each fold
  fold_maes <- c(fold_maes,mae)
}
print(Sys.time() - start_time)
mean(fold_maes)

#rm(fold, start_time, mae, model, preds)  # clean up environment






####################################

# set up parallel back-end
library(doParallel)
getDoParWorkers()
registerDoParallel(cores=detectCores())
getDoParWorkers()


# create models for each parameter set in parallel
num_folds <- 5
newresults <- foreach(k = seq(num_folds), .combine=rbind) %dopar% {
  # create model on fold
  model <- randomForest(train[sample_5fold_idx!=k, feature_set], 
                        train$loss[sample_5fold_idx!=k], 
                        ntree = num_trees)
  # create preds on hold-out fold
  preds <- predict(model, train[sample_5fold_idx==k,])
  loop_pred_df <- data.frame(id=train[sample_5fold_idx==k,"id"], pred=preds)
  loop_pred_df
}

newresults <- newresults[order(newresults$id),]
calc_mae(newresults$pred, train$loss)

####################################










######################################################
# performance test
# how much time to train a RF model on model_features4
# for one fold of 5-fold CV

# DID NOT FINISH - DO NOT RUN

feature_set <- model_features4
k <- 1
num_trees <- 10
start_time <- Sys.time()
model <- randomForest(train[sample_5fold_idx!=k, feature_set], 
                      train$loss[sample_5fold_idx!=k], 
                      ntree = num_trees)
preds <- predict(model, train[sample_5fold_idx==k,])
print(Sys.time() - start_time)
######################################################


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
# Project Schedule
####################################

# 10/24-10/30 First coding week
# Main tasks:
# Get good set of base features to use in modeling
# Tune Random Forest submission
# Create xgboost submission
# Create CV framework
# Finish project plan
# Meet with Jen/Sarah for tips on how to create project plans
# Goal: 1140 on public leaderboard
# 10/31-11/6 Halloween week
# Main tasks:
# Feature Engineering
#t-SNE algorithm
#https://github.com/oreillymedia/t-SNE-tutorial
#https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding
# Create caret version
# Goal: 1130 on public leaderboard
# 11/7-11/13
# Main tasks:
# Feature Engineering
# Goal: 1120 on public leaderboard
# 11/14-11/20
# Main tasks:
# Continue model iterations
# Goal: 1115 on public leaderboard
# 11/21-11/27: Thanksgiving Week
# Main tasks:
# Continue model iterations
# Goal: 1110 on public leaderboard
# 11/28-12/4: 2 weeks to go
# Main tasks:
# Stack models
# Goal: 1105 on public leaderboard
# 12/5-12/11: Last week
# Main tasks:
# Create final ensemble submission
# Goal: 1100 on public leaderboard
# ENDS: Monday 12/12 midnight UTC time, 7pm CST

####################################




