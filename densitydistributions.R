setwd('LOCATIONOF .CSV FILE')


library("readxl")
library(ggplot2)
library(reshape2)
library(plyr)
library(qvalue)
library(svglite)
library(tidyr)


ld = read.csv("output_antilongevity.csv", header = TRUE)
ld
ld$pval <- pchisq(ld$LR, df = 1, lower.tail = FALSE)
ld$padj <- p.adjust(ld$pval, method = 'fdr')
print("# of genes with omega higher in Heliconius")
ld
nrow(subset(ld,fg_omega  > bg_omega))


#Sort Results by LRT
sorted_ld = ld[order(-ld$LR),]
sorted_ld

#Convert dataframe into long format
wide_ld = subset(sorted_ld, select = c(ï..genename,bg_omega,fg_omega,LR,pval,padj))
head(wide_ld)
long_ld = gather(wide_ld, level, omega, bg_omega, fg_omega)


#remove "omega" form bg and fg
long_ld$level <- replace(long_ld$level, long_ld$level=='bg_omega', 'Background')    #FIRST SET OF BRANCHES NAME
long_ld$level <- replace(long_ld$level, long_ld$level=='fg_omega', 'Heliconius')    #SECOND SET OF BRANCHE NAME
long_ld

#bin the omegas
c = 3
long_ld$omega_bin <- long_ld$omega
long_ld$omega_bin[long_ld$omega_bin>c] <- c
long_ld

#Graph the results.
mu <- ddply(subset(long_ld), "level", summarise, grp.mean=mean(omega_bin))
mu

avg_bg = mu[1,2]
favg_bg = format(round(avg_bg,2), nsmall=2)

avg_fg = mu[2,2]
favg_fg = format(round(avg_fg,2), nsmall=2)


#ADJUST CHART TITLE AS NECESSARY
myplot = ggplot(subset(long_ld), aes(x=omega_bin, fill = level, color=level)) +
  ggtitle("Density Distribution of ?? Estimates for Anti-Longevity Genes in Heliconius and Background Species") +
  geom_density(alpha = 0.6) +
  xlab('dN/dS') + 
  ylab('Density') +
  geom_vline(data=mu, aes(xintercept=grp.mean, color=level),
             linetype="dashed") +
  geom_text(aes(x = .1, label = paste0("?? = ",favg_bg), y=10), colour = "red") +
  geom_text(aes(x = .18, label = paste0("?? = ",favg_fg), y=10), colour = "blue") +
  scale_color_manual(values=c(Background="red", Heliconius="darkblue")) +
  scale_fill_manual(values=c(Background="red", Heliconius="darkblue")) +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), panel.background = element_blank(), axis.line =   element_line(colour = "black"))

myplot 


#Perform stats - Kolgomorov-Smirnoff test (D=0.10349, P = 4.515e-06).
bg_omega = subset(long_ld, level == "Background")$omega_bin
fg_omega = subset(long_ld, level == "Heliconius")$omega_bin
ks.test(fg_omega, bg_omega)
