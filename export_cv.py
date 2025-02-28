import os
from pathlib import Path
from typing import Optional

from loguru import logger
from markdown_pdf import MarkdownPdf, Section

from app_logging import logging


@logging()
def load_cv(md_file: Path, phone: Optional[str], email: Optional[str]) -> str:
    assert phone is not None, "Phone number is required"
    assert email is not None, "Email is required"

    with md_file.open() as cv_file:
        cv = cv_file.read()

    return cv.format(phone=phone, email=email)


@logging()
def markdown_to_pdf(md_file: Path, pdf_file: Path, phone: Optional[str], email: Optional[str]) -> None:
    assert md_file.suffix == '.md', f"Expected markdown file, got {md_file}"
    assert md_file.is_file(), f"File {md_file} does not exist"
    assert pdf_file.suffix == '.pdf', f"Expected pdf file, got {pdf_file}"

    cv = load_cv(md_file, phone, email)
    pdf = MarkdownPdf()
    pdf.add_section(Section(cv))

    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(pdf_file)


@logging()
def convert_directory(input_dir: Path, output_dir: Path, phone: Optional[str], email: Optional[str]):
    for dir_path, _, file_names in input_dir.walk():
        logger.info("Found directory: {dir_path}", dir_path=dir_path)

        for file in file_names:
            input_file = Path(dir_path, file)
            if input_file.suffix == '.md':
                output_file = output_dir.joinpath(
                    input_file.relative_to(input_dir).with_name(f"Lery_Orlov_{input_file.name}").with_suffix('.pdf')
                )
                logger.info("Converting {input_file} to {output_file}", input_file=input_file, output_file=output_file)
                markdown_to_pdf(input_file, output_file, phone, email)


@logging()
@logger.catch(reraise=True)
def main():
    from dotenv import load_dotenv
    load_dotenv()  # take environment variables from .env.
    convert_directory(
        input_dir=Path('./cv'),
        output_dir=Path('./build'),
        phone=os.environ.get("PHONE"),
        email=os.environ.get("EMAIL")
    )


if __name__ == '__main__':
    logger.info("Converting CVs to PDFs.")
    main()
    logger.success("All files successfully converted.")
