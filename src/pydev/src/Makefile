.PHONY : init
init :  init_py init_js
init_py :
	python3 setup.py install --user;
	echo "python dependencies installed";

init_js :
	npm i package.json;
	echo "frontend server dependencies installed";
