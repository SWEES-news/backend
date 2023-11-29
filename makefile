include common.mk

API_DIR = server
DB_DIR = userdata
REQ_DIR = .

PKG = $(API_DIR)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

FORCE:

prod: tests github

github: FORCE
	- git commit -a
	git push origin master

tests: 
	cd $(API_DIR); make tests
	cd $(DB_DIR); make tests


dev_env: FORCE
	pip3 install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	cd $(API_DIR); make docs
