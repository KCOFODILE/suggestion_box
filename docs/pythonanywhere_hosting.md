# Hosting Suggestion Box App on PythonAnywhere

This guide providing step-by-step instructions to host your Flask application on [PythonAnywhere](https://www.pythonanywhere.com/).

## 1. Prepare Your Code
Before uploading, ensure your local directory is clean. PythonAnywhere works best if you use Git, but you can also upload files directly.

### Recommended: Using Git (GitHub/Bitbucket)
1. Push your code to a private repository on GitHub.
2. In the PythonAnywhere **Dashboard**, open a **Bash Console**.
3. Clone your repository:
   ```bash
   git clone https://github.com/your-username/suggestion-box-app.git
   cd suggestion-box-app
   ```

---

## 2. Set Up a Virtual Environment
In the PythonAnywhere Bash Console (within your project folder):

1. Create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 my-venv
   ```
   *(Note: You can replace `3.10` with your preferred version, e.g., `3.9` or `3.11`)*

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Configure the Web App
1. Go to the **Web** tab in the PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Select **Manual Configuration** (Do NOT select Flask directly, as we use a custom structure).
4. Choose the Python version that matches your virtual environment (e.g., Python 3.10).
5. Once created:
   - **Source code:** Set to `/home/yourusername/suggestion-box-app`
   - **Working directory:** Set to `/home/yourusername/suggestion-box-app`
   - **Virtualenv:** Set to `/home/yourusername/.virtualenvs/my-venv`

---

## 4. Edit the WSGI Configuration
This is the most critical step. PythonAnywhere uses a WSGI file to interface with your app.

1. In the **Web** tab, under "Code", click the link to the **WSGI configuration file**.
2. Delete everything in that file and replace it with:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/suggestion-box-app'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables if needed
# os.environ['SECRET_KEY'] = 'your-secret-key-here'

from run import app as application
```

---

## 5. Initialize the Database
If you haven't uploaded your `suggestion_box.db` or want to start fresh:

1. In the Bash Console:
   ```bash
   export FLASK_APP=run.py
   flask init-db
   ```
2. (Optional) Create your first user:
   ```bash
   flask create-viewer yourusername yourpassword
   ```

---

## 6. Static Files (Optional but Recommended)
If your app has a `static` folder for CSS/JS:
1. In the **Web** tab, scroll down to **Static Files**.
2. Add a new entry:
   - **URL:** `/static/`
   - **Path:** `/home/yourusername/suggestion-box-app/app/static`

---

## 7. Reload and Visit
1. Go back to the top of the **Web** tab.
2. Click the green **Reload** button.
3. Your app should now be live at `yourusername.pythonanywhere.com`!

> [!TIP]
> **Debugging:** If you see a "500 Internal Server Error", check the **Error Log** link at the bottom of the Web tab. It usually points directly to the missing dependency or configuration error.
