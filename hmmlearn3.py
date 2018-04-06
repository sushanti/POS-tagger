import sys
import json
from collections import defaultdict

if  len(sys.argv) > 0:	
	try:
		transDict = defaultdict(dict)
		emiDict = defaultdict(dict)
		smoothDict = defaultdict(dict)
		tagsSet = set(["start","end"])
		
		with open(sys.argv[1], 'r',encoding='utf8') as file:
			transDict ["transition"] ["start"] = {}
			transDict ["transition"] ["end"] = {}
			transDict ["transition"]["start"] ["totalTransCount"]=0
			transDict ["transition"]["end"] ["totalTransCount"]=0
			for line in file:
				tags=[]
				tagObs=[]
				for word in line.split():
					if "/" in word:
						tagObs.append(word)
						words = word.rsplit("/",1)
						tags.append(words[1])
						tagsSet.add(words[1])
				
				
				#Calculating transition matrix
				if len(tags)>=1:
					if tags[0] in transDict ["transition"] ["start"]:
						transDict ["transition"]["start"][tags[0]]+=1
					else:
						transDict ["transition"]["start"][tags[0]]=1
					transDict ["transition"]["start"] ["totalTransCount"]+=1

				for i in range(0,len(tags)-1):
					tag=tags[i]
					nextTag = tags[i+1]
					
					if tag in transDict["transition"]:
						if nextTag in transDict["transition"][tag]:
							transDict ["transition"] [tag] [nextTag] +=1
						else:
							transDict ["transition"] [tag] [nextTag] =1
						transDict ["transition"] [tag] ["totalTransCount"]+=1
					else:
						transDict["transition"] [tag]={}
						transDict ["transition"] [tag] ["totalTransCount"]=1
						transDict ["transition"] [tag] [nextTag] =1
					
				
				if tags[len(tags)-1] in transDict ["transition"]["end"]:
					transDict ["transition"] ["end"] [tags[len(tags)-1]] +=1
					transDict ["transition"] ["end"] ["totalTransCount"]+=1
				else:
					transDict ["transition"] ["end"] [tags[len(tags)-1]] =1
					transDict ["transition"] ["end"] ["totalTransCount"]+=1
				
						
				#Calculating emission matrix
				for obs in tagObs:
					data = obs.rsplit("/",1)
					if data[1] in emiDict ["emission"]:
						if data[0] in emiDict ["emission"] [data[1]]:
							emiDict ["emission"][data[1]][data[0]]+=1
						else:
							emiDict ["emission"][data[1]][data[0]]=1
						emiDict ["emission"] [data[1]]["totalEmissionCount"]+=1
					else:
						emiDict ["emission"][data[1]] = {}
						emiDict ["emission"][data[1]]["totalEmissionCount"]=1
						emiDict ["emission"] [data[1]][data[0]]=1	
						
		#smoothing transition matrix
		for tag in tagsSet:
				if tag in transDict["transition"]:
					for subtag in tagsSet:
						if subtag not in transDict["transition"][tag] and subtag!="start" and subtag!="end":
							transDict ["transition"] [tag] [subtag] = 0;
							if tag not in smoothDict:
								smoothDict[tag]=1
				else:
					transDict ["transition"] [tag] = {}
					transDict ["transition"] [tag] ["totalTransCount"] = 0					
					for eachtag in tagsSet:
						transDict ["transition"] [tag] ["totalTransCount"] +=1
						transDict ["transition"] [tag] [eachtag] = 1
									
		for tag in smoothDict:
			for subtag in transDict["transition"][tag]:
				if subtag!="totalTransCount":
					transDict ["transition"] [tag] [subtag] += 1; 
					transDict ["transition"] [tag ]["totalTransCount"] += 1;
				
					
				
		for tag in transDict ["transition"]:
			for subtag in transDict ["transition"] [tag]:
				if(subtag!="totalTransCount"):
					transDict ["transition"] [tag][subtag] = transDict ["transition"] [tag][subtag] / transDict ["transition"][tag]["totalTransCount"]
			
		for tag in emiDict ["emission"]:
			for obs in emiDict ["emission"] [tag]:
				if(obs!="totalEmissionCount"):
					emiDict ["emission"] [tag][obs] = emiDict ["emission"] [tag][obs] / emiDict ["emission"] [tag]["totalEmissionCount"]
		transDict.update(emiDict)
		json = json.dumps(transDict)	
		
		fileToWrite = open("hmmmodel.txt", "w")
		fileToWrite.write(json)
		fileToWrite.close()
	except OSError as e:
		print("File not found")
else:
	print("Enter file name and path")
