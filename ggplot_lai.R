library(ggplot2)
library(dplyr)

library(ggthemes)


setwd('C:/Users/luizv/OneDrive_Purdue/OneDrive - purdue.edu/CIMMYT-Purdue RS&CropModelling/Data workflow/R_lai_graphs')


dataFrame <- read.csv('LAI_ACRE_Biomass_y22.csv')

str(dataFrame)

colnames(dataFrame)

dataFrame$Days_after_planting <- as.factor(dataFrame$Days_after_planting)

bp <- ggplot(dataFrame, aes(x = Days_after_planting, y = LAI, color = environment)) +
  geom_boxplot()

bp + scale_color_grey() + labs(title = 'Soybean Public Biomass 2022', y = 'Leaf Area Index', x = 'Days After Planting', colour = 'Date of Planting')


### Early source

dataFrame_early <- filter(dataFrame, environment %in% 'Early')
dataFrame_early


bp_e_s <- ggplot(dataFrame_early, aes(x = Days_after_planting, y = LAI)) +
  geom_boxplot(aes(fill = source))

bp_e_s + labs(title = 'Soybean Public Biomass 2022 Early Date of Planting', y = 'Leaf Area Index', x = 'Days After Planting', fill = 'Source')


# Lines
sources <- unique(dataFrame_early$source)

for (name in sources) {
  
  print(name)
  
  plotPlot <- paste('LAI_ACRE_Biomass_y22_Early_source_', name, '.png', sep='')
  
  dataFrame_early_source <- filter(dataFrame_early, source %in% name)
  
  title_ <- paste('Soybean Public Biomass 2022 Early Date of Planting, Source ', name, sep = '')
  
  bp_e_s <- ggplot(dataFrame_early_source, aes(x = Days_after_planting, y = LAI)) +
    geom_boxplot(aes(fill = line))
  
  bp_e_s <- bp_e_s + labs(title = title_ , y = 'Leaf Area Index', x = 'Days After Planting', fill = 'Line')
  
  ggsave(plotPlot, width = 8.333333333333334, height = 5.427083333333333)
  
}



### Late source

dataFrame_late <- filter(dataFrame, environment %in% 'Late')
dataFrame_late

title <- paste('Soybean Public Biomass 2022 ','Late Date of Planting', sep = '')

bp_e_s <- ggplot(dataFrame_late, aes(x = Days_after_planting, y = LAI)) +
  geom_boxplot(aes(fill = source))

bp_e_s + labs(title = title , y = 'Leaf Area Index', x = 'Days After Planting', fill = 'Source')

# Lines
sources <- unique(dataFrame_late$source)

for (name in sources) {

  print(name)
  
  plotPlot <- paste('LAI_ACRE_Biomass_y22_Late_source_', name, '.png', sep='')
  
  dataFrame_late_source <- filter(dataFrame_late, source %in% name)
  
  title_ <- paste('Soybean Public Biomass 2022 Late Date of Planting, Source ', name, sep = '')
  
  bp_e_s <- ggplot(dataFrame_late_source, aes(x = Days_after_planting, y = LAI)) +
    geom_boxplot(aes(fill = line))
  
  bp_e_s <- bp_e_s + labs(title = title_ , y = 'Leaf Area Index', x = 'Days After Planting', fill = 'Line')
  
  ggsave(plotPlot, width = 8.333333333333334, height = 5.427083333333333)
  
}
