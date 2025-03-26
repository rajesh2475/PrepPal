"""
Created by: Rajesh M
Date: June 21, 2024
Description: Entry point for running the Flask application with SocketIO support.
"""

from app import create_app, socketio
from config import Config

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)