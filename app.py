from flask import Flask, request, send_file, jsonify, url_for
from io import BytesIO
from tweet_image_generator import CreateTweet  
from openai import OpenAI  
import os
import uuid  # For unique filenames

app = Flask(__name__)

# Initialize openai client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/generate_tweet_image', methods=['POST'])
def generate_tweet_image():
    user_data = request.get_json()
    user_stance = user_data.get("stance", "Please generate a tweet that reflects my position on this issue.")

    # Construct the prompt
    prompt = f"{user_stance}. Please generate a tweet that reflects my position on this issue."

    # Generate text with OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    tweet_text = completion.choices[0].message.content.strip('"')

    # Generate tweet image
    image = CreateTweet(
        author_avatar="input/avatar/obama_avatar.jpeg",
        author_name="Mark Dem",
        author_tag="@_dem2022",
        text=tweet_text,
        reactions_retweet="100",
        reactions_like="20K",
        time="2022-07-05 14:34"
    )

    # Save image to a public directory
    filename = f"{uuid.uuid4()}.png"  # Generate unique filename
    public_path = os.path.join("static", filename)  # Save in 'static' directory
    image.save(public_path, "PNG")

    # Return the public URL of the image
    public_url = url_for("static", filename=filename, _external=True)
    return jsonify({"image_url": public_url})

if __name__ == '__main__':
    app.run(debug=True)
