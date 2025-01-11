from flask import Flask, request, jsonify
import pymysql
import datetime
import numpy as np
from PIL import Image
import io
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.preprocessing import LabelBinarizer

app = Flask(__name__)

# MySQL Database Connection
db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='cinnalyze'
)

# Load Models
segmentation_model_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/unet_cinnamon_segmentation_v1.h5'
classification_model_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/final_classifier_model1.h5'
classes_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/classes4.npy'

segmentation_model = load_model(segmentation_model_path)
classification_model = load_model(classification_model_path)

# Load class labels
lb = LabelBinarizer()
class_labels = np.load(classes_path, allow_pickle=True)
lb.fit(class_labels)  # Fit LabelBinarizer with class labels
print(f"Loaded class labels: {class_labels}")

# Load ResNet50 feature extractor
feature_extractor = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Helper functions
def preprocess_for_segmentation(image):
    """Preprocess image for segmentation."""
    img = cv2.resize(image, (256, 256)) / 255.0  # Normalize to [0, 1]
    return np.expand_dims(img, axis=0)

def segment_image(image):
    """Perform image segmentation."""
    preprocessed_img = preprocess_for_segmentation(image)
    segmented_img = segmentation_model.predict(preprocessed_img)
    segmented_img = (segmented_img > 0.5).astype(np.uint8) * 255
    return cv2.cvtColor(np.squeeze(segmented_img), cv2.COLOR_GRAY2RGB)

def preprocess_for_classification(image):
    """Preprocess image for feature extraction and classification."""
    img = cv2.resize(image, (224, 224))  # Resize to 224x224
    img = preprocess_input(np.expand_dims(img, axis=0))  # Preprocess using ResNet preprocess
    return img

def classify_image(image):
    """Classify segmented image."""
    # Step 1: Extract features
    preprocessed_img = preprocess_for_classification(image)
    features = feature_extractor.predict(preprocessed_img)  # Shape: (1, 2048)

    # Step 2: Classify using the classification model
    predictions = classification_model.predict(features)  # Output shape: (1, num_classes)
    print(f"Predictions: {predictions}, Shape: {predictions.shape}")

    # Step 3: Decode class label
    try:
        predicted_class = lb.inverse_transform(predictions)[0]
    except Exception as e:
        print(f"LabelBinarizer inverse_transform failed: {str(e)}. Using fallback.")
        predicted_index = np.argmax(predictions, axis=1)[0]
        predicted_class = class_labels[predicted_index]  # Map index to class label

    return predicted_class

# Routes
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

        # Save image to MySQL database
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

        # Read and preprocess the uploaded image
        img = Image.open(io.BytesIO(file.read()))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Perform segmentation
        print("Performing segmentation...")
        segmented_img = segment_image(img)
        cv2.imwrite('segmented_output.jpg', segmented_img)  # Save segmented image for debugging
        print("Segmentation complete.")

        # Perform classification on the segmented image
        print("Performing classification...")
        quality_name = classify_image(segmented_img)
        print(f"Classification result: {quality_name}")

        # Prepare description
        description = f"The cinnamon quality is predicted to be '{quality_name}'."

        # Save analysis result to the database
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

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)