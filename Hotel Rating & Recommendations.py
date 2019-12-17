'''
Created on Nov 26, 2019
The program will create a plot showing mean ratings and number of reviews for a 
selection of hotels in a chosen state and cities. Then program will then generate a 
barchart that shows percentage of reviews for the top 3 hotels with highest average ratings.

Program uses Pandas & Matlabplot packages.

@author: Moheshwar Palani
'''

import matplotlib as mlp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import os.path

CITY = 'city'
PROVINCE = 'province'
NAME = 'name'
REVIEWS_RATING = 'reviews_rating'

def pickStateAndCities(hotel):
    ''' will be used to get user input about state and cities to generate the hotels list 
    Parameters: 
        hotel - A dataframe with information on hotel location 
    Returns:
           user chosen state and all cities in it 
    '''
    
    userstate = 'nothing'
     
    while(userstate == 'nothing'):
        userstate = input('Please enter state, e.g. MA: ')
        if (userstate in hotel[PROVINCE].values) == False:
            print('We have no data on hotels in',userstate)
            userstate = 'nothing'
            
    cityoption = hotel[hotel[PROVINCE] == userstate][CITY]
    
    cityoption = pd.Series(cityoption.unique())
    cityoption = cityoption.sort_values()
    cityoption.index = np.arange(1,len(cityoption)+1)
    cityoption.rename(inplace=True)
    
    print(cityoption)
    print()
    
    cityoption.rename(CITY,inplace=True)
    
    citychecker = 'notokay'
    while (citychecker != 'okay'):
        citynum = pd.Series(input('Select cities from above list by entering up to four indices on the same line:').split())
        
        citynum = citynum.astype('int32')
        citynum.rename('citynum',inplace=True)
        
        comparecity = pd.merge(cityoption,citynum,how='inner',left_index=True,right_on = 'citynum')
        
        if len(comparecity) > 4:
            print('You selected', len(citynum),'items, must select up to four')
            
        elif len(comparecity) != len(citynum):
            print('Selection must range from 1 to',len(cityoption))
            
        elif  len(comparecity) == len(citynum):
            citychecker = 'okay'
            
    comparecity[CITY].reindex(citynum.values)
    print('You have selected the following cities:')
    usercity = pd.DataFrame(cityoption[cityoption.index.isin(citynum.values)])
      
    print(usercity)
    print()
    
    return userstate,usercity
    

def selectHotelReviews(hotel,review,usercity,userstate):
    '''  to select and return reviews for the hotels in the selected cities 
    Parameters: 
        hotel - A dataframe with information on hotel location 
        review - a dataframe with records of customer reviews of their stays in the hotels
        usercity - all the cities selected by user
        userstate - state selected by user for generating the hotel list
    Returns:
           userhotel - the list of hotels in the location selected by user
           avgReview - dataframe with average rating and review count for the hotels in the selected location 
    '''
        
    userhotel = hotel[(hotel[CITY].isin(usercity[CITY])) & (hotel[PROVINCE] == userstate)]
    
    userhotel.sort_values(by=CITY,inplace=True)
    userhotel.index = np.arange(0,len(userhotel))
    print('Displaying rating information for the following hotels:')
    
    print(userhotel[[NAME,CITY,PROVINCE]])
    
    #calculating data for the reviewrating plot
    reviewSelectedHotel = pd.merge(review,userhotel,on=NAME)
     
    avgReview = reviewSelectedHotel.groupby(by=NAME).mean()[REVIEWS_RATING]
    
    reviewcount = reviewSelectedHotel.groupby(by=NAME).count()[REVIEWS_RATING]
    
    avgReview = pd.merge(avgReview,reviewcount,on='name')
    avgReview.columns = ['Avg_ratings','reviewcount']
    
    avgReview = pd.merge(avgReview,userhotel[[NAME,CITY]],on = NAME)
    
    avgReview.sort_values(by='Avg_ratings',inplace=True,ascending=False)
    avgReview.reset_index(drop=True,inplace=True)
    
    return userhotel, avgReview


def  reviewsRatingsPlot(userhotel,avgReview):
    '''  generates with a plot for each of the hotels in the selected cities, 
        this plot visualizes the number of reviews as a
        coordinate on the x axis and the average rating, as a coordinate on the y axis.  
    Parameters: 
        userhotel - the list of hotels in the location selected by user
        avgReview - dataframe with average rating and review count for the hotels in the selected location 
    Returns:
           the function returns nothing
    '''
    
    for pro in userhotel[CITY].unique():   
        plt.plot(avgReview[avgReview[CITY] == pro].reviewcount,avgReview[avgReview[CITY] == pro].Avg_ratings,label=pro,marker='o',linestyle='')
        
    for ele in range(len(userhotel[NAME])):
        plt.annotate(avgReview[NAME][ele],(avgReview.reviewcount[ele],avgReview.Avg_ratings[ele]))
    
    plt.xlabel('Number of reviews')
    plt.ylabel('Average Rating')
    plt.title('Hotel ratings and number of reviews.')
    plt.xticks(range(0,avgReview.reviewcount.max()+50,50))
    plt.yticks(range(0,7,1))
    plt.legend()
        
    return avgReview
    

def ratingPercentageBarchart(avgReview,review,userstate):
    '''   Barchart showing what percentage of all reviews have the specific rating (1 through 5). 
        This chart is generated for each of the top three hotels.
    Parameters:  
        avgReview - dataframe with average rating and review count for the hotels in the selected location
        review - a dataframe with records of customer reviews of their stays in the hotels
        userstate - state selected by user for generating the hotel list 
    Returns:
           the function returns nothing
    '''
    review['ceiledRating'] = review[REVIEWS_RATING].apply(np.ceil) 
    
    for eachhotel in range(3):
        tempreviewdata = review[review[NAME] == avgReview[NAME][eachhotel]].groupby(by='ceiledRating').count()
        tempreviewdata['percentages'] = ((tempreviewdata[REVIEWS_RATING]/tempreviewdata[REVIEWS_RATING].sum()).round(3))*100
        
        tempreviewdata = tempreviewdata.reindex([1,2,3,4,5],fill_value = 0)
        
        plt.figure()
        labeltoprint = tempreviewdata['percentages'].round(3).astype(str).str.cat(others=['','','','',''],sep='%')
                
        plt.bar(x=tempreviewdata.index, height=tempreviewdata['percentages'],align = 'edge')
        
        for ele in range(1,len(labeltoprint)+1):
            plt.annotate(labeltoprint[ele],(ele,tempreviewdata['percentages'][ele]))
             
        reviewtitle = 'Percentage of reviews with ratings 1 - 5 out of '+str(tempreviewdata[REVIEWS_RATING].sum())+' reviews \n for '+str(avgReview[NAME][eachhotel])+' in '+str(avgReview[CITY][eachhotel])+\
                    ', '+str(userstate)
        plt.xlabel('Rating value (1-5)')
        plt.ylabel('% of reviews with rating')
        plt.title(reviewtitle)
        plt.xticks(tempreviewdata.index)
        plt.yticks(range(0,120,20))

def main():
    folder,hotelfile,reviewfile = input('Please enter names of the subfolder and files:').split()
        
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.width', 1000) 
         
    hotel = pd.read_csv((os.path.join(os.getcwd(),folder,hotelfile)))
    
    review = pd.read_csv((os.path.join(os.getcwd(),folder,reviewfile)))
    
    userstate,usercity = pickStateAndCities(hotel)
     
    userhotel, avgReview = selectHotelReviews(hotel,review,usercity,userstate)
    
    reviewsRatingsPlot(userhotel,avgReview)
    
    ratingPercentageBarchart(avgReview,review,userstate)
    
    plt.show()
    
    print('Exiting...')

main()