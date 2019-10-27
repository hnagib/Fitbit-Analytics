SHELL=/bin/bash

install-env:
	conda create -n fitbit python=3.7
	conda activate fitbit && pip install -r requirements.txt
	conda activate fitbit && conda install ipykernel
	conda activate fitbit && python -m ipykernel install --user --name fitbit --display-name "fitbit"

uninstall-env:
	conda remove --name fitbit --all
