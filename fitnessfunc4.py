import csv
import random



def genMelody():

    # header = [['0, 0, Header, 0, 1, 960'], 
    #             ['1, 0, Start_track']]

    with open('goodTemplate.csv','w') as f:
        writer = csv.writer(f, delimiter='\n')
        # writer.writerow(header)

        # note is a value ranging from 0-14. 0 is a rest. 1 is a hold. 2-14 represent the twelve steps in an octave.
        melody = []

        for i in range(20):
            noteType = str(random.randint(0,14))           
            string = "['" + str(noteType) + ", " + str(time) + "']"
            melody.append(string)
            time += 240

        for row in melody:
            writer.writerow([row])
         
        # footer = [['0, 0, End_of_file']]
        # writer.writerow(footer)
    


def fitnessfunc(file):
    with open(file,'r') as f:
        fitness = 0
        read = csv.reader(f, delimiter=',')
        print('--------------------finding fitness--------------------------')
        noteList = []
        for row in read:
            noteList.append(row[0])


        for i in range(len(noteList)-2):
            duration = 1
            print('checking line : ' + str(i+1))
            # checks for repeated notes
            if noteList[i] == noteList[i+1] == noteList[i+2] != "['1":
                fitness+=1
                print('-------------')
                print('repeat found')
                print(str(noteList[i])+str(noteList[i+1])+str(noteList[i+2]))
                print('-------------')

            
            #checks for notes duration. Remember: a 1 is a hold of the previous note.
            duration = 1
            if noteList[i] != "['1" and noteList[i+1] == "['1":
                for j in range(i+1, len(noteList)-1):
                    if noteList[j] == "['1" and noteList[j+1] == "['1":
                        duration+=1
                    else:
                        break
                if duration >= 2:
                    fitness += 1
                    print('Note: ' + str(noteList[i]) + '. held for: ' + str(duration))

    print('--------Fitness Found------------')
    print(fitness)

# genMelody()
fitnessfunc('goodTemplate.csv')