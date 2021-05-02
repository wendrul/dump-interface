import matplotlib.pyplot as plt



def ParseSpikeInfoOnlyBiggestSpike(filename):
	#This is very hardcoded and specific to this case do not reuse
	Spikes = []
	SpikeNorms = []
	currentSpike = None
	parsedLines = []
	ignore = False
	with open(filename, "r") as file:
		lines = file.readlines()
		for line in lines:
			if "vol(a.u.)" in line or len(line) < 2:
				continue
			if "--" in line:
				Spikes.append(parsedLines)
				SpikeNorms.append(currentSpike)		
				currentSpike = None
				ignore = False
			elif "spike" in line:
				ignore = False
				if (currentSpike == None or currentSpike < float(line[9:19])):
					parsedLines = []
					currentSpike = float(line[9:19])
				else:
					ignore = True
			elif not ignore:
				parsedLines.append(list(map(float, line.split(", "))))
		Spikes.append(parsedLines)
		SpikeNorms.append(currentSpike)	
	return (Spikes, SpikeNorms)

def ParseSpikeInfoAllSpikes(filename):
	#This is very hardcoded and specific to this case do not reuse
	Spikes = []
	SpikeNorms = []
	parsedLines = []
	with open(filename, "r") as file:
		lines = file.readlines()
		for line in lines:
			if "vol(a.u.)" in line or len(line) < 2 or "--" in line:
				continue
			if "spike" in line:
				if (parsedLines != []):
					Spikes.append(parsedLines)
				SpikeNorms.append(float(line[9:19]))
				parsedLines = []
			else:
				parsedLines.append(list(map(float, line.split(", "))))
		Spikes.append(parsedLines)
	return (Spikes, SpikeNorms)

def GeneratePointsWithNbiggestMaxima(n, x, y):
	for i in n:
		x += [spike[i][1] for spike in Spikes]
		y += [spike[i][0] for spike in Spikes]

Spikes, SpikeValues = ParseSpikeInfoOnlyBiggestSpike("FreqTest.csv")


x = []
y = []
maxes = [0]
GeneratePointsWithNbiggestMaxima(maxes, x, y)

 

def mean(L):
	S = 0
	for x in L:
		S += x
	return S / len(L)

def GenerateFreqAndEvaluate(approxFreq, freqRange):
	newAbscissa = []
	Spikes, _ = ParseSpikeInfoAllSpikes("FreqTest.csv")
	Spikes2, _ = ParseSpikeInfoOnlyBiggestSpike("FreqTest.csv")
	for a in x:
		if abs(a - approxFreq) < freqRange:
			newAbscissa.append(a)
	freq = mean(newAbscissa)
	hit = 0
	total = 0
	for spike in Spikes:
		for u in spike:
			if abs(u[1] - freq) < freqRange:
				hit += 1
				break
		total +=1
	acc1 = hit / total
	hit = 0
	total = 0
	for spike in Spikes2:
		for u in spike:
			if abs(u[1] - freq) < freqRange:
				hit += 1
				break
		total +=1
	acc2 = hit / total
	print (f"For the approxFreq {approxFreq} Hz and a range of +-{freqRange:.1f}Hz:\n The tendency seems to be {freq:.1f}Hz with an accuracy of {acc1*100:.1f}% on the main spikes and {acc2*100:.1f}% accross all detections.")

#GenerateFreqAndEvaluate(2780, 100)

# SpikeValues.sort()
# print(f"\n\nmean of norms: {SpikeValues[0:10]}")

#Frequencie
#568 Hz
#1731 Hz
#4252 Hz

#mabe
#2476



plt.scatter(x, y, s=1, marker=3)
plt.yscale("log")
plt.show()

