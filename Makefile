all: status

clean:
	cd hackthology && $(MAKE) clean
	cd timtadh.github.io && $(MAKE) clean

rm-content:
	cd timtadh.github.io && $(MAKE) rm-content

nuke: clean
	cd timtadh.github.io && $(MAKE) nuke

update:
	cd hackthology && $(MAKE) html
	cp -r hackthology/output/* timtadh.github.io/

status: update
	cd timtadh.github.io/ && $(MAKE) status

diff: update
	cd timtadh.github.io/ && $(MAKE) diff

add: clean update
	cd timtadh.github.io/ && $(MAKE) add

commit: add
	cd timtadh.github.io/ && $(MAKE) commit

publish: commit
	cd timtadh.github.io/ && $(MAKE) publish

.PHONY: clean nuke update publish status rm-content commit add
