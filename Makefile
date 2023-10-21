#
# Javascript library generation Makefile.
# 
# You will need Python's Transcrypt.
#

../mods/drxtract/index.js:
	mkdir -p ../mods/drxtract
	$(MAKE) -C drxtract

clean:
	$(MAKE) -C drxtract clean

