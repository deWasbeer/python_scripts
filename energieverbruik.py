#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 13:35:12 2025

@author: johan
"""

def lamp(uur, dag):
    """
    Calculates the total wattage of lamps used at a specific hour of the day.

    Args:
        uur (int): The hour of the day (0-23).
        dag (int): The day of the year (0-364).

    Returns:
        int: The total wattage of the lamps.
    """
    aantal_lampen = 10
    watt_lampen = 10
    if 19 < uur < 22:  # Lamps are on between 8 PM (20:00) and 10 PM (22:00) exclusive
        watt_totaal = aantal_lampen * watt_lampen
    else:
        watt_totaal = 0
    return watt_totaal

def koken(uur, dag, kwartier):
    """
    Calculates the wattage used for cooking at a specific quarter of an hour.

    Args:
        uur (int): The hour of the day (0-23).
        dag (int): The day of the year (0-364).
        kwartier (int): The 15-minute interval within the hour (0-3).
                         0:00-0:14, 1:15-0:29, 2:30-0:44, 3:45-0:59.

    Returns:
        int: The wattage used for cooking.
    """
    watt_inductie = 2000
    if 18 < uur < 20:  # Cooking happens between 7 PM (19:00) and 8 PM (20:00) exclusive
        if kwartier == 0 or kwartier == 1:  # For the first 30 minutes of the hour
            watt_totaal = watt_inductie
        else:
            watt_totaal = 0
    else:
        watt_totaal = 0
    return watt_totaal

def main():
    """
    Generates a 4-dimensional list 'energie' to store the power usage
    for every 15-minute interval of the year.
    The structure is energie[day][hour][quarter][power_value].
    """
    kwartieren_per_uur = 4
    uren_per_dag = 24
    dagen_per_jaar = 365

    # Initialize the 'energie' list
    energie = []

    # Iterate through each day of the year
    for dag in range(dagen_per_jaar):
        dag_data = []  # List to store data for the current day
        # Iterate through each hour of the day
        for uur in range(uren_per_dag):
            uur_data = []  # List to store data for the current hour
            # Iterate through each 15-minute interval (quarter) of the hour
            for kwartier in range(kwartieren_per_uur):
                watt_totaal = 0

                # Calculate power usage for lamps
                watt_lampen = lamp(uur, dag)
                watt_totaal += watt_lampen

                # Calculate power usage for cooking
                watt_koken = koken(uur, dag, kwartier)
                watt_totaal += watt_koken

                # Store the power usage for this 15-minute interval
                uur_data.append([kwartier, watt_totaal])
            dag_data.append([uur, uur_data])
        energie.append([dag, dag_data])

    # Example of accessing the energy use for a specific quarter
    # Let's say we want to access the energy use on the 5th day (index 4),
    # at 10 AM (index 10), during the 3rd quarter (index 2).
    # The power value will be at index 1 of the inner list.
    if energie: # Check if the energie list is not empty
        example_power = energie[4][1][10][1][2][1] # Accessing energie[day][hour][quarter][power_value]
        print(f"Power usage on day 5, hour 10, quarter 3: {example_power} Watts")

    # Calculate the total energy used over the year in Watt-hours
    total_watt_hours = 0
    for dag_data in energie:
        for uur_data_entry in dag_data[1]: # Access the list of hour data
            for kwartier_data in uur_data_entry[1]: # Access the list of quarter data
                power_watt = kwartier_data[1]
                # Each interval is 15 minutes = 0.25 hours
                total_watt_hours += power_watt * (15/60)

    print(f"\nTotal energy used over the year: {total_watt_hours:.2f} Watt-hours")

main()