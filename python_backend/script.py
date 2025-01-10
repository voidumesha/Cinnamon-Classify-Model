from flask import Flask, request, jsonify
import pymysql
import datetime
import numpy as np
from PIL import Image
import io
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet import preprocess_input
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
segmentation_model_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/Segmentation_Model.h5.ipynb'
classification_model_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/ResNet101_Updated_Implementation_02.h5.ipynb'
classes_path = r'C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/classes4.npy'

segmentation_model = load_model(segmentation_model_path)
classification_model = load_model(classification_model_path)

# Load class labels
lb = LabelBinarizer()
lb.classes_ = np.load(classes_path)

# Helper functions
def preprocess_for_segmentation(image):
    """Preprocess image for segmentation."""
    img = cv2.resize(image, (256, 256)) / 255.0
    return np.expand_dims(img, axis=0)

def segment_image(image):
    """Perform image segmentation."""
    preprocessed_img = preprocess_for_segmentation(image)
    segmented_img = segmentation_model.predict(preprocessed_img)
    segmented_img = (segmented_img > 0.5).astype(np.uint8) * 255
    return cv2.cvtColor(np.squeeze(segmented_img), cv2.COLOR_GRAY2RGB)

def preprocess_for_classification(image):
    """Preprocess image for classification."""
    img = cv2.resize(image, (224, 224))
    return preprocess_input(np.expand_dims(img, axis=0))

def classify_image(image):
    """Classify segmented image."""
    features = preprocess_for_classification(image)
    predictions = classification_model.predict(features)
    predicted_class = lb.inverse_transform(predictions)[0]
    return predicted_class

# Routes
@app.route('/', methods=['GET'])
def home():
    return "Cinnamon Analysis API is running!", 200

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Retrieve user_id and image from the request
        user_id = request.form.get('user_id')
        file = request.files.get('image')

        if not user_id or not file:
            return jsonify({"error": "User ID and image are required."}), 400

        # Read image data
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
        segmented_img = segment_image(img)

        # Perform classification on the segmented image
        quality_name = classify_image(segmented_img)
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

        # Convert image BLOB to base64 for JSON response
        for record in results:
            if record['image']:
                record['image'] = record['image'].hex()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
