from flask import Flask, request, jsonify
import pymysql
import datetime
import numpy as np
import cv2
from PIL import Image
import io
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.preprocessing import LabelBinarizer
import tensorflow as tf
import os

app = Flask(__name__)

# ==========================
# Database Connection
# ==========================
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='cinnalyze',
    autocommit=True
)

# ==========================
# Custom Dice Loss Function
# ==========================
def dice_loss(y_true, y_pred, smooth=1.0):
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    return 1 - (2.0 * intersection + smooth) / (union + smooth)

# ==========================
# Load Models
# ==========================
segmentation_model_path = r'C:/CINNAMON/Cinnamon App/cinnamon_quality/models/best_segmentation_model.h5'
classification_model_path = r'C:/CINNAMON/Cinnamon App/cinnamon_quality/models/final_classification_model.h5'

try:
    segmentation_model = load_model(segmentation_model_path, custom_objects={'dice_loss': dice_loss})
    print("Segmentation model loaded successfully!")
except Exception as e:
    print(f"Error loading segmentation model: {e}")

try:
    classification_model = load_model(classification_model_path)
    print("Classification model loaded successfully!")
except Exception as e:
    print(f"Error loading classification model: {e}")

# ==========================
# Load Class Labels
# ==========================
IMG_SIZE = 224
BATCH_SIZE = 32

datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
train_flow = datagen.flow_from_directory(
    'C:/CINNAMON/Cinnamon App/cinnamon_quality/dataset/images',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

class_labels = {v: k for k, v in train_flow.class_indices.items()}
print(f"Class labels: {class_labels}")

# ==========================
# Helper Functions
# ==========================
def preprocess_for_segmentation(image):
    img = cv2.resize(image, (224, 224)) / 255.0
    return np.expand_dims(img, axis=0)

def segment_image(image):
    preprocessed_img = preprocess_for_segmentation(image)
    segmented_img = segmentation_model.predict(preprocessed_img)
    segmented_img = (segmented_img > 0.5).astype(np.uint8) * 255
    return cv2.cvtColor(np.squeeze(segmented_img), cv2.COLOR_GRAY2RGB)

def preprocess_for_classification(image):
    img_resized = cv2.resize(image, (224, 224)) / 255.0
    img = np.expand_dims(img_resized, axis=0)
    return img

def classify_image(image):
    preprocessed_img = preprocess_for_classification(image)
    predictions = classification_model.predict(preprocessed_img)
    predicted_index = np.argmax(predictions, axis=1)[0]
    predicted_class = class_labels[predicted_index]
    return predicted_class

# ==========================
# Flask Routes
# ==========================

@app.route('/', methods=['GET'])
def home():
    return "Cinnamon Analysis API is running!", 200

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        user_id = request.form.get('user_id')
        file = request.files.get('image')

        if not user_id or not file:
            return jsonify({"error": "User ID and image are required."}), 400

        image_data = file.read()

        cursor = db.cursor()
        sql = "INSERT INTO barkimage (User_id, image, date_time_stamp) VALUES (%s, %s, NOW())"
        cursor.execute(sql, (user_id, image_data))
        db.commit()

        return jsonify({
            "success": True,
            "message": "Image uploaded successfully!",
            "barkId": cursor.lastrowid
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        file = request.files.get('image')
        bark_id = request.form.get('bark_id')

        if not file or not bark_id:
            return jsonify({"error": "Bark ID and image are required."}), 400

        img = Image.open(io.BytesIO(file.read()))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Perform segmentation
        print("Performing segmentation...")
        segmented_img = segment_image(img)
        print("Segmentation complete.")

        # Perform classification
        print("Performing classification...")
        quality_name = classify_image(segmented_img)
        print(f"Classification result: {quality_name}")

        # Save analysis result to the database
        description = f"The cinnamon quality is predicted to be '{quality_name}'."
        cursor = db.cursor()
        sql = "INSERT INTO quality (Quality_Name, Description, barkId, created_at) VALUES (%s, %s, %s, NOW())"
        cursor.execute(sql, (quality_name, description, bark_id))
        db.commit()

        return jsonify({
            "Bark Id": bark_id,
            "Quality": quality_name,
            "Description": description,
            "Date": datetime.datetime.now()
        }), 200

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/quality-records', methods=['GET'])
def get_quality_records():
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT q.*, b.image 
        FROM quality q
        LEFT JOIN barkimage b ON q.barkId = b.barkId
        ORDER BY q.created_at DESC
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        for record in results:
            if record['image']:
                record['image'] = record['image'].hex()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ==========================
# Run the Flask Server
# ==========================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
