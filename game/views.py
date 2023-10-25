# game_recommendation_app/views.py
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def recommend_games(request):
    if request.method == 'POST':
        genres = request.POST.get('genres')
        import os

        # Get the current directory of the script
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Define the relative path to the model file
        relative_model_path = 'NoteBook/Windows_Games_List.csv'

        # Construct the absolute path to the model file
        model_file_path = os.path.join(current_directory, relative_model_path)

        # Replace backslashes with forward slashes in the path
        model_file_path = model_file_path.replace('\\', '/')
        # Load the dataset
        data = pd.read_csv(model_file_path)

        # Filter games based on the selected genre
        filtered_games = data[data['genres'].str.contains(genres, case=False, na=False)]

        if len(filtered_games) == 0:
            return render(request, 'index.html', {'message': "No games found based on your input."})
        else:
            # One-hot encode the entire 'genres' column for the entire dataset
            genres_encoded = data['genres'].str.get_dummies(sep=', ')

            # Create binary indicators for the selected genre using one-hot encoding
            filtered_genres_encoded = filtered_games['genres'].str.get_dummies(sep=', ')

            # Ensure both datasets have the same columns
            for column in genres_encoded.columns:
                if column not in filtered_genres_encoded.columns:
                    filtered_genres_encoded[column] = 0

            # Calculate similarity based on the input attributes
            input_attributes = filtered_genres_encoded.values
            data_attributes = genres_encoded.values
            similarity_scores = cosine_similarity(input_attributes, data_attributes)

            # Add similarity scores to the dataset
            data['similarity'] = similarity_scores[0]

            # Sort the dataset by similarity score in descending order
            recommended_games = data.sort_values(by='similarity', ascending=False)

            # Get the top 5 recommended games
            recommended_games = recommended_games['titles'].head(5).tolist()

            return render(request, 'recommendations.html', {'recommended_games': recommended_games})

    return render(request, 'index.html')

