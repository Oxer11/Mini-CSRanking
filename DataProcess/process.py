
fin = open("csrankings.csv", "rb")
fout = open("institution.csv", "wb")
lists = []
for line in fin:
    line = line.decode("utf-8")
    lists.append(line.strip().split(",")[1])
lists = list(set(lists))
for i in lists:
    fout.write((i + "\n").encode("utf-8"))