from flask import Flask, request, jsonify, send_file
from io import BytesIO
import base64
from tweet_image_generator import CreateTweet
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize openai client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/generate_tweet_image', methods=['GET', 'POST'])
def generate_tweet_image():
    if request.method == 'GET':
        user_stance = request.args.get("stance", "Please generate a tweet that reflects my position on this issue.")
    else:
        user_data = request.get_json()
        user_stance = user_data.get("stance", "Please generate a tweet that reflects my position on this issue.")

    # Construct the prompt with the specified logic
    prompt = f"{user_stance}. Please generate a tweet that reflects my position on this issue."

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    tweet_text = completion.choices[0].message.content.strip('"')

    # Generate tweet image
    image = CreateTweet(
        author_avatar="input/avatar/profile_dp.jpeg",
        author_name="Mark Dem",
        author_tag="@_dem2022",
        text=tweet_text,
        reactions_retweet="100",
        reactions_like="20K",
        time="2022-07-05 14:34"
    )

    # Convert image to BytesIO
    img_io = BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)

    # If it's a GET request, return the image directly
    if request.method == 'GET':
        return send_file(img_io, mimetype='image/png')

    # For POST, return JSON 
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return jsonify({
        'success': True,
        'tweet_text': tweet_text,
        'image_base64': img_base64,
        'image_type': 'image/png'
    })


if __name__ == '__main__':
    app.run(debug=True)