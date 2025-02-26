# College Basketball Modeling

### Objective: Predict winner of NCAA college basketball games

This code repo will aid in the building of models to predict the outcome of NCAA college basketball games as part of a Kaggle Competition - [2025 competition link](https://www.kaggle.com/competitions/march-machine-learning-mania-2025/)


## Next steps

1. Create training data 
   * Include step to include games from both win and loss perspective
   * Only include tournament games
   * Features - created from regular season games aggregates
2. Train model
   * To predict for win/loss likelihood
   * To predict for point differential
     * Create function to translate point differential to likelihood
3. Evaluate model using Brier score
4. Build Women's model


### Modeling thoughts to explore
* Evaluate Brier score vs. logloss to better understand gambling strategies
* Extend training data set to use late-season games in model training?
* Feature development - custom PageRank feature
  * Data from previous years? Adj_off_ppp_prev_yr
  * Coaches
  * Conference level aggregations


### Repo organization
This repo will function as a working directory of code, notebooks, analyses, and notes for next steps and things.  
The data can be found from Kaggle and will not be included here so the notebooks won't run unless you download the data locally.  
Main development work will occur in Jupyter notebook cbb_modeling_2025.ipynb.  
