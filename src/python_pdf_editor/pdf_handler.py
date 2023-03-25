from pathlib import Path

import PyPDF2


class PDFHandler:
    def __init__(self, pdf_path: str) -> None:
        self.reader = PyPDF2.PdfReader(pdf_path)
        self.pdf_path = Path(pdf_path)

    @property
    def num_pages(self) -> int:
        return len(self.reader.pages)

    def split_pages(self, storing_location: Path) -> None:
        if not storing_location.exists():
            storing_location.mkdir(parents=True)

        for page_num in range(len(self.reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(self.reader.pages[page_num])
            page_saving_name = f"page_{str(page_num).zfill(4)}_" + self.pdf_path.name
            with open(storing_location.joinpath(page_saving_name).as_posix(), "wb") as output:
                writer.write(output)

    def protect_with_password(self, password: str) -> None:
        writer = PyPDF2.PdfWriter()
        writer.append_pages_from_reader(self.reader)
        writer.encrypt(password)
        with open(
            self.pdf_path.parent.joinpath(self.pdf_path.stem + "_protected" + self.pdf_path.suffix), "wb"
        ) as output:
            writer.write(output)


if __name__ == "__main__":
    pdf_handler = PDFHandler("data/test.pdf")
    pdf_handler.split_pages(Path("data/split"))
    pdf_handler.protect_with_password("test")
