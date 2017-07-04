

# State of Sports
# Compare the betting odds that each team will win the next championship across sports

# Author: Jeremy Mobley


library(rvest)
library(stringr)
library(ggplot2)
require(gridExtra)


# links
nba_site <- "http://www.vegasinsider.com/nba/odds/futures/"
nfl_site <- "http://www.vegasinsider.com/nfl/odds/futures/"
mlb_site <- "http://www.vegasinsider.com/mlb/odds/futures/"
nhl_site <- "http://www.vegasinsider.com/nhl/odds/futures/"
ncaabb_site <- "http://www.vegasinsider.com/college-basketball/odds/futures/"




# function to scrape odds data from web into dataframe
get_odds_data <- function(url, table_num=1){
  webpage <- read_html(url)
  tableguy <- html_nodes(webpage, xpath='//*[@class="table-wrapper cellTextNorm"]')
  return(data.frame(html_table(tableguy, fill=TRUE)[table_num]))
}


# function to convert odds column to probability
convert_odds_to_prob <- function(df) {
  splits <- data.frame(str_split_fixed(df$Odds, "/", 2))
  splits$X1 <- as.numeric(as.character(splits$X1))
  splits$X2 <- as.numeric(as.character(splits$X2))
  splits$prob <- splits$X2 / (splits$X1 + splits$X2)  
  df$prob <- splits$prob
  df[is.na(df$prob),"prob"] <- 0  # set any teams missing prob to 0
  #df$prob <- df$prob / sum(df$prob)  # calculate probability from odds
  return(df)
}

# function to plot team probabilities
plot_team_probs <- function(df) {
  return(ggplot(data=df, aes(x = reorder(df$Team, X = df$prob), y = prob)) +
           geom_bar(stat = "identity") + 
           geom_text(aes(label = Odds), hjust = -0.5, size = 3) + 
           labs(y = "Championship probability", x = "Team") + 
           coord_flip(ylim = c(0, 0.6)))
}


# wrapper function to scrape and plot one sport
scrape_n_plot <- function(website, table_num) {
  df <- get_odds_data(website, table_num)
  df <- convert_odds_to_prob(df)
  return(plot_team_probs(df))
}




# # plot all sports for comparison
nba_plot <- scrape_n_plot(nba_site,1)
mlb_plot <- scrape_n_plot(mlb_site,1)
nhl_plot <- scrape_n_plot(nhl_site,1)
nfl_plot <- scrape_n_plot(nfl_site,1)

plot_title <- paste0("Championship Probabilities by Sport for ", Sys.Date())
grid.arrange(nba_plot, mlb_plot, nhl_plot, nfl_plot, ncol=2, nrow=2,
             top = plot_title)
  
  







# Create process to grab data each day
sports_list <- c("nba", "nhl", "nfl", "mlb")

nba_data <- get_odds_data(nba_site)
nba_data$sport <- "nba"

nhl_data <- get_odds_data(nhl_site,1)
nhl_data$sport <- "nhl"

nfl_data <- get_odds_data(nfl_site)
nfl_data$sport <- "nfl"

mlb_data <- get_odds_data(mlb_site,1)
mlb_data$sport <- "mlb"


all_sports <- rbind(nba_data, nhl_data, mlb_data, nfl_data)

file_name <- paste0("sports_odds_",substr(Sys.time(),0,10),".csv")

setwd("C:/Users/Jeremy/Desktop/sports_odds")
write.csv(all_sports, file_name, row.names=FALSE)







########################################################################



