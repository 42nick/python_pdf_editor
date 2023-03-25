from python_pdf_editor.pdf_handler import PDFHandler


def test_split_pages(tmp_path):
    pdf_handler = PDFHandler("data/test.pdf")
    pdf_handler.split_pages(tmp_path)

    assert len(list(tmp_path.iterdir())) == len(pdf_handler.reader.pages)
