
.PHONY: clean

clean:
	rm -r build dist yo.egg-info

install:
	python3 setup.py install --user --record install.log

watch:
	bin/watch.sh ./yo python3 setup.py install --user

uninstall:
	cat install.log | xargs rm
