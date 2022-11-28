check:
	if ./brief.py -r | grep  "xxx"; then false else true; fi
	./brief.py ./tests/basic.c | grep -q "tests/basic.c: first second third"
	./brief.py -r | grep -q "tests/basic.c: first second third"
	./brief.py -r | grep -q "tests/module.c: first second third"
	./brief.py -r | grep -q "tests/brief.cpp: first second third"
