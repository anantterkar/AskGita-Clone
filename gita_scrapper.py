import json
import pandas as pd
import datetime

with open('verse.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)
    
with open('translation.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

df_trans = pd.DataFrame(translations)
df_verses = pd.DataFrame(verses)

# Here I am filtering translations of Swami Gambirananda as it is in English
# We can later test out for other english authors as well.
df_sg = df_trans[df_trans['authorName'] == 'Swami Gambirananda']

df_merged = pd.merge(
    df_sg,
    df_verses,
    left_on='verse_id',
    right_on='id',
    how='inner'
)

df_result = df_merged[['description', 'text', 'verse_id']]
df_result.to_csv('gita_verses_translations.csv', index=False)

today = datetime.date.today()
verse_index = today.toordinal() % len(df_result)
verse_of_theday = df_result.iloc[verse_index]

# create a JSON file for your frontend to use
with open('verse_of_the_day.json', 'w', encoding='utf-8') as f:
    json.dump({
        'text': verse_of_theday['text'],
        'translation': verse_of_theday['description'],
        'verse_id': int(verse_of_theday['verse_id'])
    }, f, ensure_ascii=False, indent=2)

