import csv
import random
import statistics
import math
import py_midicsv as pm

# notes here will dictate how long the melody is in notes. 
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
            string = str(noteType)
            melody.append(string)
            

        for row in melody:
            writer.writerow([row])
    return filename+'.csv'
          
def outputMelody(notes,out):

    with open(notes, 'r') as f:
            read = csv.reader(f, delimiter=',')
            noteList = []
            for row in read:
                noteList.append(row[0])

    with open(out+".csv",'w') as results:
        writer = csv.writer(results, delimiter='\n')

        midi = []
        midi.append('0, 0, Header, 0, 1, 960')
        midi.append('1, 0, Start_track')
        time = 0

        for i in range(len(noteList)):
            if (noteList[i] in "0" or noteList[i] in "1"):
                time+=240
               
            elif(noteList[i] not in "1" and noteList[i] not in "0"):
                midi.append("1, " + str(time) + ", Note_on_c, 0, " + str(int(noteList[i])+46) + ", 127")
                time+=240
            j = i+1

            if(j<(len(noteList)-1) and (noteList[j] in "1" or noteList[j] in "0")):
                while(noteList[j] in "1" and j<(len(noteList)-1)):
                    time+=240
                    j+=1
                midi.append("1, " + str(time) + ", Note_off_c, 0, " + str(int(noteList[i])+46) + ", 0")  
                time+=240
                i=j
            elif(noteList[i] not in "1" and noteList[i] not in "0"):
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
    noteDurations=[]
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
         
            #checks for notes duration. Remember: Since a 1 represents a held note, we need
            # to score those seperately from a repated note.
            duration = 1
            if noteList[i] != 1 and noteList[i+1] == 1:
                for j in range(i+1, len(noteList)-1):
                    if noteList[j] == 1 and noteList[j+1] == 1:
                        duration+=1
                    else:
                        break
                if duration >= 16:
                    fitness += 1
            noteDurations.append(duration)
            


            
        # I considered two different methods for this. One was utilizing sum() function and iterating the list
        # while the other was the much cleaner ptsdev() func from the statistics library. I opted for the
        # cleaner approach. Utilizing pstdev to get a meaningful measurement is something I will improve.

        # using standard deviation to promote a varied note selection 
        noteVaried = math.trunc(statistics.pstdev(noteList))
        if noteVaried < 3:
            fitness+=1

        #checks for a varied note duration
        
                    
        durationVaried = statistics.pstdev(noteDurations)
        if durationVaried < 0.5:
            fitness+= math.trunc(durationVaried*len(noteDurations))
    return fitness


def geneticAlg(gens,length):
    
    #init parent arrays outside of generation iteration so they aren't wiped everytime
    ancestors = []
    breeders = []
    children = []

    

    #fill the first ancestors
    for j in range(100):
        #create a parent melody with defined length and name it by generation and parent
        ancestors.append(genMelody(length,'results/ancestors'+str(j)))
        #score the parent. This isn't a good way to store this data.
        breedScore = fitnessfunc(ancestors[j])
        breeders.append({'name':ancestors[j], 'score':breedScore})
    
    sortedBreeders=sorted(breeders, key = lambda i: i['score'])

    for i in range(gens):

        kid1=[]
        kid2=[]
        tourney=[]
        for breeding in range(50):
            for some in range(5):
                tourney.append(sortedBreeders[random.randint(0,99)])
            tourney = sorted(tourney, key = lambda i: i['score'])

            #open up parent 1
            with open(tourney[0]['name'],'r') as f:
                pRead1 = csv.reader(f, delimiter=',')
                parent1 = []
                for row in pRead1:
                    parent1.append(int(row[0].strip("[']")))

            #open up parent 2
            with open(tourney[1]['name'],'r') as f:
                pRead2 = csv.reader(f, delimiter=',')
                parent2 = []
                for row in pRead2:
                    parent2.append(int(row[0].strip("[']")))

            #crossover to make siblings
            for note in range(length-1):
                coin = random.randint(0,1)
                if coin==1:
                    kid1.append(parent1[note])
                    kid2.append(parent2[note])
                else:
                    kid1.append(parent2[note])
                    kid2.append(parent1[note])

            #mutate
            for gene in range(random.randint(0,20)):
                kid1[random.randint(0,length-2)]=random.randint(0,14)
                kid2[random.randint(0,length-2)]=random.randint(0,14)

            #convert to csv for scoring of both kids
            fName = "results/gen"+str(i+1)+"BreedingSet"+str(breeding+1)+"kid1.csv"
            with open(fName,'w') as f:
                writer = csv.writer(f, delimiter=',')
                for row in kid1:
                    writer.writerow([row]) 
            kidScore = fitnessfunc(fName)
            children.append({'name':fName, 'score':kidScore})

            fName = "results/gen"+str(i+1)+"BreedingSet"+str(breeding+1)+"kid2.csv"
            with open(fName,'w') as f:
                writer = csv.writer(f, delimiter=',')
                for row in kid2:
                    writer.writerow([row]) 
            kidScore = fitnessfunc(fName)
            children.append({'name':fName, 'score':kidScore})
        
        #turn children into sortedBreeders                   
        sortedBreeders = sorted(children, key = lambda i: i['score'])

        #assign best and worst
        if i==0:
            best = sortedBreeders[0]
            worst = sortedBreeders[99]
        elif best['score']>sortedBreeders[0]['score']:
            best = sortedBreeders[0]
        
        if worst['score']<sortedBreeders[99]['score']:
            worst=sortedBreeders[99]
        
        print("Best child of generation "+str(i)+": "+str(sortedBreeders[0]['score']))
        print("Worst child of generation "+str(i)+": "+str(sortedBreeders[99]['score']))

        #clear children for next gen
        children = []

        if i==0:
            outputMelody(best['name'],"test3/firstBest")
            outputMelody(worst['name'],"test3/firstWorst")
        
        if i==(gens/2):
            outputMelody(best['name'],"test3/middleBest")
            outputMelody(worst['name'],"test3/middleWorst")

    outputMelody(best['name'],"test3/finalBest")
    outputMelody(worst['name'],"test3/finalWorst")
    
    print("best: "+ str(best['score'])+ " | worst: "+ str(worst['score']))

# the reason for this length is to get a meaningful fitness measurement. 
# Smaller values resulted in multiple low scoring melodies
geneticAlg(500,1024)
# fitnessfunc(genMelody(1024,"test1"))



