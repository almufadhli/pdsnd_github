import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nType the name of the city you would like to see the data for, Chicago, New York, or Washington\n').lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print('please type the correct name of the city\n')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nfor which month? January, February, March, April, May, June, or All?\n').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('please type the correct name of the month or All\n')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nChoose which day of the week, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All?\n').lower()
        if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
            break
        else:
            print('please type the correct name of the day or All\n')

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month: ', months[df['Start Time'].dt.month.mode()[0] - 1].title())

    # display the most common day of week
    print('Most common day of the week: ', df['Start Time'].dt.weekday_name.mode()[0])

    # display the most common start hour
    print('Most common start hour: ', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most combination of start and end stations: ', df.groupby(['Start Station', 'End Station']).size().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total trave time: ', str(datetime.timedelta(seconds = int(total_time))))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Average travel time: ', str(datetime.timedelta(seconds = int(mean_time))), ' Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types:\n', df['User Type'].value_counts(), '\n')

    # Display counts of gender
    if 'Gender' in df: print('Count of gender:\n', df['Gender'].value_counts(), '\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:

        # earliest
        print('Earliest date of birth: ', int(df['Birth Year'].min()))

        # most recent
        print('Most recent date of birth: ', int(df['Birth Year'].max()))

        # most common
        print('Most common date of birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    """ Asks the user if they want to view raw data """

    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

        # input validation
        if view_data == 'yes':
            start_loc = 0
            end_loc = 5
            print(df.iloc[start_loc:end_loc])
            # display the next 5 rows of data each time the user enters 'yes'
            # condition will check if the user didn't reach the last index
            while end_loc <= df.last_valid_index():
                view_display = input("\n\nDo you wish to continue?: Enter yes or no\n").lower()

                # if the user choses yes the next 5 rows will display, if no then the program will exit this function
                if view_display == 'yes':
                    start_loc = end_loc
                    end_loc += 5
                    print(df.iloc[start_loc:end_loc])
                elif view_display == 'no':
                    return
                else:
                    print('\nPlease enter yes or no\n')
        elif view_data == 'no':
            break
        else:
            print('\nPlease enter yes or no\n')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
