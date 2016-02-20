all: clean pushtogit
pushtogit: 
	git push

clean:
	rm -f *~


install:
	mkdir pairdiff
	cp filter* pairdiff
	cp blockaverage* pairdiff
	cp __init__* pairdiff
	cp main* pairdiff
	cp process* pairdiff
	cp ui* pairdiff
	cp xmlreader* pairdiff
	cp pairdiff.py pairdiff
	cp pairdiff.pyc pairdiff
	rm -rf example


