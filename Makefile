.PHONY : init
init :  init_py init_js
init_py :
	pip install -r requirements.txt
	echo "python dependencies installed";
init_js : 
	cd ./vgcg/src/ && npm i && cd ../../../
	echo "frontend server dependencies installed";
