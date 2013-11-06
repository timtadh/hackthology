clean:
	cd hackthology && $(MAKE) clean
	cd timtadh.github.io && $(MAKE) clean

reset:
	cd timtadh.github.io && $(MAKE) reset

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

.PHONY: clean nuke update publish status reset commit add
