import csv
import random



def genMelody():

    header = [['0, 0, Header, 0, 1, 960'], 
                ['1, 0, Start_track']]

    with open('goodTemplate.csv','w') as f:
        writer = csv.writer(f, delimiter='\n')
        # writer.writerow(header)

        # note is a value ranging from 0-17. 0 is a rest. 17 is a hold. 1-16 represent the two octaves of notes.
        time = 0
        melody = []

        for i in range(20):
            noteType = str(random.randint(0,17))           
            string = "['" + str(noteType) + ", " + str(time) + "']"
            melody.append(string)
            time += 240

        for row in melody:
            writer.writerow([row])
         
        footer = [['0, 0, End_of_file']]
        # writer.writerow(footer)
    


def fitnessfunc(file):
    with open(file,'r') as f:
        fitness = 0
        read = csv.reader(f, delimiter=',')
        firstNote = None
        secondNote = None
        thirdNote = None
        i=0
        print('finding fitness')
        for row in read:
            if firstNote == None:
                firstNote = row[0]
                print(firstNote)
                continue
            if secondNote == None:
                secondNote = row[0]
                print(secondNote)
                continue
            if thirdNote == None:
                thirdNote = row[0]
                print(thirdNote)
                continue


            while thirdNote != None:
                if firstNote == secondNote == thirdNote:
                    fitness +=1
                    print('Repeat Found!')
                    firstNote = None
                    secondNote = None
                    thirdNote = None
                else:
                    print("no repeats")
                    firstNote = None
                    secondNote = None
                    thirdNote = None
    print('--------Fitness Found------------')
    print(fitness)

# genMelody()
fitnessfunc('goodTemplate.csv')