data_pipeline: extract_data_from_pdf feature_engineering data_collections build_features

extract_data_from_pdf:
	python special_students/extraction/data_extraction.py

feature_engineering:
	python special_students/features/feature_engineering.py

data_collections:
	python special_students/features/data_collection.py

build_features:
	python special_students/features/build_features.py