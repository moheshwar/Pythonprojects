'''
Created on Nov 15, 2019

@author: Moheshwar Palani
'''
'''
This program generates a genre wise movie recommendation for a movie using 
data from IMDB website.
Program uses Pandas & Numpy package for data processing
'''

import pandas as pd
import numpy as np
import os
import os.path

def findClosestCritics(critic,personal):
    ''' function will be used to identify three critics, whose recommendations
        are closest to the persons recommendations. 
    Parameters: 
        critic -  DataFrame containing data about critics ratings
        personal - DataFrame containing data about personal ratings
    Returns:
           function returns a list of three critics, whose ratings of movies are most 
           similar to those provided in the personal ratings data, based on Euclidean distance
    '''
    
    euclidean = pd.Series(0,index=critic.columns)
    
    for cri_num in range(1,len(critic.columns)):
        temp = pd.merge(personal,critic.iloc[:,cri_num],how = 'inner',left_index=True,right_index=True)
        
        temp['DiffSq'] = (temp.iloc[:,1] - temp.iloc[:,2])**2
    
        euclidean.loc[critic.columns[cri_num]] = np.sqrt(temp['DiffSq'].sum())
            
    euclidean.sort_values(inplace=True)
        
    return list(euclidean.index[1:4])    
        

def recommendMovies(critic,personal,CriticNames,movies):
    ''' will be used to generate movie recommendations based on
        ratings by the chosen critics. 
    Parameters: 
        critic -  DataFrame containing data about critics ratings
        personal - DataFrame containing data about personal ratings
        CriticNames -  the list of three critics most similar to the person returned from
                        function findClosestCritics()
        movies - DataFrame containing data about movies
    Returns:
           function returns DataFrame with the top-rated unwatched movies in each genre category, 
           based on the average of the three critics ratings. 
    '''
    
    NotSeen = critic[~critic.index.isin(personal.index)]
    
    moviesreco = pd.DataFrame(columns = movies.columns)
    
    NotSeen = NotSeen[CriticNames]
    
    NotSeen['AvgRating'] = NotSeen[CriticNames].mean(axis=1)
    
    MoviesWithRating = pd.merge(NotSeen['AvgRating'],movies,how='inner',left_index=True,right_index=True)
    
    genregroup = MoviesWithRating.groupby(by='Genre1',axis=0)
       
    HighestRatingbyGenre = genregroup.max()['AvgRating']
    
    for key,g in genregroup:
        
        testcase = MoviesWithRating[(MoviesWithRating['Genre1'] == key) & (MoviesWithRating['AvgRating'] >= HighestRatingbyGenre[key])]
    
        moviesreco = pd.concat([moviesreco,testcase],axis=0,sort=True)
        
    return moviesreco

def printRecommendations(moviesreco,username):
    ''' will be used to generate movie recommendations based on
        ratings by the chosen critics. 
    Parameters: 
        moviesreco - DataFrame containing data about recommended movies
        username - the name of the person, for whom the recommendation is made 
    Returns:
           function returns nothing but print output in the required format 
    '''
    print()
    print('Recommendations for ',username,':',sep='')
    maxlen = moviesreco.index.str.len().max()
    
    for row in range(len(moviesreco.index)):
    
        printline =str('"'+moviesreco.Title[row]+'"').ljust(maxlen+3)+' ('+str(moviesreco.Genre1[row])+')'+', rating: '+\
              str(round(moviesreco.AvgRating[row],2)) +', ' +  str(moviesreco.Year[row])
            
        if pd.isnull(moviesreco.Runtime[row]) == False:
            
            printline = printline + ', runs ' + str(moviesreco.Runtime[row])

        print(printline)
        
def main():
    '''function used to get user input like folder name and other files names
    parameter: Nil
    Returns: Nil
    '''
    
    folder,moviesfile,criticfile,personalfile = input('Please enter the name of the folder with files, the name of movies file,\
the name of critics file, the name of personal ratings file, separated by spaces:').split()
    
    print()
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.width', 1000) 
         
    movies = pd.read_csv((os.path.join(os.getcwd(),folder,moviesfile)),encoding = 'unicode_escape')
    movies.set_index('Title',drop=False,inplace=True)
    
    critic = pd.read_csv((os.path.join(os.getcwd(),folder,criticfile)))
    critic.set_index('Title',drop=False,inplace=True)
    
    personal = pd.read_csv((os.path.join(os.getcwd(),folder,personalfile)))
    personal.set_index('Title',drop=False,inplace=True)
                
    CriticNames = findClosestCritics(critic,personal)
    
    print('The following critics had reviews closest to the person\'s:')
    for i in range(len(CriticNames)-1): print(CriticNames[i],end=', ')
    print(CriticNames[-1])
    
    moviesreco = recommendMovies(critic,personal,CriticNames,movies)
    
    printRecommendations(moviesreco,personal.columns[1])
    

main()