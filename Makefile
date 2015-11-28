all: clean pushtogit
pushtogit: 
	git push

clean:
	rm -f *~
