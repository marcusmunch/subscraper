library(tidyverse)
library(scales)

subs = c("models", "goddesses", "prettygirls", "catsstandingup")
limits = c(10, 25, 35, 50)

for (sub in subs){
  
for (limit in limits){
count_list <- read_tsv(sprintf("output/%s_sorted.txt", sub)) %>%
  arrange(desc(counts))

ggplot(head(count_list, limit), aes(x = reorder(name, -counts), y=counts, fill=counts)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label=counts), vjust=-0.25, size = 2.5) +
  theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0.5)) +
  scale_fill_gradientn(limits = c(count_list$counts[1], count_list$counts[limit]),
                       colors = c("darkred", "yellow", "darkgreen")) +
  labs(x= "Name",
       y = "Appearances",
       title=paste(sprintf("The %s most popular titles in /r/%s (n = %s posts)", limit, sub, sum(count_list$counts, na.rm = T))),
       caption="Made by /u/MarcusMunch")

ggsave(sprintf("output/png/%s_top%s.png", sub, limit))
}}