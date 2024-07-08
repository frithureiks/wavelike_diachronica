library('distributional')
library('ggdist')
library('bayesplot')
library('ggplot2')
library('ndjson')

df_u = ndjson::stream_in('toymod_uniform.json')#uniform model
df_n = ndjson::stream_in('toymod.json')#Normal model
df_a = ndjson::stream_in('toymod_informative.json')#informative model


subdf_u = df_u[df_u$Accuracy <= quantile(df_u$Accuracy, 0.005)]
subdf_n = df_n[df_n$Accuracy <= quantile(df_n$Accuracy, 0.005)]
subdf_a = df_a[df_a$Accuracy <= quantile(df_a$Accuracy, 0.005)]

acc_df = data.frame('Loss' = subdf_u$Accuracy, 'Model' = 'uniform')
acc_df = rbind(acc_df, data.frame('Loss' = subdf_n$Accuracy, 'Model' = 'normal'))
acc_df = rbind(acc_df, data.frame('Loss' = subdf_a$Accuracy, 'Model' = 'informative'))



pdf(file = 'accuracy_comp.pdf', height = 4, width = 6)


ggplot(acc_df, aes(x=Loss, y=Model)) + stat_halfeye(slab_fill = NA, slab_color = "black", slab_linewidth = 0.5, point_interval = 'mean_qi', .width = c(.8), 
                                                    interval_color = 'blue', interval_alpha = 0.7, shape = 21, point_fill="white", stroke = 1.2) + 
  theme_classic() + scale_x_continuous(limits = c(0,400))

dev.off()

bigranges = data.frame()
ranges = seq(from = 0.8, to = 0.99, length.out = 10)
for(i in 1:length(ranges)){
  subdf_u_tmp = df_u[df_u$Accuracy <= quantile(df_u$Accuracy, 1-ranges[i])]
  bigranges = rbind(bigranges,data.frame('Loss' = mean(subdf_u_tmp$Accuracy), 'sd' = sd(subdf_u_tmp$Accuracy), 'Model' = 'uniform', 'Range' = ranges[i]))
}

for(i in 1:length(ranges)){
  subdf_n_tmp = df_n[df_n$Accuracy <= quantile(df_n$Accuracy, 1-ranges[i])]
  bigranges = rbind(bigranges,data.frame('Loss' = mean(subdf_n_tmp$Accuracy), 'sd' = sd(subdf_n_tmp$Accuracy), 'Model' = 'normal', 'Range' = ranges[i]))
}

for(i in 1:length(ranges)){
  subdf_a_tmp = df_a[df_a$Accuracy <= quantile(df_a$Accuracy, 1-ranges[i])]
  bigranges = rbind(bigranges,data.frame('Loss' = mean(subdf_a_tmp$Accuracy), 'sd' = sd(subdf_a_tmp$Accuracy), 'Model' = 'informative', 'Range' = ranges[i]))
}


g = ggplot(bigranges, aes(x=Range, y=Loss, group=Model, color=Model)) + 
  geom_line(size=0.5, position = position_dodge(width = 0.01))+
  geom_pointrange(aes(ymin=Loss-sd, ymax=Loss+sd), position = position_dodge(width = 0.01)) + theme_minimal() + xlab('Percentile')

pdf(file = 'accuracy_dev.pdf', height = 6, width = 8)
g
dev.off()

pdf(file = 'spreadparams.pdf', height = 8, width = 6)
par(mfrow=c(3,2))
hist(subdf_u$Params.spread, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Uniform', xlab = "Spread", 
     border=F, probability = T, breaks = 50)
interv = HDInterval::hdi(subdf_u$Params.spread, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_u$Params.spread), 0, lwd = 3, pch = 16)
curve(dunif(x, 0,1), add = T, type = 'l', lwd = 2, lty = 2)


hist(subdf_u$Params.riv, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Uniform', xlab = "Obstacle spread", 
     border=F, probability = T, breaks = 50)
interv = HDInterval::hdi(subdf_u$Params.riv, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_u$Params.riv), 0, lwd = 3, pch = 16)
curve(dunif(x, 0,1), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_n$Params.spread, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Normal', xlab = "Spread", 
     border=F, probability = T, breaks = 50)
interv = HDInterval::hdi(subdf_n$Params.spread, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_n$Params.spread), 0, lwd = 3, pch = 16)
curve(dtruncnorm(x, a = 0, b = 1, 0.25,0.3), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_n$Params.riv, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Normal', xlab = "Obstacle spread", 
     border=F, probability = T, breaks = 50)
interv = HDInterval::hdi(subdf_n$Params.riv, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_n$Params.riv), 0, lwd = 3, pch = 16)
curve(dtruncnorm(x, a = 0, b = 1, 0.1,0.2), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_a$Params.spread, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Informative', xlab = "Spread", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_a$Params.spread, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_a$Params.spread), 0, lwd = 3, pch = 16)
curve(dbeta(x, 5,20), add = T, type = 'l', lwd = 2, lty = 2)


hist(subdf_a$Params.riv, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Informative', xlab = "Obstacle spread", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_a$Params.riv, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_a$Params.riv), 0, lwd = 3, pch = 16)
curve(dbeta(x, 2,20), add = T, type = 'l', lwd = 2, lty = 2)

dev.off()


library(truncnorm)
pdf(file = 'innovparams.pdf', height = 8, width = 6)
par(mfrow=c(3,2))
hist(subdf_u$Params.feat0, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Uniform', xlab = "Innovation 1", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_u$Params.feat0, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_u$Params.feat0), 0, lwd = 3, pch = 16)
curve(dunif(x, 0,1), add = T, type = 'l', lwd = 2, lty = 2)


hist(subdf_u$Params.feat1, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Uniform', xlab = "Innovation 2", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_u$Params.feat1, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_u$Params.feat1), 0, lwd = 3, pch = 16)
curve(dunif(x, 0,1), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_n$Params.feat0, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Normal', xlab = "Innovation 1", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_n$Params.feat0, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_n$Params.feat0), 0, lwd = 3, pch = 16)
curve(dtruncnorm(x, a = 0, b = 1, 0.25,0.3), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_n$Params.feat1, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Normal', xlab = "Innovation 2", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_n$Params.feat1, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_n$Params.feat1), 0, lwd = 3, pch = 16)
curve(dtruncnorm(x, a = 0, b = 1, 0.75,0.3), add = T, type = 'l', lwd = 2, lty = 2)

hist(subdf_a$Params.feat0, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Informative', xlab = "Innovation 1", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_a$Params.feat0, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_a$Params.feat0), 0, lwd = 3, pch = 16)
curve(dbeta(x, 2,5), add = T, type = 'l', lwd = 2, lty = 2)


hist(subdf_a$Params.feat1, xlim = c(0,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = 'Informative', xlab = "Innovation 2", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_a$Params.feat1, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_a$Params.feat1), 0, lwd = 3, pch = 16)
curve(dbeta(x, 5,2), add = T, type = 'l', lwd = 2, lty = 2)

dev.off()


pdf(file = 'contrasts.pdf', height = 6, width = 10)
par(mfrow=c(1,2))
hist(subdf_n$Params.feat1-subdf_n$Params.feat0, xlim = c(-1,1), lwd = 0.1, col = rgb(0,0,1,1/4), main = '', xlab = "Innovation 2 - innovation 1", 
     border=F, probability = T, breaks = 20)
interv = HDInterval::hdi(subdf_n$Params.feat1-subdf_n$Params.feat0, credMass = 0.89)
lines(c(interv[1], interv[2]), c(0,0), lwd = 3)
points(median(subdf_n$Params.feat1-subdf_n$Params.feat0), 0, lwd = 3, pch = 16)

plot(subdf_n$Params.feat0, subdf_n$Params.spread,xlim = c(0,1), ylim = c(0,1) , col = rgb(0,0,1,1/4), pch = 16, xlab = 'Innovation 1', ylab = 'Spread')

dev.off()

curve(abs(dnorm(x,  0.75,0.3)-dnorm(x, 0.25,0.3)), add = F, type = 'l', lwd = 2, lty = 2)

plot(density(rtruncnorm(100000, a = 0, b = 1, 0.75,0.3)-rtruncnorm(100000, a = 0, b = 1, 0.25,0.3)), add =T)


##repros

subdf = df_n[df_n$Accuracy <= quantile(df_n$Accuracy, 0.005)]
subdf
write.csv(subdf, 'reproruns.csv')



