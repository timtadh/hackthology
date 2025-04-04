all: status

clean:
	cd hackthology && $(MAKE) clean
	cd timtadh.github.io && $(MAKE) clean

rm-content:
	cd timtadh.github.io && $(MAKE) rm-content

nuke: clean
	cd timtadh.github.io && $(MAKE) nuke

html:
	cd hackthology && $(MAKE) html

pub-html:
	cd hackthology && $(MAKE) pub-html

update: pub-html
	cp -r hackthology/publish/* timtadh.github.io/

status: update
	cd timtadh.github.io/ && $(MAKE) status

diff: update
	cd timtadh.github.io/ && $(MAKE) diff

add:
	cd timtadh.github.io/ && $(MAKE) add

commit:
	cd timtadh.github.io/ && $(MAKE) commit

publish:
	cd timtadh.github.io/ && $(MAKE) publish

.PHONY: clean nuke update publish status rm-content commit add html pub-html
