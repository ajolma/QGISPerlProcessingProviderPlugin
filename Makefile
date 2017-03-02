dist:
	mkdir perlprocessing
	cp LICENSE README.md __init__.py PerlProcessingProviderPlugin.py PerlProcessingProvider.py PerlProcessor.py metadata.txt perlprocessing
	zip perlprocessing.zip perlprocessing/*
	rm -rf perlprocessing
