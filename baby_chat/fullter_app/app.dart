import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Chatbot',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ChatBotPage(),
    );
  }
}

class ChatBotPage extends StatefulWidget {
  @override
  _ChatBotPageState createState() => _ChatBotPageState();
}

class _ChatBotPageState extends State<ChatBotPage> {
  TextEditingController _controller = TextEditingController();
  String _response = "";

  Future<void> _getPrediction(String message) async {
    final url = Uri.parse('http://127.0.0.1:5000/predict');
    final response = await http.post(url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'message': message}));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        _response = data['prediction'];
      });
    } else {
      setState(() {
        _response = 'Error: ${response.statusCode}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("ChatBot"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(hintText: "Enter your message"),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                String message = _controller.text;
                if (message.isNotEmpty) {
                  _getPrediction(message);
                }
              },
              child: Text("Send"),
            ),
            SizedBox(height: 20),
            Text("Response: $_response"),
          ],
        ),
      ),
    );
  }
}
