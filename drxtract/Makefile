#
# Javascript library generation Makefile.
# 
# You will need Python's Transcrypt.
#

JSSRC="../../mods/_drxtract"
OUTPUT="../../mods/drxtract"
PY2JS='pj'
STRIP='strip-hints'
sources = \
	$(wildcard lingosrc/ast/[^_]*.py) \
	$(wildcard lingosrc/codegen/[^_]*.py) \
	$(wildcard lingosrc/model/[^_]*.py) \
	$(wildcard lingosrc/opcodes/[^_]*.py) \
	$(wildcard lingosrc/parse/[^_f]*.py) \
	$(wildcard bitd/[^_]*.py) \
	$(wildcard cas/[^_]*.py) \
	$(wildcard vwsc/[^_]*.py)
	
stripped = $(sources:.py=.pys)
jsclasses = $(stripped:.pys=.js)

py_packages = lingosrc \
	lingosrc/ast \
	lingosrc/codegen \
	lingosrc/model \
	lingosrc/opcodes \
	lingosrc/parse \
	bitd \
	cas \
	vwsc

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

all: $(OUTPUT)/index.js

$(OUTPUT)/index.js: $(jsclasses)
	cp --parents $(jsclasses) $(OUTPUT)
	$(foreach pack,$(py_packages), \
		$(STRIP) -o $(pack)/__init__.pys $(pack)/__init__.py ; \
		sed -i -E "s/^from typing import .*//" $(pack)/__init__.pys ; \
		$(PY2JS) $(pack)/__init__.pys ; \
		rm $(pack)/__init__.pys ; \
		sed -i -E "s/^import \{([^}]+)\} from '([^']+)'/import {\1} from '\2.js'/"  $(pack)/__init__.js ; \
		mv $(pack)/__init__.js $(OUTPUT)/$(pack)/index.js ; \
	)
	touch $(OUTPUT)/index.js
	cd $(JSSRC); find . -name "*.js" -exec cp \{\} ../drxtract/\{\} \;

%.pys: %.py
	$(STRIP) -o $@ $<
	sed -i -E "s/cast\([ ]*([A-Za-z_0-9]+)[ ]*,[ ]*([^ \)]+)[ ]*\)/\2/" $@
	sed -i -E "s/^from typing import .*//" $@
	sed -i -E "s/^from abc import .*//" $@
	sed -i -E "s/__metaclass__ = .*//" $@
	sed -i "s/@abstractmethod//" $@



%.js: %.pys
	$(PY2JS) $<
	sed -i -E "s/^import \{([^}]+)\} from '([^']+)'/import {\1} from '\2.js'/" $@
	sed -i -E "s/^import \{Enum\} from 'enum.js'/import {Enum} from 'enum'/" $@
	sed -i -E "s/^import \{([^}]+)\} from 'builtins.js'/import {\1} from 'py2jscompat'/" $@	
	sed -i -E "s/^class[ ]+([^ ]+)/export class \1/" $@
	sed -i -E "s/^function[ ]+([A-Za-z0-9]+)/export function \1/" $@
	sed -i -E 's/(ValueError|ZeroDivisionError|EnvironmentError)/Error/' $@
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
	rm -f bitd/*.js
	rm -f bitd/*.map
	rm -f cas/*.js
	rm -f cas/*.map
	rm -f vwsc/*.js
	rm -f vwsc/*.map
	rm -rf $(OUTPUT)/*

