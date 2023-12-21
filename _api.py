from flask import Flask, request, jsonify
import keras
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
from io import BytesIO

app = Flask(__name__)

def chestScanPrediction(img_data, model_path):
    model = keras.models.load_model(model_path)
    
    # Loading Image
    img = Image.open(BytesIO(img_data))
    
    # Convert image to RGB format
    img = img.convert('RGB')
    
    # Resize Image to match the expected input shape
    target_size = (350, 350)
    img = img.resize(target_size, Image.BILINEAR)
    
    # Normalizing Image
    norm_img = image.img_to_array(img) / 255
    
    # Converting Image to Numpy Array
    input_arr_img = np.array([norm_img])
    
    # Getting Predictions
    pred = np.argmax(model.predict(input_arr_img))
    
    # Returning Model Prediction
    if pred == 0:
        return "The scan is adenocarcinoma"
    elif pred == 1:
        return "The scan is large.cell.carcinoma"
    elif pred == 2:
        return "The scan is normal"
    else:
        return "This scan is squamous.cell.carcinoma"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        uploaded_file = request.files['file']
        img_data = uploaded_file.read()
        result = chestScanPrediction(img_data, './ct_cnn_best_model.keras')
        return jsonify({"prediction": result})
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/')
def home():
    return "Welcome to the Lung Cancer Detection API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
