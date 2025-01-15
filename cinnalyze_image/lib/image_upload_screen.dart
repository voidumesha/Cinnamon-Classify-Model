import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';
import 'package:image_picker/image_picker.dart';

class ImageUploadScreen extends StatefulWidget {
  @override
  _ImageUploadScreenState createState() => _ImageUploadScreenState();
}

class _ImageUploadScreenState extends State<ImageUploadScreen> {
  int? _barkId;
  File? _image;
  final _picker = ImagePicker();

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _uploadImage() async {
    if (_image == null) {
      _showMessage('Image is not selected');
      return;
    }

    final request = http.MultipartRequest(
      'POST',
      Uri.parse(
          'http://192.168.137.197:3001/upload'), // Ensure this URL matches the backend
    );
    request.fields['user_id'] = '7'; // Example user ID
    request.files.add(await http.MultipartFile.fromPath('image', _image!.path));

    try {
      final response = await request.send();
      final responseData = await response.stream.bytesToString();

      print('Response status: ${response.statusCode}');
      print('Response body: $responseData');

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(responseData);
        _barkId = jsonResponse['barkId']; // Store barkId
        print('Bark ID: $_barkId');
        _navigateToAnalysisScreen();
      } else {
        _showMessage('Image upload failed! Please try again.');
      }
    } catch (e) {
      print('Upload error: $e');
      _showMessage('An error occurred while uploading the image.');
    }
  }

  void _navigateToAnalysisScreen() {
    if (_image != null && _barkId != null) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) =>
              AnalysisScreen(image: _image!, barkId: _barkId!),
        ),
      );
    }
  }

  void _showMessage(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Upload Status'),
          content: Text(message),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('OK'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload Image'),
        backgroundColor: Color(0xFF8B5E3C),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _image != null
                ? Image.file(_image!, height: 300)
                : Image.asset(
                    'assets/images/cinnamon6.png',
                    height: 300,
                  ),
            SizedBox(height: 20),
            Text(
              'Select an option',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.brown,
              ),
            ),
            SizedBox(height: 20),
            Padding(
                padding: const EdgeInsets.symmetric(
                    horizontal: 16.0, vertical: 24.0),
                child: Column(
                  children: [
                    // Button for picking image from gallery
                    ElevatedButton.icon(
                      onPressed: () => _pickImage(ImageSource.gallery),
                      icon: Icon(Icons.photo_library, color: Color(0xFF8B5E3C)),
                      label: Text(
                        'Select an image from device storage',
                        style: TextStyle(color: Color(0xFF8B5E3C)),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        elevation: 2,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    // Button for capturing image using camera
                    ElevatedButton.icon(
                      onPressed: () => _pickImage(ImageSource.camera),
                      icon: Icon(Icons.camera_alt, color: Color(0xFF8B5E3C)),
                      label: Text(
                        'Capture an image from camera',
                        style: TextStyle(color: Color(0xFF8B5E3C)),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        elevation: 2,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    // Upload button
                    ElevatedButton(
                      onPressed: _uploadImage,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF8B5E3C),
                        foregroundColor: Color(0xffffffff),
                      ),
                      child: Text('Upload Image'),
                    ),
                    SizedBox(height: 10),
                    // Next button
                  ],
                ))
          ],
        ),
      ),
      backgroundColor: Color(0xFFFDF3E7),
    );
  }
}

class AnalysisScreen extends StatefulWidget {
  final File image;
  final int barkId;

  const AnalysisScreen(
      {super.key, required this.image, required, required this.barkId});

  @override
  _AnalysisScreenState createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  String? quality;
  String? description;
  String? barkId;
  String? date;
  bool isLoading = false;

  Future<void> _analyzeImage() async {
    final uri =
        Uri.parse('http://192.168.137.197:3001/analyze'); // Flask server URL

    setState(() {
      isLoading = true; // Show loading indicator
    });

    try {
      final request = http.MultipartRequest('POST', uri);
      request.fields['bark_id'] = widget.barkId.toString();
      request.files.add(
        await http.MultipartFile.fromPath('image', widget.image.path),
      );

      final response = await request.send();
      if (response.statusCode == 200) {
        final responseData = await response.stream.bytesToString();
        final result = jsonDecode(responseData);

        setState(() {
          // Update state with API results
          quality = result['Quality'];
          description = result['Description'];
          barkId = result['Bark Id'];
          date = result['Date'];
        });
      } else {
        final responseData = await response.stream.bytesToString();
        final result = jsonDecode(responseData);
        throw Exception(result);
      }
    } catch (e) {
      setState(() {
        quality = null;
        description = null;
        barkId = null;
        date = null;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      setState(() {
        isLoading = false; // Hide loading indicator
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Analyze Image'),
        backgroundColor: Color(0xFF8B5E3C),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.file(widget.image, height: 300),
              SizedBox(height: 20),
              isLoading
                  ? CircularProgressIndicator()
                  : Column(
                      children: [
                        // Display results if available
                        if (quality != null &&
                            description != null &&
                            barkId != null)
                          Column(
                            children: [
                              Text(
                                'Analysis Results',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.brown,
                                ),
                              ),
                              SizedBox(height: 10),
                              Text('Bark ID: $barkId'),
                              Text('Quality: $quality'),
                              Text('Description: $description'),
                              Text('Date: $date'),
                              SizedBox(height: 20),
                            ],
                          )
                        else if (!isLoading)
                          Text(
                            'No results yet. Please analyze the image.',
                            style: TextStyle(color: Colors.grey),
                          ),
                      ],
                    ),
              SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.symmetric(
                    horizontal: 16.0, vertical: 24.0),
                child: Column(
                  children: [
                    // Analyze button
                    ElevatedButton(
                      onPressed: _analyzeImage,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF8B5E3C),
                        foregroundColor: Colors.white,
                        elevation: 2,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: Text('Analyze Image'),
                    ),
                    SizedBox(height: 20),
                    // Go to Main Menu button
                    ElevatedButton(
                      onPressed: () {
                        Navigator.popUntil(context, (route) => route.isFirst);
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF8B5E3C),
                        foregroundColor: Colors.white,
                        elevation: 2,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: Text('Go to Main Menu'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      backgroundColor: Color(0xFFFDF3E7),
    );
  }
}
