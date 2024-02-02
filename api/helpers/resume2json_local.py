# Textract comes with bunch of other dependencies. Make sure they are installed.
# https://textract.readthedocs.io/en/stable/installation.html
import textract
from txt2json import txt2json


def extract_text_from_pdf(file):
    try:
        return textract.process(file)
    except Exception as e:
        print("Error processing file: ", str(e))


text = str(extract_text_from_pdf("../static/resume.pdf"))
json = txt2json(text, "grammar/schemas/candidate.json")
print(json)
