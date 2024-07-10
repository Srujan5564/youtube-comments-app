# app.py

from flask import Flask, request, jsonify, render_template
from fetch import get_comments
import random

# Import your sentiment analysis model here
from model import predict_sentiment
# from your_model import predict_sentiment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.json['video_url']
    max_comments = min(int(request.json.get('max_comments', 100)), 1000)  # Default to 100, max 1000
    
    comments = get_comments(video_url,max_comments)
    if comments is None:
        return jsonify({'error': 'Failed to fetch comments'}), 500

    # Perform sentiment analysis on comments
    # Replace this with your actual sentiment analysis logic
    positive = neutral = negative = 0
    analyzed_comments = []
    for comment in comments:
        sentiment = predict_sentiment(comment)  # Placeholder, replace with your model's prediction
        if sentiment == 'LABEL_2':
            actual_sentiment = "Positive"
            positive += 1
        elif sentiment == 'LABEL_1':
            actual_sentiment = "Neutral"
            neutral += 1
        else:
            actual_sentiment = "Negative"
            negative += 1

        analyzed_comments.append({
                'text': comment[:100] + '...' if len(comment) > 100 else comment,  # Truncate long comments
                'sentiment': actual_sentiment
            })

    # print(positive,negative,neutral)

    total_comments = positive + neutral + negative
    if total_comments == 0:
        return jsonify({'error': 'No comments to analyze'}), 400

    return jsonify({
        'positive': positive / total_comments * 100,
        'neutral': neutral / total_comments * 100,
        'negative': negative / total_comments * 100,
        'total_comments' :  total_comments,
        'comments': analyzed_comments[:20]
    })

if __name__ == '__main__':
    app.run(debug=True)