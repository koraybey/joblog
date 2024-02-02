from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS
from gql_mutations import create_vacancy_mutation
from helpers.txt2json import txt2json

app = Flask(__name__)
CORS(app)


@app.route("/html2text", methods=["POST"])
def convert():
    data = request.get_json()

    if "html" not in data:
        return {"error": "No HTML content provided."}, 400

    soup = BeautifulSoup(data["html"], "html.parser")

    for s in soup.select("form"):
        s.extract()

    text = soup.get_text()
    print(text)
    json = txt2json(text, "grammar/schemas/vacancy.json")
    print(json)

    result = create_vacancy_mutation(json)
    return {"success": result}, 200


if __name__ == "__main__":
    app.run(debug=True)
