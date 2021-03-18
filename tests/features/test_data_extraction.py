from special_students.extraction.data_extraction import Extraction
from special_students.settings import settings

RAW_DATA: str = settings.raw_pdf_path


def test_extraction():
    ext = Extraction(RAW_DATA)
    df = ext.extract()
    assert df.shape[0] == 604
