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
        for _ in range(notes):
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
                time+=480
               
            elif(noteList[i] not in "1" and noteList[i] not in "0"):
                midi.append("1, " + str(time) + ", Note_on_c, 0, " + str(int(noteList[i])+46) + ", 127")
                time+=480

            j = i+1
            if(j<(len(noteList)-1) and (noteList[j] in "1" or noteList[j] in "0")):
                while(noteList[j] in "1" and j<(len(noteList)-1)):
                    time+=480
                    j+=1
                midi.append("1, " + str(time) + ", Note_off_c, 0, " + str(int(noteList[i])+46) + ", 0")  
                
                i=j
            elif(noteList[i] not in "1" and noteList[i] not in "0"):
                midi.append("1, " + str(time) + ", Note_off_c, 0, " + str(int(noteList[i])+46) + ", 0")  
                
                
        midi.append('1, '+str(time)+ ', End_track')        
        midi.append('0, 0, End_of_file')
        writer.writerow(midi)
        
        
        midi_obj = pm.csv_to_midi(midi)

        with open(out+".mid","wb") as out_file:
            midi_writer = pm.FileWriter(out_file)
            midi_writer.write(midi_obj)
    
def fitnessfunc(file,scale):
    noteDurations=[]
    badNote=0
    totalDuration = 0    
   

    with open(file,'r') as f:
        fitness = 0
        read = csv.reader(f, delimiter=',')
        noteList = []
        for row in read:
            if row == []:
                continue
            noteList.append(int(row[0].strip("[']")))
        f.close()

        # assess phrase for rests
        for k in range(0,len(noteList)-1,10):
            phraseRest=0
            j=0
            half1=0
            half2=0
            for j in range(0,10):
                if k+j <len(noteList)-1:
                    if noteList[k+j]==0:
                        phraseRest+=1 
                
                # call and response assessment

                for note1 in range(k,k+4):
                    if note1+1<len(noteList):
                        half1+=noteList[note1]-noteList[note1+1]
                for note2 in range(k+4,k+9):
                    if note2+1<len(noteList):
                        half2+=noteList[note2]-noteList[note2+1]
                if half1<0 and half2<0:
                    fitness+=5
                if half1>0 and half2>0:
                    fitness+=5

            if phraseRest>3:
                fitness+=6


        for i in range(len(noteList)-2):
            found = False
            duration = 1

            # checks for repeated notes
            if i+3 <(len(noteList)-1):
                if noteList[i] == noteList[i+1] == noteList[i+2] == noteList[i+3] != 1:
                    fitness+=5

         
            # checks for notes duration. Remember: Since a 1 represents a held note, we need
            # to score those seperately from a repated note.
            duration = 1
            totalDuration = 0
            if noteList[i] != 1 and noteList[i+1] == 1:
                for j in range(i+1, len(noteList)-1):
                    if noteList[j] == 1 and noteList[j+1] == 1:
                        duration+=1
                        totalDuration+=1
                    else:
                        break
                if duration >= 8:
                    fitness += 10
            noteDurations.append(duration)
            
            # checks for next note in scales
            for index in range(len(scale)-1):
                if noteList[i]==scale[index]:
                    found = True
            if noteList[i]!=0 and noteList[i] != 1 and found == False:
                fitness+=5
                    
            

        if totalDuration<len(noteList)*.3:
            fitness+=5*(1+(2-totalDuration))

        #check how many bad notes
        if badNote>len(noteList)*.1:
            fitness+=badNote
        

        # assess the amount of rests
        rests = noteList.count(0)
        if rests>len(noteList)*.25 or rests<len(noteList)*.15:
            if rests>len(noteList)*.25:
                fitness+=rests-(len(noteList)*.25)
            elif rests<len(noteList)*.1:
                fitness+=(len(noteList)*.1)-rests

        # using standard deviation to promote a varied note selection 
        noteVaried = math.trunc(statistics.pstdev(noteList))
        if noteVaried < 4:
            fitness+=5*(1+(2-noteVaried))

        #checks for a varied note duration
        durationVaried = math.trunc(statistics.pstdev(noteDurations))
        if durationVaried < 4:
            fitness+= 5*(1+(3-durationVaried))
    return fitness

def scaleSelect(val):
    #scales in the key of c
    switch = {
        0: [2,4,5,7,8,10,11,13,14], #Dominant Diminished Scale
        1: [2,4,6,8,10,12,14],      #Major Scale
        2: [2,4,5,7,9,11,12,14],    #Dorian Minor Scale
        3: [2,3,5,7,9,10,12,14],    #Phrygian Minor Scale
        4: [2,4,6,8,9,10,11,13,14], #Lydian Major Scale
        5: [2,4,6,7,9,11,12,14],    #Mixolydian Scale
        6: [2,4,5,7,9,10,12,14],    #Aeolian Scale
        7: [2,3,5,7,8,10,12,14],    #Locrian Scale
        8: [2,4,5,7,8,10,11,13,14], #Whole-Half Diminished Scale
        9: [3,4,6,7,9,11,13],       #Altered Scale
        10:[2,4,6,8,10,12,14],      #Whole-Tone Scale
        11:[2,5,7,8,9,12,14],       #Minor Pentatonic Scale
        12:[2,4,6,8,9,11,12,14],    #Lydian Dominant Scale
        13:[2,4,6,7,9,11,13,14],    #Major Bebop Scale
        14:[2,4,6,7,9,10,11,13,14], #Minor Bebop Scale
        15:[2,4,6,7,9,11,12,13,14]  #Mixolydian Bebop Scale
    }
    print("Selected scale: " +str(switch.get(val)))
    return switch.get(val)

#gens is the amount of generations to evolve through and length is the number of notes
#to be generated in the melody.
def geneticAlg(gens,length):
    #init parent arrays outside of generation iteration so they aren't wiped everytime
    ancestors = []
    breeders = []
    children = []

    # set scale in key of C
    scale = scaleSelect(random.randint(0,15))
    

    #fill the first ancestors
    for j in range(100):
        #create a parent melody with defined length and name it by generation and parent
        ancestors.append(genMelody(length,'/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/results/ancestors'+str(j)))
        #score the parent.
        breedScore = fitnessfunc(ancestors[j],scale)
        breeders.append({'name':ancestors[j], 'score':breedScore})
    
    sortedBreeders=sorted(breeders, key = lambda i: i['score'])

    for i in range(gens):

        tourney=[]
        for breeding in range(50):
            for _ in range(10):
                tourney.append(sortedBreeders[random.randint(0,99)])
            tourney = sorted(tourney, key = lambda i: i['score'])

            #open up parent 1
            with open(tourney[0]['name'],'r') as f:
                pRead1 = csv.reader(f, delimiter=',')
                parent1 = []
                for row in pRead1:
                    if row==[]:
                        continue
                    parent1.append(int(row[0].strip("[']")))

            #open up parent 2
            with open(tourney[1]['name'],'r') as f:
                pRead2 = csv.reader(f, delimiter=',')
                parent2 = []
                for row in pRead2:
                    if row==[]:
                        continue
                    parent2.append(int(row[0].strip("[']")))

            kid1=[]
            kid2=[]
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
            for _ in range(random.randint(0,20)):
                kid1[random.randint(0,length-2)]=random.randint(0,14)
                kid2[random.randint(0,length-2)]=random.randint(0,14)

            #convert to csv for scoring of both kids
            fName = "/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/results/gen"+str(i+1)+"BreedingSet"+str(breeding+1)+"kid1.csv"
            with open(fName,'w') as f:
                writer = csv.writer(f, delimiter=',')
                for row in kid1:
                    writer.writerow([row]) 
            kidScore = fitnessfunc(fName,scale)
            children.append({'name':fName, 'score':kidScore})

            fName = "/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/results/gen"+str(i+1)+"BreedingSet"+str(breeding+1)+"kid2.csv"
            with open(fName,'w') as f:
                writer = csv.writer(f, delimiter=',')
                for row in kid2:
                    writer.writerow([row]) 
            kidScore = fitnessfunc(fName,scale)
            children.append({'name':fName, 'score':kidScore})
        
        children[len(children)-2] = sortedBreeders[0]
        children[len(children)-1] = sortedBreeders[1]
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
        
        print("Best child of generation "+str(i+1)+": "+str(sortedBreeders[0]['score']))
        # print("Worst child of generation "+str(i+1)+": "+str(sortedBreeders[99]['score']))

        #clear children for next gen
        children = []

        if i==0:
            outputMelody(best['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/firstBest")
            outputMelody(worst['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/firstWorst")
        
        if i==(gens/2):
            outputMelody(best['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/middleBest")
            outputMelody(worst['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/middleWorst")

    outputMelody(best['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/finalBest")
    outputMelody(worst['name'],"/Users/thompson/Desktop/Spring21/SeniorProject/SeniorProject-master/test7/finalWorst")
    
    print("results from "+ str(gens) +" generations of melodies size "+ str(length))
    print("best: "+ str(best['score'])+ " | worst: "+ str(worst['score']))

# run it
geneticAlg(500,1024)
# fitnessfunc(genMelody(1024,"test"))










