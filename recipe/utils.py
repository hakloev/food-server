from datetime import timedelta, datetime
import time


def get_today_as_string():
    """
    Returns todays date as a string
    :return: The date as string
    """
    return time.strftime('%Y-%m-%d')


def get_week_from_date(date):
    """
    Returns the week number for a datetime object
    :param date: The date to return week number for
    :return: The week number, as int
    """
    return date.isocalendar()[1]


def calculate_week_ends_for_date(date):
    """
    Calculates start and end date for a week, given a date in the week
    :return: beginning and end of week
    """
    day_of_week = date.weekday()
    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = date - to_beginning_of_week
    to_ending_of_week = timedelta(days=6 - day_of_week)
    end_of_week = date + to_ending_of_week
    return beginning_of_week, end_of_week


def get_start_date_from_year_and_week(query):
    """
    Returns start date for a query on the following format: '%s-W%s' % (year, week)
    :param query: The query in question
    :return: The start date of the week (monday)
    """
    return datetime.strptime(query + '-1', '%Y-W%W-%w')