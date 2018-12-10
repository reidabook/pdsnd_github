#!/usr/bin/env python
# coding: utf-8

# # Bikeshare Project
#
# I will use this notebook to help develop my Bikeshare project.

# In[3]:


import time              #used to calculate the time it takes to run the statistic calculations
import calendar as c     #used to pull the day of the week and month names after users input numbers
import pandas as pd      #used to load documents and perform calculations


# In[4]:


#used to map city names to the names of their associated csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington, dc': 'washington.csv' }


# All files must be stored in the same directory as this file.

# In[5]:


#collects the information for the city, month, and day of the week filters from the user
def get_filters():

    #First, collect input from the user.
    #Then check with the user that their input is correct and they wish to continue (continue_check)'''

    city_check = ""
    while city_check != 'Y':
        print("Please select a city from the following list:","\n1 - Chicago", "\n2 - New York City", "\n3 - Washington, DC")
        city = city_match(input("\nInput: ")) #collects the user input

        city_check = continue_check(city) #Checks that the input was correct. Allows the user to continue or start over


   #collects the date information from the user. Allows them to select by month, day of week, both, or all dates
   #then validates that their selection is correct so they can move forward

    date_check = ""
    while date_check != "Y":

        #collects user input for month and day
        print("Would you like to filter the data by:", "\n1 - Month", "\n2 - Day", "\n3 - Both", "\n4 - All Dates")
        month, day = date_match(input("\nInput: "))

        #generates the actual month and weekday names from the inputted integers.
        if day != 0:
            if month != 0:
                month_name = c.month_name[month]
                selected_date = month_name + " & " + c.day_name[day-1]
            else:
                selected_date = c.day_name[day-1]
        elif month != 0:
            month_name = c.month_name[month]
            selected_date = month_name
        else:
            selected_date = "All Dates"

        #passes the month and day of the week names into continue_check to validate that they are accurate with the user
        date_check = continue_check(str(selected_date))

    #print("I am finishing up get_filters", city, month, day,type(city), type(month), type(day))
    return city, month, day


# In[6]:


def city_match(response):

    temp_response = clean_string(response)

    try:
        if temp_response.isalpha(): #check if all char in the string are alphabetic
            city = "incorrect value"

            #checks that the input text is one of the cities
            for key in CITY_DATA.keys():
                if temp_response in key.replace(" ", "").replace(",", ""):
                    city = key

    #if not all letters, check if a number and match to a key in CITY_DATA
        elif temp_response.isdigit():
            temp_response = int(temp_response)
            if temp_response in range(1,4):
                list_temp = list(CITY_DATA.keys()) #creates a temporary list of the cities in CITY_DATA from the keys
                city = list_temp[temp_response - 1] #to account for list starting at 0 while the city options started at 1
            else:
                return print(error_message(response)) #returns error if cannot find result
        else:
            return print(error_message(response)) #return an error message if can't find a match

    except Exception as e:
        return print(error_message(response), e)

    #print("city value returned ", city, type(city))
    return city


# In[7]:


def date_match(response):

    month = 0
    day = 0

    temp_response = clean_string(response)

    try:
        #check if all char in the string are alphabetic, then matches to option based on response value
        if temp_response.isalpha():
            month, day = month_day(temp_response)

        #checks if characters are numbers
        elif temp_response.isdigit():
            temp_response = int(response)
            if temp_response in range(1,5): #validates the the input is a number within the options
                if temp_response == 1:
                    month, day = month_day('month')
                elif temp_response == 2:
                    month, day = month_day('day')
                elif temp_response == 3:
                    month, day = month_day('both')
                elif temp_response == 4:
                    return 0, 0
        else:
            print(error_message(response)) #return an error message if can't find a match

    except Exception as e:
        print(error_message(response), e) #return an error message if can't find a match

    #print("I am finishing up date_match", month, type(month), day, type(day))
    return month, day


def clean_string(input_string):
    return input_string.replace(" ", "").replace(",", "").lower() #normalizes user input

def month_day(response):

    month = 0
    day = 0
    check = False
    month_valid = ""
    day_valid = ""

    if response in "alldates": check=True #if the fourth option was selected, skip over the while loop

    while check == False:

        #asks the user to input a month
        if response == 'month' or response == 'both':
            month = input("Please type your response as an integer (e.g. January = 1): ")

            #validates that the month inputted is a number and aligns with a month value (1-12)
            if month.isdigit():
                month = int(month)
                if 0 < month < 13:
                    month_valid = True #confirms it is a valid input and saves it as a variable
            else:
                month_valid = False

        #asks the user to input a day of the week as an integer
        if response == 'day' or response == 'both':
            day = input("Which day of the week? Please type your response as an integer (e.g. Monday = 1): ")

            #validates that the day is a number and it is between 1-7
            if day.isdigit():
                day = int(day)
                if 0 < day < 8:
                    day_valid = True
            else:
                day_valid = False

        #if the user inputted either the month or day incorrectly, starts the loop over
        if month_valid != False and day_valid != False:
            check = True
        else:
            print("\nPlease enter correct values and try again.\n")

    #print("I am finishing up month_day", month, type(month), day, type(day))
    return month, day


# In[9]:


def error_message(input_text):
    #prints this when there is an error message
    return "\nError: We were unable to find a match for your input of \'{}\'. Please start over and try again.".format(input_text)


# In[10]:


def continue_check(user_selection):
    #asks the user if he/she would like to continue with the inputed value
    if user_selection != None:
        return input("We've received your selection of \'{}\'. Is this correct? (Y/N): ".format(user_selection.title())).upper()


# In[11]:


def load_data(city, month, day):

    filename = CITY_DATA[city]
    df = pd.read_csv(filename, parse_dates=True, infer_datetime_format=True) #loads data for the specified city

    df['Start Time'] = pd.to_datetime(df['Start Time']) #ensure the 'Start_Time' column is in date format

    df['Month'] = df['Start Time'].dt.month #creates a Month column which is an integer
    df['Day of Week'] = df['Start Time'].dt.dayofweek #creates a day of weeks column which is an integer

    #applies a filter to df based on the value of month if value exists
    if month != 0:
        df = df[df['Month'] == month]

    #applies a filter to df based on the value of day if value exists
    if day != 0:
        df = df[df['Day of Week'] == day-1]

    #print("returning df")
    return df


# In[114]:


def show_rawdata(df):
    check = ""
    check = input("Would you like to see the raw data (Y/N)? ").upper()
    lines=5
    while check != "N":
        print(df.head(lines))
        check = input("Would you like to see an additional 5 rows (Y/N)? ").upper()
        print("\n")
        lines+=5


# In[115]:


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')

    print("**Popular times of travel**\n")
    start_time = time.time()
    # display the most common month
    temp_table = df['Month'].value_counts().nlargest(1)   #.mode() would also return the most frequent month, unsure how to provide the count as well though
    mnth_num = int(temp_table.index[0])-1
    frequency_print(temp_table.name, c.month_name[mnth_num].title(),temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df[['Start Time','Month']])

    start_time = time.time()
    # display the most common day of week
    temp_table = df['Day of Week'].value_counts().nlargest(1)
    dow_num = int(temp_table.index[0])
    frequency_print(temp_table.name, c.day_name[dow_num].title(),temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df[['Start Time','Day of Week']])

    start_time = time.time()
    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    temp_table = df['Start Hour'].value_counts().nlargest(1)
    frequency_print(temp_table.name, temp_table.index[0], temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df[['Start Time','Start Hour']])

    start_time = time.time()
    print("\n**Popular stations and trips**\n")
    # display the most common start station
    temp_table = df['Start Station'].value_counts().nlargest(1)
    frequency_print(temp_table.name, temp_table.index[0], temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df['Start Station'])

    start_time = time.time()
    # display the most common end station
    temp_table = df['End Station'].value_counts().nlargest(1)
    frequency_print(temp_table.name, temp_table.index[0], temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df['End Station'])

    start_time = time.time()
    # most common trip from start to end (i.e., most frequent combination of start station and end station)
    df['Trip'] = df['Start Station']+" -> "+df['End Station']
    temp_table = df['Trip'].value_counts().nlargest(1)
    frequency_print(temp_table.name, temp_table.index[0], temp_table.iloc[0]) #repetitive print function
    endtime(start_time)
    show_rawdata(df[['Start Station','End Station']])


    print("\n**Trip durations**\n")
    start_time = time.time()
    #display the total travel time
    secs = df['Trip Duration'].sum()
    print("Total travel time: {}".format(time.strftime("%H hours %M minutes %S seconds", time.gmtime(secs))))
    endtime(start_time)
    show_rawdata(df[['Start Time','End Time','Trip Duration']])

    start_time = time.time()
    #display the average travel time
    secs = df['Trip Duration'].mean()
    print("Average travel time: {}".format(time.strftime("%H hours %M minutes %S seconds", time.gmtime(secs))))
    endtime(start_time)
    show_rawdata(df[['Start Time','End Time','Trip Duration']])

    print("\n**User information**\n")
    start_time = time.time()
    #display the counts of each user type
    print("Counts of each user type: ")
    temp_table = df['User Type'].value_counts().reset_index()
    print(temp_table.to_string(header=None, index=None))
    endtime(start_time)
    show_rawdata(df['User Type'])

    start_time = time.time()
    #display the counts of each gender (only available for NYC and Chicago)
    if city == "new york city" or city == "chicago":
        print("\nCounts of each gender:")
        temp_table = df['Gender'].value_counts().reset_index()
        print(temp_table.to_string(header=None, index=None))
        endtime(start_time)
        show_rawdata(df['Gender'])

        start_time = time.time()
    #display the earliest, most recent, most common year of birth (only available for NYC and Chicago)
        temp_table = df['Birth Year']
        print("\nEarliest birth year: {}".format(int(temp_table.min())))
        print("Most recent birth year: {}".format(int(temp_table.max())))
        temp_table = temp_table.value_counts().nlargest(1)
        frequency_print(temp_table.name, int(temp_table.index[0]), temp_table.iloc[0]) #repetitive print function
        endtime(start_time)
        show_rawdata(df['Birth Year'])

    print('-'*40)


# In[116]:


def endtime(start_time):
    print("\nThis took %s seconds." % (time.time() - start_time))


# In[117]:


def frequency_print(stat_name, result, count_val):
    print("{} with highest frequency: {} ({})".format(stat_name, result, count_val))


# ##### #1 Popular times of travel (i.e., occurs most often in the start time)
# - most common month
# - most common day of week
# - most common hour of day
#
# ##### #2 Popular stations and trip
# - most common start station
# - most common end station
# - most common trip from start to end (i.e., most frequent combination of start station and end station)
#
# ##### #3 Trip duration
# - total travel time
# - average travel time
#
# ##### #4 User info
# - counts of each user type
# - counts of each gender (only available for NYC and Chicago)
# - earliest, most recent, most common year of birth (only available for NYC and Chicago)

# In[118]:


def main():

    print("Hello! Let's explore some US bikeshare data. Let\'s start by applying filters.")

    check = ""
    while check != "N":

        city, month, day = get_filters() #grabs filter values for city, month, and day

        print('\n','-'*40,"\n") #prints a line to break out the interface

        df = load_data(city, month, day) #loads csv file and adds filters

        if df['Start Time'].count() != 0:  #after filters are applied, checks that there are >0 rows in df
            time_stats(df, city)  #runs the stats
            raw_data = input("\nWould you like to see all of the raw data (Y/N)? ").upper()
            if raw_data == "Y":
                lines = int(input("How many lines of data would you like to see? Default is 5. "))
                print(df.head(lines))
            check = input("\nWould you like to start over (Y/N)? ").upper()
        else:
            print("Your filters resulted in a file with no results. Please Try again.\n")

    print("\nThanks!")



# In[119]:


if __name__ == "__main__":
    main()
