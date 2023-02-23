import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set the NewsAPI endpoint and query parameters
endpoint = 'https://newsapi.org/v2/everything'
params = {
    'apiKey': '788c747ed2444c88830930b1956b5b1e',
    'q': '',
    'pageSize': 10
}

# Define a function to get news articles for a given query
def get_news(query):
    # Update the query parameter
    params['q'] = query

    # Send a GET request to the NewsAPI endpoint with the query parameters
    response = requests.get(endpoint, params=params)

    # Parse the JSON response
    data = response.json()

    # Extract the articles from the response
    articles = data.get('articles', [])

    # Return the articles
    return articles

# Define a route for the home page
@app.route('/')
def home():
    return 'Welcome to the Blog Suggestion API!'

# Define a route for the blog suggestion endpoint
@app.route('/suggest_blogs', methods=['GET'])
def suggest_blogs():
    # Get the topic parameter from the request query string
    topic = request.args.get('topic')

    # Check if the topic parameter is present
    if topic is None:
        return jsonify({'error': 'Missing topic parameter'}), 400

    # Call the get_news function to retrieve news articles related to the topic
    articles = get_news(topic)

    # Extract the article titles and URLs
    suggestions = [{'title': article['title'], 'url': article['url'], 'image': article['urlToImage'], 'content': article['content']} for article in articles]

    # Return the suggestions as JSON
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run()
