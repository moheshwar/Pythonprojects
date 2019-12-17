'''
Created on Oct 25, 2019

@author: Moheshwar Palani
'''
'''
This program process multiple files and text documents 
to generate course requirements and then list the eligible students for
a particular course.
'''

import os
import os.path
def processProgramFile(filepath):
    '''Function used to read information about different programs and store 
        it as an dictionary for retrieval.
    Parameters: 
        filepath - a single parameter of type str, providing the path to a program description file
    Returns:
         a tuple, consisting of the program name and the created dictionary
    '''
    programdict={}
    with open(filepath,'r') as programfile:
        programName = programfile.readline()
        
        for line in programfile:
            linelst=line.split(maxsplit=1)
            if linelst[1].strip().endswith('.'):
                programdict[linelst[0]]=linelst[1].strip()
            else:
                programdict[linelst[0]]=linelst[1].strip()+'.'
        return programName,programdict

def processPrereqsFile(prereqpath):
    ''' used to read information about the prerequisites structure 
        and store it as dictionary for retrieval
    Parameters: 
        prereqpath - a single parameter of type str, providing the path to a file defining prerequisites.
    Returns:
          returns the constructed dictionary of prerequisites with the main course as keys 
          and prereq course as tuple
    '''
    with open(prereqpath,'r') as prereqfile:
        prereqdict={}
        for line in prereqfile:
            linelst=line.split(':',1)
            courselst=linelst[1].split()
            prereqdict[linelst[0]]= tuple(courselst)
    
    return prereqdict        

def processClassFiles(classfolder):
    ''' funtion will combine the data about enrollments into courses from multiple files 
        into a single dictionary organized by course number
    Parameters: 
        classfolder - defining the subfolder with the class list files containing the enrolled student details
    Returns:
          returns the constructed dictionary of students enrolled in each class
    '''
    
    Studentsinclass={}
    folderContentslist=os.listdir(os.path.join(os.getcwd(),classfolder))
    
    for filename in folderContentslist:
        #checking if class file
        with open(os.path.join(os.getcwd(),classfolder,filename)) as currentfile:
            
            checkletter = currentfile.read(1)
            coursecode = currentfile.read(4)
            currentfile.readline()
            #processing the class file
            if checkletter =='c' and coursecode.isdigit():
                #creating new key when course not in the dictionary
                if coursecode not in Studentsinclass: 
                    Studentsinclass[coursecode]=set()
                    
                for line in currentfile:                    
                    linelst=line.split()
                    (Studentsinclass.get(coursecode)).add(linelst[0]) 
                    
    return Studentsinclass              

def initFromFiles(folder):
    ''' function will create data structures with the information 
        that is currently available in files by calling the required function
    Parameters: 
        folder -  a single parameter, defining the subfolder with the files
    Returns:
           return a tuple with the constructed dictionaries for program courses, 
           class lists and prerequisites.
    '''
    #calling functions to get program details in the file
    programName1,programCourse1dict =processProgramFile(os.path.join(os.getcwd(),folder,'program1.txt'))

    programName2,programCourse2dict =processProgramFile(os.path.join(os.getcwd(),folder,'program2.txt'))
    
    #creating a common dictionary with courses in all programs
    programdict=programCourse1dict
    
    for key in programCourse2dict.keys():
        if key not in programdict:
            programdict[key]=programCourse2dict[key]
            
    #calling prereq function to get prereq details        
    prereqdict=processPrereqsFile(os.path.join(os.getcwd(),folder,'prereqs.txt'))
    
    #calling function to get student details in different course
    classdict=processClassFiles(folder)
    
    return programdict,classdict,prereqdict

def estimateClass(coursecode,programdict,classdict,prereqdict):
    ''' function used to find a list of eligible students for a given class 
    Parameters: 
        coursecode - User inputed coursecode for which eligibile student list to be populated
        programdict - dictionary of combined list of classes offered in different programs
        classdict -  dictionary of student enrolled in a class with coursecode as key 
        prereqdict - dictionary of prerequisite for course
    Returns:
           return a tuple with the constructed dictionaries for program courses, 
           class lists and prerequisites.
    '''
    eligiblestudents=set()
    
    if coursecode in programdict.keys():
        #creating all student list
        for values in classdict.values():
            eligiblestudents = eligiblestudents.union(values)
        
        #checking if already taken the course and eliminating those students
        eligiblestudents = eligiblestudents.difference(classdict[coursecode])
        
        #checking prereq qualification and making the final list of eligible students
        
        if coursecode in prereqdict.keys():
            for prereq in prereqdict[coursecode]:
                eligiblestudents = eligiblestudents.intersection(classdict[prereq])
        
        return list(eligiblestudents)
        
        
    else:
        return list(set())

def main():
    '''function used to get user input like folder name and coursecode
    parameter: Nil
    Returns: Nil
    '''
    #user inputs for the corresponding folder
    folder=input('Please enter the name of the subfolder with files:')
    
    programdict,classdict,prereqdict= initFromFiles(folder)
    
    #recursive input for coursecode and printing output
    coursecode=0
    while(coursecode != ''):
            coursecode=input('Enter course number or press enter to stop:')
            if coursecode.isdigit():
                eligiblestudentslst=estimateClass(coursecode,programdict,classdict,prereqdict)
                if coursecode in programdict.keys():
                    print('There are', len(eligiblestudentslst),'students who could take course',coursecode,programdict[coursecode])
                else:
                    print('There are', len(eligiblestudentslst),'students who could take course',coursecode,'None')
                    
                
        
        
main()
        