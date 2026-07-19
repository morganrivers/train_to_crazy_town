

############################################
### GENERAL MODELLING ASSUMPTIONS###########
############################################

implementation_discount <- rbeta_ci(0.05,0.45) 
years_credit <- rgamma_ci(5,20)
fish_grocery <- rbeta_ci(0.6,0.75)


######################################################
### STUNNING INTERVENTION ASSUMPTIONS ################
######################################################

## Pilot scenario
mshare_pilot_france <- rbeta_ci(0.001,0.01)
mshare_pilot_spain <- rbeta_ci(0.001,0.02)
mshare_pilot_italy <- rbeta_ci(0.001,0.01)
psuccess_pilot <- rbeta_ci(0.3,0.6)
cost_pilot <- 100E3*1.09 #100k EUR at 1.09 USD to a EUR
summarystats(mshare_pilot_france,mshare_pilot_spain,mshare_pilot_italy,psuccess_pilot)

## Scale scenario
mshare_scale_france <- rbeta_ci(0.01,0.24)
mshare_scale_spain <- rbeta_ci(0.04,0.14)
mshare_scale_italy <- rbeta_ci(0.03,0.1)
psuccess_scale <- rbeta_ci(0.15,0.35)
cost_scale <- 250E3*1.09 #100k EUR at 1.07 dollars to a euro
summarystats(mshare_scale_france,mshare_scale_spain,mshare_scale_italy,psuccess_scale)

## $/DALY range assumptions
duration_share <- rbeta_ci(0.5,0.9)
fish_welfarerange_impact_stun <- rbeta_ci(0.1,0.5)

######################################################
### NON-STUNNING INTERVENTION ASSUMPTIONS ############
######################################################

mshare_welfare_france <- rbeta_ci(0.001,0.24)
mshare_welfare_spain <- rbeta_ci(0.001,0.14)
mshare_welfare_italy <- rbeta_ci(0.001,0.1)
psuccess_welfare <- rbeta_ci(0.01,0.15)
cost_welfare <- 400E3*1.09 #100k EUR at 1.09 dollars to a euro

## $/DALY range assumptions
interventionlifesshare <- rbeta_ci(0.1,0.25)
fish_welfarerange_impact <- rbeta_ci(0.01,0.1)


#################################################################################
### LIST OF COUNTRIES AND SPECIES OVER WHICH TO PRODUCE CALCULATIONS ############
#################################################################################
country_list <- c("france","spain","italy")
species_list <- c("seabream","seabass","smalltrout")
bar_values <- c(50,1000,70000)

######################################################
### CONVERSION FACTOR ###############################
######################################################
hours_to_years <- (24*365.25)^-1

######################################################
### WELFARE RANGE APPROACH ASSUMPTIONS - BASELINE#####
######################################################

#Salmon moral weights
salmon_wr<- rbet(0.13,0.17)

# DALY as a share of human welfare range
DALY_share_of_welfare_range <- 0.5

######################################################
### WELFARE RANGE APPROACH ASSUMPTIONS - ALTTERNATIVE#
######################################################

#Salmon moral weights - double baseline
salmon_wr_alt <- salmon_wr*2

# DALY as a share of human welfare range
DALY_share_of_welfare_range_alt <- 0.1


