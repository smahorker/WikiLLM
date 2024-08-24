import pandas as pd
import re


def clean_text(text):
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s.]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def simple_sentence_tokenize(text):
    # Split on periods followed by a space and a capital letter
    return re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)


def preprocess_data(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Clean the text
    df['clean_content'] = df['content'].apply(clean_text)

    # Split content into sentences
    df['sentences'] = df['clean_content'].apply(simple_sentence_tokenize)

    # Flatten the sentences and create a new dataframe
    sentences_df = df.explode('sentences')

    # Remove any empty sentences
    sentences_df = sentences_df[sentences_df['sentences'].str.strip() != '']

    # Save the preprocessed data
    sentences_df[['title', 'sentences']].to_csv(output_file, index=False)


# Preprocess the data
preprocess_data('warframe_data.csv', 'preprocessed_warframe_data.csv')