
all:
	python build.py build

msi:
	python build.py bdist_msi

dmg:
	python build.py bdist_dmg
