publish: clean
	python -m build
	twine upload dist/*

clean:
	rm -vrf ./build ./dist ./*.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.tgz' -delete
