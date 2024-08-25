from os import environ
from string import Formatter

from dotenv import load_dotenv
from markdown_pdf import MarkdownPdf, Section

load_dotenv()  # take environment variables from .env.


def load_cv():
    phone = environ.get("PHONE")
    email = environ.get("EMAIL")

    with open('./cv/master_cv.md') as cv_file:
        cv = cv_file.read()

    return cv.format(phone=phone, email=email)


def markdown_to_pdf():
    cv = load_cv()
    pdf = MarkdownPdf()
    pdf.add_section(Section(cv))

    pdf.save('./build/master_cv.pdf')


if __name__ == '__main__':
    markdown_to_pdf()
