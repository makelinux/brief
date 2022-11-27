check:
	if ./brief.py -r | grep  "xxx"; then false else true; fi
	./brief.py ./tests/basic.c | grep -q "tests/basic.c: first second third"
