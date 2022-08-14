###
# /bot-discord/Makefile
# py-bot-uprm
# 
# Created by Gabriel S Santiago on 2022/08/12
# 
# Last Modified: Friday, 12th August 2022 11:53:21 am
# Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
# 
# Copyright © 2022 agSant01. All rights reserved.
# Copyright © 2022 teamMADE. All rights reserved.
###


test:
	python -m unittest discover -s tests -t .

check:
	@echo "\n> Black formatter:"
	black --diff --color --preview --line-length 89 .
	@echo "" 
	@echo "\n> autoflake: remove unused vars and imports"
	autoflake --exclude */venv/* --recursive --remove-unused-variables --remove-all-unused-imports .
	@echo ""

	@echo "\n> isort: ordering imports"
	isort --profile=black --check --diff .
	@echo ""

lint:
	black --preview --line-length 89 .
	autoflake --exclude */venv/* --recursive --in-place --remove-unused-variables --remove-all-unused-imports .
	isort --profile=black .
