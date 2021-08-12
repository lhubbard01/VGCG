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

def gather_src(files):
	pass 	
def generate_cb_file(loc):
	leading_whitespace     = re.compile(r"^\s+")
	end_of_fn_sig          = re.compile(r"[\w\s\d,:_\)]+\)\s*:") # Figure out why not coutning
	#TODO figure out ways to get whether has hyperparams, etc

	files = load(loc)

	print(files)
	indents  = [0]
	argums   = []

	indent   = 0
	nested   = 0

	init_hit   = False
	ended_args = False
	for fl in files:

		with open(fl, "r") as f:
			for i, line in enumerate(f.readlines()):

				lwsm = leading_whitespace.match(line)
				
				if lwsm:
					lwsm = lwsm.span()[1]
				else:
					lwsm = 0
				
				if "class" in line :
					nested += 1
					init_hit   = False
					ended_args = False

				elif "__init__" in line and not init_hit:
					print("in init")
					init_hit = True
					ended_args = False
					argums = []
					print(line, line.split(","))
					if end_of_fn_sig.match(line):
						print("matched as beginning and end")
						argums += line.split(",")
						print(argums)
						ended_args = True
					print("exitting init")
				elif init_hit and not ended_args:
					if end_of_fn_sig.match(line):
						ended_args = True
						print("ended reading in args")
					
					argums += line.split(",")

				if lwsm > indents[-1]: #leading white space match
					indents += [lwsm]
				elif lwsm < indents[-1]:
					indents.pop(-1)
					nested -= 1
					if init_hit and ended_args:

						print(argums)

				elif lwsm == indents[-1]:

					pass
				print(line, indents)
				input()
			
def gen_js(TYPE, isparam, name, hyperPs, indent : int = 4):
	fn = ""
	fn += "function " + TYPE + " () {\n"
	fn += indent * " " + "let data = {"
	fn += indent * " " + "isParametric: " + isparam + "," + "\n"
	fn += indent * " " + "isNative: true," + "\n"
	fn += indent * " " + "mType: " + TYPE + "," + "\n"
	fn += indent * " " + "Name: " + "name,\n"
	fn += indent * " " + "hyperp:  JSON.stringify( +" + str(hyperPs) +", )\n"
	fn += indent * " " + "}; \n"
	fn += indent * " " + "send(data, \"add\");"
	fn += "}"

	return fn

if __name__ == "__main__":
	generate_cb_file("torch")
	"""files = load("torch")

	for fl in files	:
		if "linear" in fl:
			with open(fl, "r") as f:
				print(f.read())"""
