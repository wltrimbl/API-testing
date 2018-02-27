


test:
	py.test tests/test_byhand.py

testall:
	py.test

test_api:
	./API-testing.py -p > tests/test_api.py
