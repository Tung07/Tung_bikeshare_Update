import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    yAsks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the da of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please choice a in three city below: Chicago, New York City or Washington to Analyze\n\n")
        city = city.lower()

        if city not in ('new york city', 'chicago', 'washington'):
            print("Please enter a valid in (Chicago, New York City or Washington) to Analyze")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to analyze for " + city.title() +
                      "? You can choose between January, February, March, " +
                      "April, May and June, or type all if you do not wish " +
                      "to specify a month.\n\n")

        month = month.lower()

        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Please enter a valid (january, february, march, april, may, june)")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = input("Now, let's pick a day to detail." +
                            "(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday), "
                            "or type all if you do not wish to specify a day.\n\n")

        day_of_week = day_of_week.lower()

        if day_of_week not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("day of week not valid!!! " +
                  "Please enter a valid day in (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday)" +
                  "or all for a week")
            continue
        else:
            break

    print('-' * 40)
    return city, month, day_of_week


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
    # read the dataframe of the choice city
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to a datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get month and day from dataframe
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday

    # filtering of dataset, based on selections
    # if month != 'all':
    month = month.capitalize()
    list_month_name = list(cal.month_name)
    if month in list_month_name:
        month = list_month_name.index(month)
        df = df[df['Month'] == month]

    # if day != 'all':
    day = day.capitalize()
    list_day_name = list(cal.day_name)
    if day in list_day_name:
        day = list_day_name.index(day)
        df = df[df['Weekday'] == day]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # determine most common month
    ind_month = df['Month'].value_counts().idxmax()

    # print full name of most common month
    if month != 'all':
        print('You have choice analyze', month.title(), ', so, unsurprisingly, the most common ' +
              'month in', city.title(), 'is', cal.month_name[ind_month], ' \n\n')

    else:
        print('The most common month in ', city.title(), ' is',
              cal.month_name[ind_month], '.\n\n')

    # determine most common weekday
    ind_day = df['Weekday'].value_counts().idxmax()

    # print full name of most common weekday
    if day != 'all':
        print('You have choice analyze', day.title(), 'so, unsurprisingly, the most common ' +
              'day of the week in', city.title(), 'is', cal.day_name[ind_day], '\n\n')
    else:
        print('The most common day of the week is', cal.day_name[ind_day], '\n\n')

    # extract the hour part from Start Time and save in new variable
    df['Start Hour'] = df['Start Time'].dt.hour

    # print most common start hour
    print('The most common start hour is',
          df['Start Hour'].value_counts().idxmax(), 'o\'clock.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most common start station is',
          df['Start Station'].value_counts().idxmax(), '.\n\n')

    print('The most common end station is',
          df['End Station'].value_counts().idxmax(), '.\n\n')

    # combine start and end stations into new column
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station'] + ' (end).'

    # print station combination
    print('The most common station combination is ',
          df['Station Combination'].value_counts().idxmax(), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time in seconds with .sum()
    trip_sum_sec = df['Trip Duration'].sum()

    # convert total travel time to hours and round with zero decimal points
    trip_sum_h = round(trip_sum_sec / 60 / 60, 0)

    # print total travel time
    print('The total travel time is', trip_sum_h, 'hours.\n\n')

    # calculate mean travel time in seconds with .mean()
    trip_mean_sec = df['Trip Duration'].mean()

    # convert total travel time to minutes and round with zero decimal points
    trip_mean_min = round(trip_mean_sec / 60, 0)

    # display mean travel time either in minutes if below one hour, or in hours if above
    if trip_mean_min < 60:
        print('The mean travel time is', trip_mean_min, 'minutes.\n\n')
    else:
        trip_mean_h = round(trip_mean_min / 60, 1)
        print('The mean travel time is', trip_mean_h, 'hours.\n\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. Statistics will be calculated using NumPy."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # convert user type to an NumPy array for subsequent counts
    user_types = df['User Type'].values

    # count the occurrences of the different user types
    ct_subscriber = (user_types == 'Subscriber').sum()
    ct_customer = (user_types == 'Customer').sum()

    # print user type counts
    print('The number of subscribers in', city.title(), 'is:', ct_subscriber, '\n')
    print('The number of customers in', city.title(), 'is:', ct_customer, '\n')

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # gender and year of birth are missing from the Washington dataset
    if city.title() != 'Washington':
        # counts of gender
        # convert gender to an NumPy array for subsequent counts
        gender = df['Gender'].values

        # count the occurrences of the different user types
        ct_male = (gender == 'Male').sum()
        ct_female = (gender == 'Female').sum()

        # print counts
        print('The number of male users in', city.title(), 'is:', ct_male, '\n')
        print('The number of female users in', city.title(), 'is:', ct_female, '\n')

        # year of birth
        # convert gender to an NumPy array for subsequent statistics
        birth_year = df['Birth Year'].values

        # get unique birth years and exclude NaNs
        birth_year_unique = np.unique(birth_year[~np.isnan(birth_year)])

        # the latest birth year is the highest / maximum number
        latest_birth_year = birth_year_unique.max()

        # the earliest birth year is the lowest / minimum number
        earliest_birth_year = birth_year_unique.min()

        # print latest and earliest birth year
        print('The most recent birth year of users in', city.title(), 'is:',
              latest_birth_year, '\n')
        print('The earliest birth year of users in', city.title(), 'is:',
              earliest_birth_year, '\n')

        # display most common birth year
        print('The most common birth year of users in', city.title(), 'is:',
              df['Birth Year'].value_counts().idxmax(), '\n')

    else:
        print('Sorry. Gender and birth year information are not available for Washington!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """ Displays 5 lines of raw data at a time when yes is selected."""
    i = 1
    while True:
        rawdata = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if rawdata.lower() == 'yes':
            print(df[i:i + 5])
            i = i + 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
