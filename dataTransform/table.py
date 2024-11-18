import pandas as pd
import json
from collections import Counter

# Extended list of stop words (including common auxiliary verbs, pronouns, determiners, and other common words)
stop_words = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
    'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn',
    'wasn', 'weren', 'won', 'wouldn', 'like', 'know', 'really', 'think', "it's", "i'm", "don't", 'going', 'get', 'time',
    'people', "that's", 'could', 'said', 'go', 'right', 'back', 'also', 'see', "didn't", 'got', 'two', 'even', 'want', 'found',
    'kind', 'little', 'well', 'actually', 'something', 'yeah', 'say', 'way', 'lot', "you're", 'gonna', 'okay', 'first',
    'went', 'look', 'much', 'day', 'make', 'would', 'one', 'never', 'there\'s', 'still', 'things', 'maybe', 'many', 'next',
    'old', 'happened', '[music]', 'always', 'bit', 'away', 'point', 'around', 'home', 'good', 'um', 'oh', '-', 'yeah', 'uh',
    'hmm'
])


def main():
    # Load the JSON data
    with open('../dataset/true_crime_grouped.json', 'r') as file:
        data = json.load(file)

    # Extract all transcripts from the JSON structure
    all_transcripts = []
    for channel, videos in data.items():
        for video in videos:
            if 'transcript' in video:
                all_transcripts.append(video['transcript'])

    # Combine all transcripts into a single string
    all_text = ' '.join(all_transcripts)

    # Split the text into words and count frequencies, excluding stop words
    word_counts = Counter(word.lower() for word in all_text.split() if word.lower() not in stop_words)

    # Get the 50 most common words
    most_common_words = word_counts.most_common(50)

    # Convert to a DataFrame for easier handling
    word_table = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

    # Save the table to a CSV file for further use
    word_table.to_csv('most_used_words_filtered.csv', index=False)

    # Print the table
    print(word_table)

if __name__ == "__main__":
    main()
