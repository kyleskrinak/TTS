#!/bin/bash

# Retrieve system-based values for deciding whether to prompt:
system_day_number=$(date +"%d")  # e.g. "05"
system_month=$(date +"%m")      # e.g. "01"
system_year=$(date +"%y")       # e.g. "25"

# Check if the system day is within the first 7 days of the month.
if [[ $((10#$system_day_number)) -le 7 ]]; then
    # Prompt for a new month (mm).
    read -p "Enter month (mm) [$system_month]: " month
    month=${month:-$system_month}
else
    # Use system month by default.
    month=$system_month
fi

# If it is January and within the first 7 days, prompt for the year.
if [[ "$system_month" == "01" && $((10#$system_day_number)) -le 7 ]]; then
    read -p "Enter year (yy) [$system_year]: " year
    year=${year:-$system_year}
else
    year=$system_year
fi

# Separately, ask the user which day number they actually want to use for the filename.
default_day_number=$(date +"%d" | awk '{printf "%02d", $1}')
read -p "Enter day number (dd) [$default_day_number]: " day_number
day_number=${day_number:-$default_day_number}

# Validate the user’s day number input.
if [[ ! "$day_number" =~ ^[0-9]{2}$ ]]; then
    echo "Invalid day number. Please enter a valid two-digit number."
    exit 1
fi

# Form the yy-mm-dd prefix.
date_prefix="$year-$month-$day_number"

# Prompt for the media description.
read -p "Enter media description [Dispatch]: " media_description
media_description=${media_description:-Dispatch}

# Combine them into a final filename.
filename="${date_prefix}-${media_description}.txt"

# Display the command.
echo "nvim $filename"

# Confirm execution.
read -p "Do you want to execute this command? (yes/no) [yes]: " confirm
if [[ "$confirm" == "yes" || "$confirm" == "" ]]; then
    nvim "$filename"
else
    echo "Command execution cancelled."
fi