
test_json:
	py.test --json=report.json tests/test_byhand.py

test:
	py.test tests/test_byhand.py

testall:
	py.test

test_api:
	./API-testing.py -p > tests/test_api.py

utf8:
	py.test -k utf8
