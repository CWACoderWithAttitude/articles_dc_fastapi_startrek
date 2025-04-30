# run tests
test:
	pytest test_main.py

# run tests on any change
continuous_test:
#	ptw *.py
	ptw main.py settings.py test_*.py


# generate coverage report as html
coverage:
	pytest test_main.py --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html

# start app in dev mode
# --host="0.0.0.0" makes the server available on all network interfaces
# --port=8000 specifies the port on which the server will listen
# --reload makes the server restart automatically when code changes

dev:
	uvicorn main:app --host="0.0.0.0" --port=8000 --reload
