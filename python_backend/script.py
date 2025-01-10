from flask import Flask, request, jsonify
import pymysql
import datetime
import numpy as np
from PIL import Image
import io
import tensorflow as tf

app = Flask(__name__)

#MySQL Database Connection
db = pymysql.connect(
    host='127.0.0.1',  # Use 'localhost' or '127.0.0.1'
    user='root',       # MySQL username
    password='',       # MySQL password (leave blank if none)
    database='cinnalyze'  # Your database name
)

#Load TensorFlow Model (If available)
model = tf.keras.models.load_model("/C:/CINNAMON/Cinnamon App/Cinnamon App/python_backend/Segmentation_Model.h5")
# model = tf.keras.models.load_model("your_model_path.h5")

#Route to Confirm Server is Running
@app.route('/', methods=['GET'])
def home():
    return "Cinnamon Analysis API is running!", 200

#Upload Route to Save Image to Database
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

#Analyze Route to Process the Uploaded Image
@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        file = request.files.get('image')
        bark_id = request.form.get('bark_id')

        if not file or not bark_id:
            return jsonify({"error": "Bark ID and image are required."}), 400

        # Process the image for prediction (Mock process here)
        img = Image.open(io.BytesIO(file.read()))
        img = img.resize((224, 224))  # Resize as needed for model
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Mock prediction logic (replace with your model)
        # predictions = model.predict(img_array)
        # quality_name = "high" if predictions[0][0] > 0.5 else "low"
        quality_name = "high"  # Example output
        description = "It is high-quality cinnamon."

        # Save analysis result to the 'quality' table
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

#  Route to Fetch Quality Records
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

# Run the Flask Server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
