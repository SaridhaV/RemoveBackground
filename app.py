from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

def remove_background(image):
    # Open the image
    img = Image.open(image)

    # Convert the image to RGBA mode
    img = img.convert("RGBA")

    # Get the pixel data
    data = img.getdata()

    # Get the background color (top-left corner)
    background_color = data[0]

    # Create a new list to store the modified pixel data
    newData = []

    # Iterate over the pixel data and check if it's similar to the background color
    for item in data:
        # Calculate the Euclidean distance between the pixel's RGB value and the background color
        distance = sum((a - b) ** 2 for a, b in zip(item[:3], background_color[:3])) ** 0.5
        # If the distance is below a threshold, consider it as part of the background
        if distance < 100:  # Adjust this threshold as needed
            newData.append((255, 255, 255, 0))  # Set alpha to 0 (transparent)
        else:
            newData.append(item)

    # Update the image with the modified pixel data
    img.putdata(newData)

    # Save the modified image
    output_image_path = "static/output_image.png"
    img.save(output_image_path, "PNG")

    return output_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['image']

    if file.filename == '':
        return render_template('index.html', message='No image selected')

    if file:
        output_image_path = remove_background(file)
        return render_template('result.html', image_path=output_image_path)

if __name__ == '__main__':
    app.run(debug=True)
