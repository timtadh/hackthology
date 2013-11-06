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

publish: clean update
	cd timtadh.github.io/ && $(MAKE) publish

.PHONY: clean nuke update publish status reset
