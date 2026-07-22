.PHONY: all clean history

all:
	/app/bin/rebuild-forge

clean:
	rm -rf /app/repo/target /app/output/*

history:
	git -C /app/repo log --graph --oneline --decorate --all
