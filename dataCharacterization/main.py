import pandas as pd
import json
from collections import Counter
import wordcloud
import seaborn as sns
from matplotlib import pyplot

with open('dataset/true_crime_grouped.json') as f:
    data = json.load(f)

## add channel name to each video
for channel in data:
    for video in data[channel]:
        video['channel'] = channel

## flatten the json to include only the video data
data = [video for channel in data for video in data[channel]]

## transfrom list to dict with numeric keys
data = {i: data[i] for i in range(len(data))}

## convert each json object in the list to a pandas dataframe
df = pd.DataFrame.from_dict(data, orient='index')


sns.set_theme(style="darkgrid",)

## count transcripts that are not empty
transcript_count = df['transcript'].apply(lambda x: len(x) > 0).sum()
views_count = df['Views'].apply(lambda x: len(x) > 0).sum()
print(f"Views count: {views_count}")
print(f"Transcript count: {transcript_count}")
print(f"Transcript percentage: {transcript_count/len(df) * 100}")
print(f"Total videos: {len(df)}")

## count views not empty

## transcripts analysis
all_transcripts = ' '.join(df['transcript'])
# cloud = wordcloud.WordCloud(width=800, height=400, background_color='white').generate(all_transcripts)
# cloud.to_file('graphics/wordcloud.png')

df['Views'] = df['Views'].apply(lambda x: x if x else '0')
df['Views_int'] = df['Views'].apply(lambda x: int(float(x)))

average_views = df.groupby('channel')['Views_int'].mean().sort_values(ascending=True)
average_views['Others'] = average_views[:-1].sum()
pyplot.figure(figsize=(38, 10))
# plot = sns.barplot(y=average_views.index[-2:], x=average_views[-2:])
plot = sns.barplot(y=average_views.index[:-2], x=average_views[:-2])
pyplot.setp(plot.get_yticklabels(), rotation=10, fontsize=18)
pyplot.setp(plot.get_xticklabels(), fontsize=16)
pyplot.xlabel('Average views', fontsize=18)
pyplot.ylabel('Channel', fontsize=18)
# plot.figure.savefig('graphics/average_views_jcs.png')
# plot.figure.savefig('graphics/average_views_others.png')

# plot the views distribution of the channel 'JCS - Criminal Psychology'
# sns.kdeplot(df[df['channel'] == 'JCS - Criminal Psychology']['Views_int'], log_scale=True).figure.savefig('graphics/views_distribution_jcs.png')

# print number of unique channels
print(f"Number of unique channels: {len(df['channel'].unique())}")

df['Likes'] = df['Likes'].apply(lambda x: x if x else '0')
df['Likes_int'] = df['Likes'].apply(lambda x: int(float(x)))
# sns.histplot(df['Likes_int'], log_scale=True).figure.savefig('graphics/likes_distribution.png')

df['Comments'] = df['Comments'].apply(lambda x: x if x else '0')
df['Comments_int'] = df['Comments'].apply(lambda x: int(float(x)))
# sns.histplot(df['Comments_int'], log_scale=True).figure.savefig('graphics/comments_distribution.png')

transcript_length = df[df['transcript'].apply(lambda x: len(x) > 0)]['transcript'].apply(lambda x: len(x))
print(transcript_length.describe())
# sns.kdeplot(transcript_length, log_scale=True).figure.savefig('graphics/transcript_length.png')

df["PublishedDate_datetime"] = pd.to_datetime(df["PublishedDate"])
df["PublishedDate_year"] = df["PublishedDate_datetime"].apply(lambda x: x.year)
# print count of distinct years
