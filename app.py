from flask import Flask

from storage import engagement_artifacts

app = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, Document Assembly!"


def get_engagement_artifacts(engagement_id: str) -> dict:
    return engagement_artifacts(engagement_id, version=1)


if __name__ == "__main__":
    app.run(debug=True)
