
rm-db:
	rm -rf data/db/*

runpy:
	python3 main.py

pylint:
	pylint ./ --recursive=true
