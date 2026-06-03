import fitz


def extract_pdf_text(path):

    text = ""

    pdf = fitz.open(path)

    for page in pdf:

        text += page.get_text()

    return text