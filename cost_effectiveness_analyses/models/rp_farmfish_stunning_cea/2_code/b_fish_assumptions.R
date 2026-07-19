

##################################################################
### CONSUMPTION IN METRIC TONNES BY COUNTRY ######################
#################################################################

seabream_italy_tons <-  39449
seabream_spain_tons <-  18743
seabream_france_tons <-  13320
seabass_italy_tons <-  31122
seabass_spain_tons <-  25290
seabass_france_tons <-  9640
smalltrout_italy_tons <-  19816
smalltrout_spain_tons <-  24389
smalltrout_france_tons <-  7940


############################################
### FISH WEIGHTS ###########################
############################################

weight_seabass <- rgamma_ci(0.4,0.5) # match fishcount range of 400 to 500g (90% CI) https://perma.cc/VB99-T48E 
weight_seabream <- rgamma_ci(0.3,0.4) # match fishcount range of 300 to 400g (90% CI) https://perma.cc/VB99-T48E
weight_smalltrout <-rgamma_ci(0.21,1.2) # match fishcount range of 210g to 1.2kg for small trout (not large trout) (90% CI) https://perma.cc/M3LC-VL8D


############################################
### SLAUGHTER DURATION######################
############################################

# Slaughter duration in minutes
slaughter_minutes_seabass <- rgamma_ci(5,40)
slaughter_minutes_seabream <- rgamma_ci(5,40)
slaughter_minutes_smalltrout <- rgamma_ci(2,10)

# Share stunned
seabream_stunned <- runi(0.15,0.30) 
seabass_stunned <- runi(0.1,0.25) 
smalltrout_stunned <- runi(0.2,0.5) 


############################################
### LIFE EXPECTANCY ########################
############################################

#Life expectancy in months (not accounting for pre-slaughter mortality)
lifexp_seabass <- rgamma_ci(14,24) # match fishcount.org https://perma.cc/VB99-T48E 
lifexp_seabream <- rgam(15.8,2.4) # match fishcount.org https://perma.cc/VB99-T48E.  Not set using rgam, as rgamma_ci search function does not work for these parameters.
lifexp_smalltrout <- rgamma_ci(12,15) # 3-6m pre grow-out https://perma.cc/T3NM-FKRL , 9m grow out https://perma.cc/XV5N-6B5R 

