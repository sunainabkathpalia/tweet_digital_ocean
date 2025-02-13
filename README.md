# AI-Generated Tweet Image API

## Overview
This tool is a Flask-based web service that generates Twitter-style images using OpenAI API model and PIL.

The tool:
- Accepts a policy stance from a user.
- Uses OpenAI to generate a tweet-style response.
- Renders the response into a twitter image.
- Returns either:
  - A direct image (for GET requests, viewable in a browser).
  - A Base64-encoded JSON response (for POST requests).

This app is deployed on DigitalOcean and can be integrated with Qualtrics surveys.

## API Endpoint
**Base URL:**  
```
https://coral-app-qwqn5.ondigitalocean.app/generate_tweet_image
```

| Method  | Request Type                      | Description                                        |
|---------|-----------------------------------|----------------------------------------------------|
| **GET**  | URL Params (`?stance=xyz`)       | Returns a direct image  |
| **POST** | JSON Payload (`{"stance": "xyz"}`) | Returns a JSON response with a Base64-encoded image. |

## Features
- Dynamic tweet generation using OpenAI.
- Twitter-style image rendering with PIL.
- Supports both `GET` and `POST` requests.
  - `GET` returns an image directly.
  - `POST` returns JSON with a Base64 image.

## Project Structure
```
├── app.py                       # Main Flask application
├── tweet_image_generator.py      # Helper function for generating Twitter-style images
└── requirements.txt              # Required dependencies
```

## API Usage

### Example 1: Using GET (Returns an Image) - in browser
**Request:**  
```
https://coral-app-qwqn5.ondigitalocean.app/generate_tweet_image?stance=I support climate action
```

### Example 2: Using POST (Returns JSON with Base64)

**Python Code to Test the API:**
```python
import requests
import base64
from PIL import Image
from io import BytesIO

url = "https://coral-app-qwqn5.ondigitalocean.app/generate_tweet_image"
payload = {"stance": "I support universal healthcare."}

response = requests.post(url, json=payload)
if response.status_code == 200:
    data = response.json()
    
    # Decode Base64 image
    image_data = base64.b64decode(data["image_base64"])
    image = Image.open(BytesIO(image_data))
    image.show()
else:
    print(f"Error: {response.status_code}")
```

## Using with Qualtrics

### 1. Configure a Web Service Block
- **Method:** `POST`
- **API URL:**  
  ```
  https://coral-app-qwqn5.ondigitalocean.app/generate_tweet_image
  ```
- **Body Parameters:**  
  - **Key:** `stance`
  - **Value:** `${e://Field/stance}`

- **Custom Header:**  
  - **Key:** `Content-Type`
  - **Value:** `application/json`

### 2. Store Response in Embedded Data
Map the API response fields to embedded data fields:
- `image_base64` → `image_base64`
- `image_type` → `image_type`

