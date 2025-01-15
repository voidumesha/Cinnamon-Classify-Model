const express = require('express');
const mysql = require('mysql');
const multer = require('multer');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const db = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root', 
    password: '', 
    database: 'cinnalyze' 
});

db.connect(err => {
    if (err) throw err;
    console.log('Connected to database');
});

const upload = multer({ storage: multer.memoryStorage() });

app.post('/upload', upload.single('image'), (req, res) => {
    const { user_id } = req.body;
    const image = req.file ? req.file.buffer : null;

    if (!user_id || !image) {
        console.log("Missing user_id or image in request");
        return res.status(400).send('User ID and image are required.');
    }

    console.log(`Received user_id: ${user_id}`);
    console.log(`Image size: ${image.length} bytes`);

    const query = `INSERT INTO barkimage (User_id, image, date_time_stamp) VALUES (?, ?, NOW())`;
    db.query(query, [user_id, image], (err, result) => {
        if (err) {
            console.error("Database error:", err);
            return res.status(500).send(err);
        }

        console.log(`Image successfully uploaded with barkId: ${result.insertId}`);
        res.send({ success: true, message: 'Image uploaded successfully!', barkId: result.insertId });
    });
});


app.get('/quality-records', (req, res) => {
    const query = `
        SELECT q.*, b.image 
        FROM quality q
        LEFT JOIN barkimage b ON q.barkId = b.barkId
        ORDER BY q.created_at DESC
    `;
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).send({
                success: false,
                message: 'Error fetching quality records.',
                error: err
            });
        }

        const mappedResults = results.map(record => {
            if (record.image) {
                record.image = record.image ? record.image.toString('base64') : null;
            }
            return record;
        });
        console.log(mappedResults);
        res.status(200).json(mappedResults); 
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});