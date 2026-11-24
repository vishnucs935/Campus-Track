# Campus Track

A classroom project for reporting campus maintenance issues and tracking repairs. A student submits an issue and its location using Flutter. The React maintenance desk reads the same reports and marks completed repairs as resolved. Django owns the state and stores it in SQLite.

## Run the local demo

Install Python 3.10 or newer. Extract the ZIP, open a terminal in the directory containing manage.py, and run:

```sh
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\activate.bat` in Windows Command Prompt. Then run:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

Open the student form at http://127.0.0.1:8000/report/ and the maintenance desk at http://127.0.0.1:8000/ in two tabs. This local demonstration gives both tabs access to the same database without accounts.

## Two-minute demonstration

1. On the Flutter form, try submitting with a blank location. Check that the form asks for both fields.
2. Enter **Projector will not turn on** and **Engineering block, room 204**. Submit and note the report number.
3. In the React desk, select **Open** and press **Refresh**. Match the report number and location.
4. Click **Mark resolved**, then select **Resolved**. Reload the page and select **Resolved** again to show that Django saved the change.

## Design and tests

The issue record has an integer ID, title (1–120 characters), location (1–100 characters), and a resolved flag. New issues start open. Resolution is idempotent so repeating the action leaves the record resolved. Django validates submissions before writing them to SQLite.

| Action | Interface | Result |
|---|---|---|
| Submit report | POST /api/issues with JSON title and location | 201 and the saved record |
| Load desk | GET /api/issues | Records ordered newest first |
| Resolve report | POST /api/issues/{id}/resolve with JSON {} | 200 on success, 404 for a missing record |

The automated suite in tracker/tests.py exercises creation, trimming, listing, resolution, repeated resolution, invalid inputs and a missing record. The steps above form a manual acceptance test across both clients.

## Rebuild after editing

The main source files are mobile/lib/main.dart, tracker/models.py, tracker/urls.py and web/src/main.jsx. From the project directory:

- **React** — In web/, run `npm ci` and `npm run build` using Node 22.12 or newer. Copy the contents of web/dist/ into site/, preserving site/report/.
- **Flutter** — In mobile/, run `flutter pub get` and `flutter build web --no-web-resources-cdn --base-href /report/ --pwa-strategy none`. Copy the contents of mobile/build/web/ into site/report/.
- Restart Django, reload the pages and repeat the demonstration.

The Flutter client targets mobile browsers for this demo.
