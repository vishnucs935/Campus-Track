import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MaterialApp(
      title: 'Campus reports',
      theme: ThemeData(colorSchemeSeed: const Color(0xff195549)),
      home: const ReportPage(),
    ));

class ReportPage extends StatefulWidget {
  const ReportPage({super.key});
  @override
  State<ReportPage> createState() => _ReportPageState();
}

class _ReportPageState extends State<ReportPage> {
  final title = TextEditingController();
  final location = TextEditingController();
  bool sending = false;
  String message = '';

  @override
  void dispose() {
    title.dispose();
    location.dispose();
    super.dispose();
  }

  Future<void> submit() async {
    if (title.text.trim().isEmpty || location.text.trim().isEmpty) {
      setState(() => message = 'Enter both the issue and its location.');
      return;
    }
    setState(() {
      sending = true;
      message = '';
    });
    try {
      final response = await http
          .post(
            Uri.base.resolve('/api/issues'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(
                {'title': title.text.trim(), 'location': location.text.trim()}),
          )
          .timeout(const Duration(seconds: 15));
      if (!mounted) return;
      final data = jsonDecode(response.body);
      if (response.statusCode == 201) {
        title.clear();
        location.clear();
        setState(() => message = "Report #${data['id']} submitted.");
      } else {
        setState(() => message = data['error'] ?? 'Submission failed.');
      }
    } catch (_) {
      if (mounted)
        setState(() => message =
            'Could not confirm submission. Check the desk before retrying.');
    } finally {
      if (mounted) setState(() => sending = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Campus services')),
        body: Center(
            child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 520),
          child: ListView(padding: const EdgeInsets.all(24), children: [
            Text('Report an issue',
                style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 24),
            TextField(
                controller: title,
                enabled: !sending,
                maxLength: 120,
                decoration: const InputDecoration(
                    labelText: 'What needs fixing?',
                    hintText: 'Projector will not turn on')),
            TextField(
                controller: location,
                enabled: !sending,
                maxLength: 100,
                decoration:
                    const InputDecoration(labelText: 'Building and room')),
            FilledButton(
                onPressed: sending ? null : submit,
                child: Text(sending ? 'Submitting…' : 'Submit report')),
            const SizedBox(height: 16),
            Semantics(liveRegion: true, child: Text(message)),
          ]),
        )),
      );
}
