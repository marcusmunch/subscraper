library(tidyverse)
library(scales)

limits = c(10, 15, 25, 35)

if (!file.exists("output/png")){
  cat('Created graphics output folder')
  dir.create("output/png")
}

for (sub in gsub(".txt$", "", list.files("output", ".txt"))){
  cat(paste0("Analyzing subreddit /r/", sub))
  contents <- read_tsv(sprintf("output/%s.txt", sub))
  nrows <- nrow(contents)
  
  for (limit in limits){

contents %>%
  group_by(author) %>%
  filter(author != "[deleted]") %>%
  summarise(totalscore = sum(score), n = n(), avgscore = mean(score)) %>%
  arrange(desc(totalscore)) %>%
  head(limit) %>%

ggplot(aes(x=reorder(author, -totalscore), y = totalscore, fill=totalscore)) +
  geom_bar(stat="identity") +
  scale_fill_gradientn(colors = c("darkred", "yellow", "darkblue")) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0.5)) +
  labs(x = "Name",
       y = "Total upvotes",
       title = sprintf("The %s most upvoted posters in /r/%s (n = %s)", limit, sub, nrows))

ggsave(sprintf("output/png/%s_author_top%s.png", sub, limit), height = 5, width = 8)

contents %>%
  group_by(title) %>%
  filter(n() > 2) %>%
  summarise(totalscore = sum(score), n = n(), avgscore = mean(score)) %>%
  arrange(desc(totalscore)) %>%
  head(limit) %>%

ggplot(aes(x=reorder(title, -totalscore), y = totalscore, fill=totalscore)) +
  geom_bar(stat="identity") +
  scale_fill_gradientn(colors = c("darkred", "yellow", "darkblue")) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0.5)) +
  labs(x = "Name",
       y = "Total upvotes",
       title = sprintf("The %s most upvoted titles in /r/%s (n = %s)", limit, sub, nrows))

ggsave(sprintf("output/png/%s_title_top%s.png", sub, limit), height = 5, width = 8)

  }
}
