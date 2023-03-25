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
        for page_num in range(len(self.reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(self.reader.pages[page_num])
            page_saving_name = self.pdf_path.stem + f"_{page_num}" + self.pdf_path.suffix
            with open(storing_location.joinpath(page_saving_name).as_posix(), "wb") as output:
                writer.write(output)
