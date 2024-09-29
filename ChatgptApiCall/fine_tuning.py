import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("your_dataset.csv")
df.head()

def convert_to_gpt35_format(dataset):
    fine_tuning_data = []
    for _, row in dataset.iterrows():
        json_response = '{"Top Category": "' + row['Top Category'] + '", "Sub Category": "' + row['Sub Category'] + '"}'
        fine_tuning_data.append({
            "messages": [
                {"role": "user", "content": row['Support Query']},
                {"role": "system", "content": json_response}
            ]
        })



    # Stratified splitting. Assuming 'Top Category' can be used for stratification
    train_data, val_data = train_test_split(
        converted_data,
        test_size=0.2,
        stratify=dataset['Top Category'],
        random_state=42  # for reproducibility
    )
    return fine_tuning_data
