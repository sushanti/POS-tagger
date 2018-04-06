import sys
import json
from collections import defaultdict
from collections import defaultdict

transition={}
emission={}


with open('hmmmodel.txt','r',encoding='utf8') as file:
	data = json.loads(file.read())
	transition = data ["transition"]
	emission = data["emission"]
	
outputFile = open("hmmoutput.txt", "w+",encoding='utf-8')
with open(sys.argv[1],'r',encoding='utf8') as file:
	for line in file:
		index=0;
		viterbi = defaultdict(dict)
		viterbiTags = defaultdict(dict)
		words = line.split()
		for i in range(0,len(words)):
			for tag in emission:
				if words[i] in emission[tag]:
					viterbi[index][tag] = {}
					if i==0 and i==len(words)-1:
						viterbi[index][tag] ["value"]  = transition["start"][tag] * emission[tag][words[i]] * transition ["end"] [tag]
					elif i==0:
						viterbi[index][tag] ["value"]  = transition["start"][tag] * emission[tag][words[i]]
					elif i < (len(words)-1):
						maximum=0.0
						for prevTags in viterbi[index-1]:
							if  viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]] >= maximum:
								maximum = viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]]
								viterbi[index][tag] ["value"] = viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]]
								viterbi[index][tag] ["prevTag"] = prevTags
					elif i==len(words)-1:
						maximum=0.0
						for prevTags in viterbi[index-1]:
							if  viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]] * transition ["end"] [tag]  >= maximum:
								maximum = viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]] * transition ["end"] [tag]
								viterbi[index][tag] ["value"] = viterbi[index-1][prevTags] ["value"] * transition[prevTags][tag] * emission[tag][words[i]] * transition ["end"] [tag]
								viterbi[index][tag] ["prevTag"] = prevTags
			
			if not index in viterbi:
				if i==0 and i==len(words)-1:
					for tag in transition:
						if tag!="start" and tag!="end":
							viterbi[index][tag] = {}
							viterbi[index][tag] ["value"] = transition ["start"][tag] * transition ["end"] [tag]
				elif i==0:
					for tag in transition:
						if tag!="start" and tag!="end":
							viterbi[index][tag] = {}
							viterbi[index][tag] ["value"] = transition ["start"][tag]
				elif i<len(words)-1:
					for tag in transition:
						if tag!="start" and tag!="end":
							maximum=0.0
							viterbi[index][tag] = {}
							for prevTag in viterbi[index-1]:
								if viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag] >= maximum:
									maximum = viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag]
									viterbi[index][tag] ["value"] = viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag]
									viterbi[index][tag] ["prevTag"] = prevTag
				elif i==len(words)-1:
					for tag in transition:
						if tag!="start" and tag!="end":
							maximum=0.0
							viterbi[index][tag] = {}
							for prevTag in viterbi[index-1]:
								if viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag] * transition["end"][tag] >= maximum:
									maximum = viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag] * transition["end"][tag]
									viterbi[index][tag] ["value"] = viterbi[index-1][prevTag] ["value"] * transition[prevTag][tag] * transition["end"][tag]
									viterbi[index][tag] ["prevTag"] = prevTag
			index+=1
			
		maximum=0.0
		
		for lastWordTag in viterbi[index-1]:
			if viterbi[index-1][lastWordTag] and viterbi[index-1][lastWordTag]["value"]>=maximum:				
				maximum = viterbi[index-1][lastWordTag]["value"]
				viterbiTags[index-1] = lastWordTag;
		
		if index>1:
			for i in range(index-1,0,-1):
				viterbiTags[i-1] = viterbi[i][viterbiTags[i]]["prevTag"]
		
				
		outputLine=""
		for i in range(0,len(words)):
			outputLine+=words[i]+"/"+viterbiTags[i]+" "
		outputLine = outputLine.rstrip()
		outputFile.write(outputLine)
		outputFile.write("\n")     
outputFile.close()
