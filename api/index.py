from app import app

if __name__ == '__main__':
    """
    Main entry point to run the Flask application.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
