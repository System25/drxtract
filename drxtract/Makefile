#
# Javascript library generation Makefile.
# 
# You will need Python's Transcrypt.
#

PY2JS='pj'
sources = $(wildcard lingosrc/[^_]*.py) $(wildcard lingosrc/ast/[^_]*.py)
jsclasses = $(sources:.py=.js)
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

all: drxtract.lib.js

drxtract.lib.js: $(jsclasses)
	cat $(jsclasses) > ../drxtract.lib.js


%.js: %.py
	$(PY2JS) $<

clean:
	rm -f lingosrc/*.js
	rm -f lingosrc/*.map
	rm -f lingosrc/ast/*.js
	rm -f lingosrc/ast/*.map
	rm -f ../drxtract.lib.js

