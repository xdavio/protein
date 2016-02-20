all: clean pushtogit
pushtogit: 
	git push

clean:
	rm -f *~

install:
	mkdir pairdiff
	mv filter* pairdiff
	mv blockaverage* pairdiff
	mv __init__* pairdiff
	mv main* pairdiff
	mv process* pairdiff
	mv ui* pairdiff
	mv pairdiff.py pairdiff
	mv pairdiff.pyc pairdiff
