# Installation

## Prerequisites

- Python 3.12+
- Node.js (for frontend dependencies)
- Django 5.x

## Steps

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd delta
    ```

2. **Install Python dependencies**

    ```sh
    pip install -e .[dev]
    ```

3. **Install Node.js dependencies**

    ```sh
    npm install
    ```

4. **Copy static assets**

    ```sh
    python copy_node_to_static.py
    ```

5. **Apply migrations**

    ```sh
    python manage.py migrate
    ```

6. **Create a `.env` file**

    ```
    SECRET_KEY=your-secret-key
    ```

7. **Run the development server**

    ```sh
    python manage.py runserver
    ```

8. **Access the app**

    Open [http://localhost:8000](http://localhost:8000) in your browser.


