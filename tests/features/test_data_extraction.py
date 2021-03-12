from special_students.features.data_extraction import Extraction


RAW_DATA: str = "data/raw/ResultadoAE20211.pdf"


def test_extraction():
    ext = Extraction(RAW_DATA)
    df = ext.extract()
    assert df.shape[0] == 604
