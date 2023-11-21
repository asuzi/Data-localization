import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import calendar

con = sqlite3.connect("V:\\supercell_data_intern_task\\sample.sqlite")
sessions = pd.read_sql_query("SELECT account_id, date FROM account_date_session", con)
sessions = sessions.to_dict()
con.close()


def getActiveUsers(mode: str, plot: bool):
    """
    Returns a dictionary of daily users. Use mode to specify.

    Mode:
    "day", to return the Active Users by Day
    "month", to return the Active Users by Month

    Plot:
    "True" to plot the given data
    "False" to not to plot data
    """

    unique_accounts = {}
    dates = {}

    for i in range(len(sessions["account_id"])):
        # Unique ID and Date from dictionary.
        uid = sessions["account_id"][i]
        date = sessions["date"][i]

        # Reset counter
        unique_count = 0
        returning_count = 0

        # New user
        if uid not in unique_accounts:
            unique_accounts[uid] = date
            unique_count += 1

        # Returning user
        else:
            returning_count += 1
            unique_accounts[uid] += date

        # Check for mode. If true, slice day from date
        if mode == "month":
            date = date[0:-3]

        # Calculate amount of days in given year, month.
        year_month = int(date[0:4]), int(date[5:7])

        # Create 'dates' dictionary
        if date not in dates:
            dates[date] = {}
            dates[date]["new_user_count"] = unique_count
            dates[date]["returing_user_count"] = returning_count
            dates[date]["day_count"] = calendar.monthrange(
                year_month[0], year_month[1]
            )[1]
        else:
            dates[date]["new_user_count"] += unique_count
            dates[date]["returing_user_count"] += returning_count

    # Plot data if true
    if plot:
        plotData(dates, mode=mode)
    return dates


def plotData(dates: dict, mode: str):
    # Helper function for getActiveUsers to plot data. Takes in a dictionary created from getActiveUsers.
    for date in dates:
        new, returning, full = (
            dates[date]["new_user_count"],
            dates[date]["returing_user_count"],
            dates[date]["new_user_count"] + dates[date]["returing_user_count"],
        )

        # Calculate average if month.
        if mode == "month":
            full = (new + returning) / dates[date]["day_count"]
            new = new / dates[date]["day_count"]
            returning = returning / dates[date]["day_count"]

        plt.stem(
            date, new, linefmt=None, markerfmt="Blue", basefmt=None
        )  # New users per month
        plt.stem(
            date, returning, linefmt=None, markerfmt="Red", basefmt=None
        )  # Returning users per month
        plt.stem(
            date, full, linefmt=":", markerfmt="Green", basefmt=None
        )  # New users + returing users per month

    plt.title("Active Users average by month.")
    if mode == "day":
        plt.title("Active Users by day.")

    plt.figtext(
        0.7,
        0.9,
        "Green = New users and returning users combined \n Red = Returning users \n Blue = New users",
    )
    plt.show()


if __name__ == "__main__":
    getActiveUsers(mode="day", plot=True)
