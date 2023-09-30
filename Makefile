#
# Javascript library generation Makefile.
# 
# You will need Python's Transcrypt.
#

drxtract.lib.js:
	$(MAKE) -C drxtract

clean:
	$(MAKE) -C drxtract clean

