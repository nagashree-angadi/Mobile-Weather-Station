import random
result = []
with open("E:/Project/Final/data/channel_data.csv") as f:
    for line in f:
        #print(line)
        if( not line[0].isalpha() and line != ''):
            linedata = line.strip(' \n').split('\t')
            #print(linedata)
            for i in linedata:
                if(len(i) != 0):
                    data = i.split(',')
                    date = data[0].split(" ")[0]
                    co = data[2]
                    pm = data[3]
                    humi = data[4]
                    temp = data[5]
                    lat = data[6][0:10]
                    long = data[7][0:10]
                    result.append(
                        long+","
                        +lat+","
                        +co+","
                        +pm+","
                        +humi+","
                        +temp+","
                        +date+"\n"
                    )

cat = ""

target = open("E:/Project/Final/data/data.csv", 'w')
for i in result:
    cat += i

target.write(cat[:-1])
print(cat)
target.close()

