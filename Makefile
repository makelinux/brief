check:
	./brief.py ./tests/basic.c | grep -q "tests/basic.c: first second third"
