



# Time until I get to go home today function
min_til_work_done <- function(){
  difftime(as.POSIXlt(paste0(Sys.Date()," 17:00:00 CDT")), 
           Sys.time(), units = "mins")
}


say_time_til_work_done <- function() {
  timeguy <- as.numeric(min_til_work_done())
  if (timeguy < 0) {
    system(command = "say work time is over")
    exit
  }
  say_is_are <- ifelse(floor(timeguy/60) > 1, "are", "is")
  hour_plural <- ifelse(floor(timeguy/60) > 1, "hours", "hour")
  ifelse(timeguy > 60, 
         system(command = paste0("say JEREMY, there ", say_is_are, " ", floor(timeguy/60), hour_plural, " and ", 
                                 round(timeguy %% 60), " minutes until 5pm")),
         system(command = paste0("say JEREMY, there are ", round(timeguy), " minutes until 5pm"))
  )
}

say_time_til_work_done()

