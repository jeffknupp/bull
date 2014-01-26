.PHONY: docs release clean build

clean:
	rm -rf bull_env htmlcov

build:
	virtualenv bull_env && source bull_env/bin/activate && \
		pip install -r requirements.txt

test: clean build
		source bull_env/bin/activate && \
		coverage run --source=bull setup.py test && \
		coverage html && \
		coverage report
