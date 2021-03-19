from special_students.extraction.data_extraction import data_extraction
from special_students.features.build_features import build_features
from special_students.features.data_collection import data_collection
from special_students.features.feature_engineering import feature_engineering


def data_pipeline():
    print("Starting data pipeline...")
    data_extraction()
    feature_engineering()
    data_collection()
    build_features()
    print("Data pipeline finished.")


if __name__ == "__main__":
    data_pipeline()
