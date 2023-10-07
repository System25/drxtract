#
# Javascript library generation Makefile.
# 
# You will need Python's Transcrypt.
#

PY2JS='pj'
STRIP='strip-hints'
sources = $(wildcard lingosrc/[^_]*.py) \
	$(wildcard lingosrc/ast/[^_]*.py) \
	$(wildcard lingosrc/codegen/[^_]*.py) \
	$(wildcard lingosrc/model/[^_]*.py) \
	$(wildcard lingosrc/opcodes/[^_]*.py) \
	$(wildcard lingosrc/parse/[^_f]*.py)
stripped = $(sources:.py=.pys)
jsclasses = $(stripped:.pys=.js)

py_packages = lingosrc \
	lingosrc/ast \
	lingosrc/codegen \
	lingosrc/model \
	lingosrc/opcodes \
	lingosrc/parse

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

all: ../js/drxtract/index.js

../js/drxtract/index.js: $(jsclasses)
	cp --parents $(jsclasses) ../js/drxtract
	$(foreach pack,$(py_packages), \
		$(PY2JS) $(pack)/__init__.py ; \
		mv $(pack)/__init__.js ../js/drxtract/$(pack)/index.js ; \
	)
	touch ../js/drxtract/index.js

%.pys: %.py
	$(STRIP) -o $@ $<
	sed -i -E "s/cast\([ ]*([A-Za-z_0-9]+)[ ]*,[ ]*([A-Za-z_0-9\.]+)[ ]*\)/\2/" $@
	sed -i -E "s/^from typing import .*//" $@


%.js: %.pys
	$(PY2JS) $<
	sed -i -E "s/^import \{([^}]+)\} from '([^']+)'/import {\1} from '\2.js'/" $@
	$(foreach pack,$(py_packages), \
		sed -i "s|$(notdir $(pack)).js'|$(notdir $(pack))/index.js'|" $@ ; \
	)


clean:
	rm -f lingosrc/*.js
	rm -f lingosrc/*.map
	rm -f lingosrc/ast/*.js
	rm -f lingosrc/ast/*.map
	rm -f lingosrc/codegen/*.js
	rm -f lingosrc/codegen/*.map
	rm -f lingosrc/model/*.js
	rm -f lingosrc/model/*.map
	rm -f lingosrc/opcodes/*.js
	rm -f lingosrc/opcodes/*.map
	rm -f lingosrc/parse/*.js
	rm -f lingosrc/parse/*.map
	rm -rf ../js/drxtract/*

