import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june'] # list of months for use in later functions
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] # list of days for use in later functions

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (Chicago, New York City, Washington).

    while True:
        city = input("Which city's data would you like to see? (Chicago, New York City, Washington): ").lower()
        if city not in CITY_DATA:
            print("Sorry, there is no data for that city.")
            continue
        else:
            break

    # Gets user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month you would like to see data for. If not, enter 'all': ").lower()
        if month not in months:
            if month == 'all':
                break
            else:
                print("Our database only has data from January to June. If you want to see all data, enter 'all'")
                continue
        else:
            break

    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day of week, or 'all': ").lower()
        if day not in days:
            if day == 'all':
                break
            else:
                print("Please enter a day of the week, or 'all': ")
                continue
        else:
            break

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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
    popular_month = df['month'].mode()[0]
    print('Month with the highest usage is:', popular_month)\

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week is: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most frequent start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most popular start station is: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most popular end station is: ', end_station)

    # display most frequent combination of start station and end station trip
    combination = ("\nStart: " + df['Start Station'] + "\nEnd: " + df['End Station'])
    popular_combination = combination.mode()[0]
    print('Most frequently used combination of start and end stations is: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('Total cumulative travel time is: ', time.strftime("%H:%M:%S", time.gmtime(travel_time)))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Bike users' average travel time is: ", time.strftime("%H:%M:%S", time.gmtime(mean_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = pd.value_counts(df['User Type'])
    print(user_count)

    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = pd.value_counts(df['Gender'])
        print(gender_count)
    else:
        print("Sorry, there is no gender data at the moment.")

    if "Birth Year" in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("The oldest user is born in {}. \nThe youngest user is born in {}. \nMost users are born in {}.".format(earliest, most_recent, most_common))
    else:
        print("Sorry, there is no birth year data at the moment.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Show 5 rows of data at a time upon user's request"""

    start_loc = 0

    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? yes/no: ").lower()

        if view_data == 'yes':
            print(df.iloc[0 : 5])
            start_loc += 5
            view_display = input("View the next 5?: ").lower()
            if view_display == 'yes':
                print(df.iloc[start_loc : start_loc + 5])
            elif view_display == 'no':
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no': ")
        elif view_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no': ")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
