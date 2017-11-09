#Roy David
#Bascriptie

#Descr:	calculate accuracy of distant supervision method
#	outputs accuracy in %'s

print("")
print("Descr: calculate accuracy of distant supervision method")
print("Manually annotated file")
print("If N, S, E, W was given behind the line the program was wright")
print("If U, X, V was given behind the line the program was wrong*")
print("*: U = location unknown: either user or location is not retrievable, X = location that does not fit within areas, V = location is vague")
print("")

annotated = open("random100_annotated.txt").readlines()
print("RESULTS:")
print("total: ", len(annotated))

areas = ["N\n","S\n","E\n","W\n"]
bad = []

for line in annotated[:100]:
	line = line.split("\t")
	if line[3] not in areas:
		bad.append(line)

print("bad: ", len(bad))
for line in bad:
	if line[3] == "U\n":
		print("\tUknown location: ", line) # meaning either username has changed/user deleted or location was removed from profile and not possible to retrieve
	elif line[3] == "X\n":
		print("\tWrong location: ", line) # meaning location that does not fit area
	elif line[3] == "V\n":
		print("\tVague location: ", line) # meaning location could be multiple areas
	else:
		print("\t", line)
good = len(annotated) - len(bad)
print("good: ", good)
acc = (good/(len(annotated)))*100
print("acc: ", acc,"%")
print("")