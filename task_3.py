import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

PATH = os.getcwd() + "\\task_3_2.txt"

con = sqlite3.connect("V:\\supercell_data_intern_task\\sample.sqlite")
account_created_id_country = pd.read_sql_query(
    "SELECT account_id, country_code FROM account", con
)
iap_purchases = pd.read_sql_query(
    "SELECT account_id, iap_price_usd_cents FROM iap_purchase", con
)
con.close()


def getTotalRevenue_User_Country(
    account_created_id_country=account_created_id_country, iap_purchases=iap_purchases
):
    """
    Helper function.
    Takes in pandas dataframe.

    Returns a dictionary in format, {Country_code : [amount_users, amount_revenue]}.
    Each key contains a list with two values corresponding to values for the given country.
    """

    # Transform dataframe to dictionary
    account_created_id_country.to_dict()
    iap_purchases.to_dict()

    # Create dictionary for accounts with purchases. Format: {account_id : revenue}
    account_with_purchase = {}
    for idx in range(len(iap_purchases["account_id"])):
        account_id = iap_purchases["account_id"][idx]
        money_spent = iap_purchases["iap_price_usd_cents"][idx]

        if account_id not in account_with_purchase:
            account_with_purchase[account_id] = money_spent
        else:
            account_with_purchase[account_id] += money_spent

    # Create dictionary for where the account was created from. Format: {account_id : country_code}
    account_country = {}
    for idx in range(len(account_created_id_country)):
        account_id = account_created_id_country["account_id"][idx]
        country_code = account_created_id_country["country_code"][idx]

        account_country[account_id] = country_code

    # With the use of the two above dictionaries, create new dictionary where all the values are combined. (Read function description for format)
    country_revenue = {"Total": 0}
    for account in account_country:
        if account_country[account] not in country_revenue:
            revenue = 0
            user_count = 1
            country_code = account_country[account]

            if account in account_with_purchase:
                revenue = account_with_purchase[account]

            country_revenue[country_code] = [user_count, revenue]
            country_revenue["Total"] += revenue

        else:
            country_revenue[account_country[account]]
            revenue = 0
            user_count = 1
            country_code = account_country[account]

            if account in account_with_purchase:
                revenue = account_with_purchase[account]

            country_revenue[country_code][0] += 1
            country_revenue[country_code][1] += revenue
            country_revenue["Total"] += revenue

    return country_revenue


def plotData(
    user_p: np.array, user_label: list, revenue_p: np.array, revenue_label: list
):
    plt.subplot(1, 2, 1)
    plt.title("Users")
    plt.pie(user_p, labels=user_label)

    plt.subplot(1, 2, 2)
    plt.title("Revenue")
    plt.pie(np.array(revenue_p), labels=revenue_label)

    plt.show()


def getPercentage(
    float_len=2,
    path=PATH,
    plot=True,
    plot_if_user_p_greater=1,
    plot_if_revenue_p_greater=1,
):
    """
    float_len, takes in an int. Represents the amount of numbers shown after the decimal dot. Default: 2 - e.g. 0.15
    path, takes in a string representing a file destination to dump all data. e.g. "Country: GB | User: 2.00% | Revenue: 3.41% | Avg. revenue 0.64 USD per user."
    plot, takes in a bool. If true will plot data and show two different plots. One for the users % in a country, and one for the revenue % in a country. Default: True
    plot_if_user_p_greater, takes in an number (int, float), that represents a percentile. Will plot ONLY countries with higher percentile than defined in here. Default : 1
    plot_if_revenue_p_greater, takes in an number (int, float), that represents a percentile. Will plot ONLY countries with higher percentile than defined in here. Default : 1
    """

    # Delete existing data dump file. (Because writing to file uses append meaning running the code multiple times will cause the file to get crowded with old data.)
    if os.path.exists(path=path):
        os.remove(path=path)

    country_revenue = getTotalRevenue_User_Country()

    percentages_rev = []
    labels_rev = []

    percentages_usr = []
    labels_usr = []

    for country in country_revenue:
        if country == "Total" or country == None:
            continue

        # User
        x = country_revenue[country][0]
        user_p = x / len(account_created_id_country["account_id"]) * 100

        # Get data for plotting.
        if user_p > plot_if_user_p_greater:
            percentages_usr.append(user_p)
            label = f"{country} | {user_p:.1f}%"
            labels_usr.append(label)

        # Revenue
        x = country_revenue[country][1]
        revenue_p = x / int(country_revenue["Total"]) * 100

        # Get data for plotting.
        if revenue_p > plot_if_revenue_p_greater:
            percentages_rev.append(revenue_p)
            label = f"{country} | {revenue_p:.1f}%"
            labels_rev.append(label)

        # Avg. Revenue per user
        avg = country_revenue[country][1] / country_revenue[country][0]
        avg = avg / 100  # convert cents_usd to dollars_usd

        # Write all data to a file.
        with open(path, "a") as f:
            f.write(
                f"Country: {country} | User: {user_p:.{float_len}f}% | Revenue: {revenue_p:.{float_len}f}% | Avg. revenue {avg:.{float_len}f} USD per user. \n"
            )
    f.close()

    if plot:
        plotData(
            user_p=np.array(percentages_usr),
            user_label=labels_usr,
            revenue_p=np.array(percentages_rev),
            revenue_label=labels_rev,
        )


if __name__ == "__main__":
    getPercentage(plot_if_revenue_p_greater=1, plot_if_user_p_greater=1, plot=True)
