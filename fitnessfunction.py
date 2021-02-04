import py_midicsv as pm
from tokenize import tokenize

def getFit(str):

        # iterates through the csv file. We shave off the header data
        # so we only have to parse through actual notes. The header
        # data has no real value in scope.
        
        #list to hold lists of note data
        melody=[]

        #loop to parse through csv of notes
        for line in str[2:len(str)-2]:
            noteData = []
            
            #index for pulling note data
            i=0
            data = line.split(',')
            
            #actual note number
            note = data[i+4]
            noteData.append(note)
            
            #0 is note off and 58 is note on
            event = data[i+5].rstrip()
            noteData.append(event)
            
            #time of event
            time = data[i+1]
            noteData.append(time)
            
            #add note data to overall melody to access later for fitness
            melody.append(noteData)
            
            #clears list for next iteration
            noteData =[]
        # print(melody)
        
        #Actual fitness grading. Lower is better.
        fitness = 0
        for i, note in enumerate(melody):

            #bounds to avoid looking for notes that dont exist.
            if i+4 < len(melody):
                #check for notes repeated 3 times. We dont want that
                if melody[i][0]==melody[i+2][0] and melody[i+2][0]==melody[i+4][0]:
                    fitness+=1
                    print('fitness increased')

            # checks for to many rests. We're not making the album of silence. 
            # Currenlty checks for rest longer than an 8th
            if i+2 < len(melody) and melody[i][1] == ' 0':
                if int(melody[i+2][2])-int(melody[i][2]) > 480:
                    print(melody[i+2] + melody[i])
                    fitness+= 1
                    print(fitness)
        print('<-----------------fitness measured: lower is better----------------->')        
        print(fitness)

            #checks if note movements are appropriate

#run fitness    
csv_string = pm.midi_to_csv("../midiFiles/clips/basicTest.mid")
getFit(csv_string)

