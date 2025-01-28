# How to Run This Flask Application

Follow these steps to run the Flask application:

1. **Clone the repository:**
  ```bash
  git clone https://github.com/Techcabz/mces_inventory.git
  cd [project name]
  ```

2. **Create a virtual environment:**
  ```bash
  python3 -m venv .venv
  ```

3. **Activate the virtual environment:**
  - On Windows:
    ```bash
    .venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

4. **Install the dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

5. **Set the Flask application environment variable:**
  - On Windows:
    ```bash
    set FLASK_APP=run.py
    set FLASK_ENV=development
    ```
  - On macOS/Linux:
    ```bash
    export FLASK_APP=run.py
    ```

6. **Run the database migrations:**
  ```bash
  flask db init        # Initialize the migrations folder (only once)
  flask db migrate -m "Initial migration"
  flask db upgrade
  ```

7. **Run the Flask application:**
  ```bash
  flask run
  ```

8. **Open your web browser and navigate to:**
  ```
  http://127.0.0.1:5000
  ```

You should now see your Flask application running.
