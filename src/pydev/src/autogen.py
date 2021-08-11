import os
import sys
import re
def load(cand):
	cb_list = []
	for d in sys.path: # for searchable import paths...
		for p in os.walk(d):      # find a directory whose contents are navigated until...
			if cand == p[0].split(os.path.sep)[-1]:  #our target loc for automated cb make is found
				lloc = p[0]
				break
	for loc in os.walk(lloc): #for the location for the modules
		if not loc[0].split(os.path.sep)[-1] in ["nn", "modules"]:
			continue
		for f in loc[2]:  #for the files in the dir
			if re.match(r".*\.py\b",f) :   # if a pure python source
					cb_list.append(os.path.join(loc[0],f))
	




	return cb_list







if __name__ == "__main__":
	files = load("torch")

	for fl in files	:
		if "linear" in fl:
			with open(fl, "r") as f:
				print(f.read())
