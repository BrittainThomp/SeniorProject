import csv
import random
import statistics
import math
import py_midicsv as pm

# notes here will dictate how long the melody is in notes. I've commented out portions of the
# template that are required for converting the csv to midi. This was to streamline the development
# process and keep me on track for producing deliverables.
def genMelody(notes,filename):

    with open(filename+'.csv','w') as f:
        writer = csv.writer(f, delimiter='\n')

        # note is a value ranging from 0-14. 0 is a rest. 1 is a hold. 
        # 2-14 represent the twelve steps in an octave respectively.
        # C, C#, D, D#, E, F, G, G#, A, A#, B.
        
        # melody will store the array of notes.
        melody = []
        for i in range(notes):
            noteType = str(random.randint(0,14))           
            string = "['" + str(noteType) + "']"
            melody.append(string)
            

        for row in melody:
            writer.writerow([row])
    return filename+'.csv'
          
def outputMelody(notes,out):

    with open(notes, 'r') as f:
            read = csv.reader(f, delimiter=',')
            noteList = []
            for row in f:
                noteList.append(row.strip("[']\n"))

    with open(out+".csv",'w') as results:
        writer = csv.writer(results, delimiter='\n')

        midi = []
        midi.append('0, 0, Header, 0, 1, 960')
        midi.append('1, 0, Start_track')
        time = 0

        for i in range(len(noteList)):
            if (noteList[i]=="0" or noteList[i]=="1"):
                time+=240
                break
            if(noteList[i] != "1"):
                midi.append("1, " + str(time) + ", Note_on_c, 0, " + str(int(noteList[i])+46) + ", 127")
                time+=240
                string = ""
            j = i+1
            if(j<(len(noteList)-1)):
                while(noteList[j]=="1" and j<(len(noteList)-1)):
                    time+=240
                    j+=1
                midi.append("1, " + str(time) + ", Note_off_c, 0, " + str(int(noteList[i])+46) + ", 0")  
                time+=240
                i=j
            elif(noteList[i]!="1"):
                midi.append("1, " + str(time) + ", Note_off_c, 0, " + str(int(noteList[i])+46) + ", 0")   
                time+=240
                
        midi.append('1, '+str(time)+ ', End_track')        
        midi.append('0, 0, End_of_file')
        writer.writerow(midi)
        
        
        midi_obj = pm.csv_to_midi(midi)

        with open(out+".mid","wb") as out_file:
            midi_writer = pm.FileWriter(out_file)
            midi_writer.write(midi_obj)
    
def fitnessfunc(file):
    with open(file,'r') as f:
        fitness = 0
        read = csv.reader(f, delimiter=',')
        noteList = []
        for row in read:
            noteList.append(int(row[0].strip("[']")))

        for i in range(len(noteList)-2):
            duration = 1

            # checks for repeated notes
            if noteList[i] == noteList[i+1] == noteList[i+2] != 1:
                fitness+=1
         
            #checks for notes duration. Remember: Since a 1 represens a held note, we need
            # to score those seperately from a repated note.
            duration = 1
            if noteList[i] != 1 and noteList[i+1] == 1:
                for j in range(i+1, len(noteList)-1):
                    if noteList[j] == 1 and noteList[j+1] == 1:
                        duration+=1
                    else:
                        break
                if duration >= 4:
                    fitness += 1

        # I considered two different methods for this. One was utilizing sum() function and iterating the list
        # while the other was the much cleaner ptsdev() func from the statistics library. I opted for the
        # cleaner approach. Utilizing pstdev to get a meaningful measurement is something I will improve.

        # using standard deviation to promote a varied note selection 
        noteVaried = math.trunc(statistics.pstdev(noteList))
        if noteVaried < 3:
            fitness+=1
    return fitness


def geneticAlg(gens,length):
    
    #init parent arrays outside of generation iteration so they aren't wiped everytime
    parents = []
    parentsScore = []
    children = []

    #fill the first ancestors
    for j in range(5):
        #create a parent melody with defined length and name it by generation and parent
        parents.append(genMelody(length,'results/gen1parent'+str(j)))
        #score the parent. This isn't a good way to store this data.
        parentsScore.append(str(fitnessfunc(parents[j])))
    
    for i in range(gens):

        #pairing the parents
        pair1 = []
        pair2 = []

        # need to put in a way to sort the melodies by score. Maybe change melody func to call the fitness func?
        # This pair appending doesn't work at all. It's pairing scores not the actual melodies
        pair1.append(parentsScore[0])
        pair1.append(parentsScore[1])
        for parents in range(len(pair1)):
            print(pair1)

        pair2.append(parentsScore[2])
        pair2.append(parentsScore[3])
        for parents in range(len(pair2)):
            print(pair2)

# the reason for this length is to get a meaningful fitness measurement. 
# Smaller values resulted in multiple low scoring melodies
geneticAlg(5,1024)


