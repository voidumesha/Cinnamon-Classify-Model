import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class QualityDetailsScreen extends StatelessWidget {
  final Map<String, dynamic> record;

  const QualityDetailsScreen({super.key, required this.record});

  @override
  Widget build(BuildContext context) {
    // Decode the Base64 image
    Uint8List? imageBytes =
        record['image'] != null ? base64Decode(record['image']) : null;

    return Scaffold(
      appBar: AppBar(
        title: Text('Quality Details'),
        backgroundColor: Color(0xFF8B5E3C),
      ),
      body: Container(
        color: Color(0xFFFDF3E7),
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: imageBytes != null
                  ? Image.memory(
                      imageBytes,
                      height: 200,
                      width: 200,
                      fit: BoxFit.cover,
                    )
                  : Icon(
                      Icons.image_not_supported,
                      size: 200,
                      color: Colors.grey,
                    ),
            ),
            SizedBox(height: 16),
            Text(
              'Quality ID: ${record['Quality_id']}',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.brown,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Quality Name: ${record['Quality_Name']}',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 8),
            Text(
              'Description: ${record['Description']}',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 8),
            Text(
              'Bark ID: ${record['barkId']}',
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 8),
            Text(
              'Created At: ${record['created_at']}',
              style: TextStyle(fontSize: 14, color: Colors.black54),
            ),
          ],
        ),
      ),
    );
  }
}
