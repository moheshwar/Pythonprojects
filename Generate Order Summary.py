'''
Created on Oct 2, 2019

@author: Moheshwar Palani
'''
'''
The program generates an time wise order summary for a coffee shop
This includes text processing and calculations
'''

import orderlog
ORDERS = orderlog.orderlst

OPEN=360 #Store opening time in minutes
CLOSE=1440 #Store closing time in minutes

def labelString(int_num,OPEN,interval):
    '''Function produces a string of the required time interval like '6:00 - 6:59'
    Parameters: 
        int_num - interval number of the the time period in the required output
        OPEN - Store opening time in minutes calculated from midnight
        interval - length of the time interval for each line item in the output
    Returns:
        a string defining the start and end time of the interval, as shown above
    '''
    
    interval_count = int((CLOSE-OPEN)/interval)
    interval_duration = (CLOSE-OPEN)/interval_count
    starttime=int(OPEN+(int_num*interval_duration))
    endtime=int(starttime+interval_duration)
    starttime_hour = starttime//60
    starttime_min = starttime%60
    endtime_hour = (endtime-1)//60
    endtime_min = (endtime-1)%60
    s=str(starttime_hour)+':'+str(starttime_min).zfill(2)+' - '+str(endtime_hour)+':'+str(endtime_min).zfill(2)
    return s 

def composeOrderMatrix(days=31, interval=60):
    '''Creates a two-dimensional list, representing the order summary matrix.
        With the days wise order recieved in the each time interval as inputed by user.
    Parameters:
        days - number of days for which the order summary to be created. Default value is 31.
        interval - length of the time interval for each line item in the output. Default value is 60.
    Returns:
        a two-dimensional list, representing the order summary matrix
    '''
    #creating a empty matrix
    interval_count=int((CLOSE-OPEN)/interval)
    matrix = [[0 for i in range(days)] for j in range(interval_count)]
    del ORDERS[0]
    
    #Counting number of order day wise & time interval wise
    for ordernum in ORDERS:
        date,time=ordernum[0].split()
        year,month,day = date.split('-')
        hours,mins,sec = time.split(':')
        ordersum=0
        if int(day)<=days:
            ordertime = (int(hours)*60)+int(mins)+(int(sec)/60)
            orderint = [int(i) for i in ordernum[3:]]
            
            interval_num = (ordertime-OPEN)//interval
            matrix[int(interval_num)][int(day)-1]+=1 
             
    return matrix

def printOrderSummaryMatrix(matrix,interval=60):
    '''The function should display the content of the matrix as shown 
        in the interaction, with the exact formatting.
    Parameters:
        matrix - a two dimensional matrix to be printed in the exact format as required
        interval - length of the time interval for each line item in the output.
    Returs:
        The function does not return anything
    '''
    #Finding max rowlen for printing in format
    rowlen=[16 for row in range(len(matrix))]
    for i in range(len(matrix)):#no of rows
        for j in range(len(matrix[i])):# no of columns
            rowlen[i] += len(str(matrix[i][j]))
            
    maxrowlen = max(rowlen) 
    
    #Finding max element length in each row
    maxElementLen = [0 for row in range(len(matrix[0]))]
    for i in range(len(matrix[0])):
        maxElementLen[i] = len(str(matrix[0][i]))
        for j in range(len(matrix)):
            if maxElementLen[i] < len(str(matrix[j][i])):
                maxElementLen[i] = len(str(matrix[j][i]))
               
    print(('ORDER SUMMARY').center(16+sum(maxElementLen)))
    print(('TIME \ DAY').center(16),'|',end='')
    
    for i in range(len(matrix[0])): print(str(i+1).rjust(maxElementLen[i]),end=' ')
    print()    
    for i in range(18+int(1.5*sum(maxElementLen))): print('-',sep='',end='')
    print()
      
    #Printing the values
    for i in range(len(matrix)):
        print((labelString(i,OPEN,interval)).rjust(16),'|',end='')
        for j in range(len(matrix[i])):
            print(str(matrix[i][j]).rjust(maxElementLen[j]),end=' ')
        print()
        
        
def printHistogram(matrix,histogram_day,interval=60):
    '''The function displays a histogram time interval wise for the day as inputed by the user.
        The histogram visualizes the numbers from the appropriate column of the matrix using * symbols.
    Parameters:
        matrix - a two dimensional matrix containing the day wise order summary
        histogram_day - the day inputed by the user for displaying the histogram
        interval - length of the time interval for each line item in the output
    Returns:
        The function does not return anything
    '''
    
    maxrowlen = 16+max(i[histogram_day] for i in matrix)
    
    header='NUMBER OF ORDERS PER '+str(interval)+' min FOR DAY '+str(histogram_day+1)
    print(header.center(maxrowlen))
    interval_count=int((CLOSE-OPEN)/interval)
    
    #Printing * corresponding to the order count
    for i in range(interval_count):
        print((labelString(i,OPEN,interval)).rjust(16),'|',end='')
        for j in range(matrix[i][histogram_day]):print('*',end='')
        print()  
    
def main():
    '''function used to start the program flow, read user input and call other methods as needed
    Parameters: Nil
    Returns: Nil
    '''
    #data input
    days=eval(input('How many days would you like to include?'))
    interval=eval(input('Please specify the length of the time interval in minutes:'))
    
    
    #checking input data and calling functions accordingly
    if days <= 0 or days > 31: 
        
        if interval < 0 or interval > 1080: 
            matrix=composeOrderMatrix()
            printOrderSummaryMatrix(matrix)
                
        else:
            matrix=composeOrderMatrix(interval=interval)
            printOrderSummaryMatrix(matrix, interval)
        
    if 0 < days <= 31:    
        if interval < 0 or interval > 1080:
            matrix=composeOrderMatrix(days)
            printOrderSummaryMatrix(matrix)
        
        else:        
            matrix=composeOrderMatrix(days, interval)
            printOrderSummaryMatrix(matrix, interval)
        

    #User inputs for histogram and calling functions
    histogram_day=0
    if days <= 0 or days > 31: days = 31
    while(histogram_day == 0):
        histogram_day = eval(input('Enter day number from 1 to '+str(days)+' to see a histogram, or -1 to exit:'))
        if 0 < histogram_day <= days:
            if 0 < interval <= 1080:
                printHistogram(matrix,histogram_day-1,interval)  
            else:
                printHistogram(matrix,histogram_day-1)
            
            histogram_day = 0
            
        elif histogram_day < -1 or histogram_day > days:
            histogram_day = 0
            
    print('Bye!')
            

main()

