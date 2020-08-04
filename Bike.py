import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Which city would you like to analyze? Please choose from Chicago, New York City, or Washington.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please type the city's name that you would like to analyze: ")
    while city.lower() != "new york city" and city.lower() != "washington" and city.lower() != "chicago": 
        city = input('Please try again and enter a valid city: ')

    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to evaluate? Please write out the month (all, january, february, ... , june) or write "all" to see all results : ')
    while month.lower() not in valid_months:
        month = input('Please enter a valid month or type "all": ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day do you want to evaluate? (all, monday, tuesday, ... sunday)) : ')
    while day.lower() not in valid_days:
        day = input('Please write a valid day of the week: ')

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
    # load in city
    if city.lower() == "chicago":
        df = pd.read_csv("chicago.csv")
    elif city.lower() == "new york city":
        df = pd.read_csv("new_york_city.csv")
    elif city.lower() == "washington":
        df = pd.read_csv("washington.csv")
    else:
        print ('error: did not load correct df')

    #convert to times 
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    #load in month
    if month.lower() == 'all':
        df = df

    elif month.lower() == 'january' or 'february' or 'march' or 'april' or 'may' or 'june':
        month_key = {'january' : 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        month_num = int(month_key[month])
        df = df.loc[df["Start Time"].dt.month==month_num]
    else:
        print('month error')
    #load in day 
    if day.lower() == 'all':
        df = df
    elif day.lower() in valid_days:
        day_key = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday':5, 'sunday': 6}
        day_num = int(day_key[day])
        df = df.loc[df["Start Time"].dt.dayofweek==day_num]
    else: 
        print('error day')
    # ask user if they want to see results - need a loop to keep going if the user enters they want to see more - TODO
    print("Do you want to see the first five lines of the results? Please type yes or no: ")
    display = input()
    display = display.lower()

    i = 5
    while display == 'yes':
        """ Display five rows of data at a time """
        print(df[:i])
        print("Would you like to see five more rows of the selection's data? Type yes or no ")
        i += 5
        display = input()
        display = display.lower()

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month_selection = df['month'].mode()[0]
    print('Most Popular Start Month For The Selection:', popular_month_selection)
    print()

    # display the most common day of week
    df['dow'] = df['Start Time'].dt.dayofweek
    popular_dow_selection = df['dow'].mode()[0]
    print('Most Popular Start Day of Week For Selection (Monday = 0):', popular_dow_selection)
    print()

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most Popular Start Hour for the selection is:", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station_start = df["Start Station"].mode()[0]
    print("The most popular start station is: ", popular_station_start)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print("The most popular ending station is: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start_End'] = df.groupby(['Start Station','End Station']).ngroup()
    popular_SE = df['Start_End'].mode()[0]

    name_of_start_end = df.loc[df['Start_End'] == popular_SE]
    print()
    print("The most popular start and stop station for the selection is:")
    print(name_of_start_end[['Start Station']].head(1))
    print(name_of_start_end[['End Station']].head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    hour_time = int(total_travel_time) / 3600
    print("Total travel time in hours is: ", hour_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    min_time = int(mean_travel_time) /60
    print('The average trip time in minutes is: ', min_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print("No Gender Data Avalible")

    # Display earliest, most recent, and most common year of birth
    # earliest 
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        print('the earliest year is: ', earliest_year)
    else:
        print("No Birth Year Data Avalible")
    # most recent 
    if 'Birth Year' in df:
        most_recent = int(df.dropna()['Birth Year'].tail(1))
        print('the most recent year is: ', most_recent)
    else:
        print("No birth year data avalible")
    # most common 
    if 'Birth Year' in df:    
        most_common_birth = int(df['Birth Year'].mode())
        print('the most common birth year is: ', most_common_birth)
    else:
        print("no birth year data avalible")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
