SHELL=/bin/bash

install-env:
	conda create -n fitbit python=3.7
	source activate fitbit && pip install -r requirements.txt
	source activate fitbit && conda install ipykernel
	source activate fitbit && python -m ipykernel install --user --name fitbit --display-name "fitbit"

uninstall-env:
	conda remove --name fitbit --all
