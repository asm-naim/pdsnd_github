import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' }

city_lists = ['chicago', 'new york city', 'washington']
filter_lists = ['month', 'day', 'none']
month_lists = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_lists = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
see_raw_data_lists = ["yes", "no"]

#helper function
def options(array):
    title_array = [x.title() for x in array]
    options = "\n\t".join(title_array)
    return "\n\t" + options

#helper function
def error_text(filter, questionfilter):
    return input("\nOpps! You have enter the wrong option, please try again and select from the given {} options.{}".format(filter, questionfilter)).lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington).
    questioncity = "\nPlease enter the city you want to analyze : {} \n".format(options(city_lists))
    city = input(questioncity).lower()
    while city not in city_lists:
        city = error_text("cities", questioncity)

    #get user input for filter type (month, week, all)
    questionfilter = "\nPlease enter the filter you want to apply : {} \n".format(options(filter_lists))
    choice = input(questionfilter).lower()
    while choice not in filter_lists:
        choice = error_text('filters', questionfilter)
    
    #get user input for month (all, january, february, ... , june)
    if(choice == 'month'):
        questionmonth ="\nPlease enter the month you want to analyze.  If you do not want a month filter enter 'all'.  \nMonths options are as below : {} \n".format(options(month_lists))
        month = input(questionmonth).lower()
        while month not in month_lists:
            month = error_text("months", questionmonth)
        day = 'all'

    #get user input for day of week (all, monday, tuesday, ... sunday)
    elif(choice == 'day'):
        questionday ="\nPlease enter the day you want to analyze. If you do not want a day filter enter 'all'. \nDays options : {} \n".format(options(day_lists))
        month = 'all'
        day = input(questionday).lower()
        while day not in day_lists:
            day = error_text("days", questionday)

    elif(choice == "none"):
        month = 'all'
        day = 'all'    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read data from csv based on selected city
    df = pd.read_csv(CITY_DATA[city])
    
    #convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #create new columns by extracting month and day from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.weekday_name #day_of_week

    #filter by month, if month filter is selected
    if (month != 'all' and day == 'all'):
        months = month_lists
        month = months.index(month) + 1
        # Filter by month and overwrite the existing dataframe
        df = df[df['month'] == month]

    #filter by week, if week filter is selected
    elif  (month == 'all' and day != 'all'): 
        # Filter by week and overwrite the existing dataframe
        df = df[df['day_name'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #extract month from start time column to create month column 
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    most_common_month = df['month'].mode()[0]
    months = month_lists[:6]
    month_name = months[most_common_month - 1].title()
    print('The most common month of the year: \n', month_name) 

    #display the most common day of week
    most_common_day = df['day_name'].mode()[0] 
    print('The most common day of the week: \n', most_common_day) 

    #display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common start hour: \n", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    #display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station: \n", most_start_station)

    #display most commonly used start station
    most_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station: \n", most_end_station)

    #most frequent combination of start station and end station trip
    combined_station = df['Start Station'] + " to " + df['End Station']
    most_frequent_combined_station = combined_station.mode()[0]
    print("The most most frequent combination of trips: \n", most_frequent_combined_station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minute, second = divmod(total_travel_time, 60)
    hour, minute = divmod(minute, 60)
    print("The total cumulative travel time : \n{} hours, {} minutes, and {} seconds.".format(hour, minute, second))

    #display mean travel time
    mean_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(mean_duration, 60)
    minute = int(minute)
    second = int(second)
    if minute > 60:
        hour, minute = divmod(minute, 60)
        hour = int(hour)
        minute = int(minute)
        print('The mean travel time : \n{} hours, {} minutes, and {} seconds.'.format(hour, minute, second))
    else:
        print('The mean travel time : \n{} minutes and {} seconds.'.format(minute, second))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display counts of user types
    user_type = df['User Type'].value_counts()
    print("The total of number of users base on type:\n{}\n".format(user_type))

    #display counts of gender and handle error if gender column not included
    try:
        gender = df['Gender'].value_counts()
        print("The total of number of users base on gender:\n{}\n".format(gender))
    except:
        print("Opps! gender data does not exist in this data files.\n")

    #display earliest, most recent, and most common year of birth handle error if birth column not included
    try:
        most_earliest_year = int(df['Birth Year'].min())
        print("The earliest year of birth: \n{}".format(most_earliest_year))
        most_recent_year = int(df['Birth Year'].max())
        print("\nThe most recent year of birth: \n{}".format(most_recent_year))
        common_year_year = int(df['Birth Year'].mode()[0])
        print("\nThe most common year of birth: \n{}".format(common_year_year))
    except:
        print("Opps! birth year data does not exist in this data files.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start = 0
    end = 5

    #display raw data 5 row each view
    question_see_raw_data = "Would you like to see raw data? Enter 'yes' or 'no'\n"
    see_raw_data = input(question_see_raw_data).lower()
    while see_raw_data not in see_raw_data_lists:
        see_raw_data = error_text("", question_see_raw_data)
    if see_raw_data == 'yes':
        while end <= df.shape[0] - 1:
            print(df.iloc[start:end,:])
            start += 5
            end += 5
            question_end_see_raw_data = "Do you wish to continue? Enter yes or no\n"
            end_see_raw_data = input(question_end_see_raw_data).lower()
            while end_see_raw_data not in see_raw_data_lists:
                end_see_raw_data = error_text("", question_end_see_raw_data)
            if end_see_raw_data == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
