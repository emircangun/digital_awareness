from flask import Flask
from flask_session import Session
from datetime import timedelta

from controller import main_controller
import config


def create_app():
    app = Flask(__name__)

    app.secret_key = '1773'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=3)
    
    app.add_url_rule("/", view_func=main_controller.main_page, methods=["GET", "POST"])
    app.add_url_rule("/questions/<int:url_id>", view_func=main_controller.question_page, methods=["GET", "POST"])
    app.add_url_rule("/pairwise-comparison", view_func=main_controller.pairwise_comp_page, methods=["GET", "POST"])
    app.add_url_rule("/report", view_func=main_controller.digital_report, methods=["GET", "POST"])
    
    Session(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=config.LOCALHOST_IP, port=config.PORT, debug=True)