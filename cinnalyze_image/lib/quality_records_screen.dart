import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'quality_details_screen.dart';

class QualityRecordsScreen extends StatelessWidget {
  Future<List<Map<String, dynamic>>> fetchQualityRecords() async {
    final response = await http
        .get(Uri.parse('http://192.168.137.197:3001/quality-records'));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body);
      return data.map((record) => Map<String, dynamic>.from(record)).toList();
    } else {
      throw Exception('Failed to load quality records');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Quality Records'),
        backgroundColor: Color(0xFF8B5E3C),
      ),
      body: Container(
        color: Color(0xFFFDF3E7),
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: fetchQualityRecords(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(
                child: Text(
                  'Error: ${snapshot.error}',
                  style: TextStyle(
                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              );
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return Center(
                child: Text(
                  'No records found.',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.black54,
                  ),
                ),
              );
            } else {
              return ListView.builder(
                padding: EdgeInsets.all(16.0),
                itemCount: snapshot.data!.length,
                itemBuilder: (context, index) {
                  final record = snapshot.data![index];
                  return GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              QualityDetailsScreen(record: record),
                        ),
                      );
                    },
                    child: Card(
                      elevation: 4,
                      margin: EdgeInsets.only(bottom: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
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
                              style: TextStyle(
                                  fontSize: 14, color: Colors.black87),
                            ),
                            SizedBox(height: 8),
                            Text(
                              'Description: ${record['Description']}',
                              style: TextStyle(
                                  fontSize: 14, color: Colors.black87),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              );
            }
          },
        ),
      ),
    );
  }
}
