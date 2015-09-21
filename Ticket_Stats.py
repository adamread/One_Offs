import csv
import datetime
import pandas as pd

start_days = {}
first_day = datetime.date.today()
end_days = {}
open_tickets_per_day = {}
sum_open_days = 0
max_open_days = 0
min_open_days = 1000
num_prio_tickets = {'1': 0, '2': 0, '3': 0}

with open('C:/Users/Adam/Downloads/CPCM_All_Tickets_2015-09-21.csv', newline='') as csvfile:
    ticket_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for ticket in ticket_reader:
        ticket_start_date = datetime.datetime.strptime(ticket[7],  '%d.%m.%Y %H:%M:%S').date()

        if ticket[9] != '':
            ticket_end_date = datetime.datetime.strptime(ticket[9],  '%d.%m.%Y %H:%M:%S').date()
        else:
            ticket_end_date = None

        if ticket_start_date in start_days:
            start_days[ticket_start_date] += 1
        else:
            start_days[ticket_start_date] = 1

        if ticket_end_date is not None:
            if ticket_end_date in end_days:
                end_days[ticket_end_date] += 1
            else:
                end_days[ticket_end_date] = 1

            days_open = (ticket_end_date - ticket_start_date).days
        else:
            days_open = (datetime.date.today() - ticket_start_date).days

        sum_open_days += days_open
        if days_open > max_open_days:
            max_open_days = days_open
        if days_open < min_open_days:
            min_open_days = days_open

        if ticket_start_date < first_day:
            first_day = ticket_start_date

day_index = pd.date_range(first_day, datetime.date.today()).to_pydatetime()
issue_sum = 0
for day in day_index:
    if day.date() in start_days:
        issue_sum += start_days[day.date()]

    open_tickets_per_day[day.date()] = issue_sum

issue_sum = 0
for day in day_index:
    if day.date() in end_days:
        issue_sum += end_days[day.date()]

    open_tickets_per_day[day.date()] -= issue_sum

with open('C:/Users/Adam/Downloads/ticket_progression.csv', 'w') as out_file:
    writer = csv.writer(out_file)
    for key in sorted(list(open_tickets_per_day.keys())):
        writer.writerow([key, open_tickets_per_day[key]])

print("Max open days:", max_open_days)
print("Min open days:", min_open_days)
print("Average open days:", sum_open_days/len(start_days))
