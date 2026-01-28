# Hosting Suggestion Box App on PythonAnywhere

   git clone https://github.com/KCOFODILE/suggestion_box
   cd suggestion_box
   

1. Install `uv` on PythonAnywhere:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.cargo/env
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   cd ~/suggestion_box
   uv sync
   ```

---

## 3. Configure the Web App
1. Go to the **Web** tab in the PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Select **Manual Configuration**.
4. Choose **Python 3.11**.
5. Once created:
   - **Source code:** Set to `/home/Hicneud/suggestion_box`
   - **Working directory:** Set to `/home/Hicneud/suggestion_box`
   - **Virtualenv:** Set to `/home/Hicneud/suggestion_box/.venv`

---

## 4. Edit the WSGI Configuration
This is the most critical step. PythonAnywhere uses a WSGI file to interface with your app.

1. In the **Web** tab, under "Code", click the link to the **WSGI configuration file**.
2. Delete everything in that file and replace it with:

```python
import sys
import os

# Add your project directory to the sys.path
path = '/home/Hicneud/suggestion_box'
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
   uv run flask init-db
   ```
2. (Optional) Create your first user:
   ```bash
   uv run flask create-viewer yourusername yourpassword
   ```

---

## 6. Static Files (Optional but Recommended)
If your app has a `static` folder for CSS/JS:
1. In the **Web** tab, scroll down to **Static Files**.
2. Add a new entry:
   - **URL:** `/static/`
   - **Path:** `/home/Hicneud/suggestion_box/app/static`

---

## 7. Reload and Visit
1. Go back to the top of the **Web** tab.
2. Click the green **Reload** button.
3. Your app should now be live at `hicneud.pythonanywhere.com`!

> [!TIP]
> **Debugging:** If you see a "500 Internal Server Error", check the **Error Log** link at the bottom of the Web tab. It usually points directly to the missing dependency or configuration error.
