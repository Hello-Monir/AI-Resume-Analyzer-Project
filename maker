.PHONY: setup run test
setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run:
\tstreamlit run main.py

test:
\tpytest -q
