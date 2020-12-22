

#                                                           Imports
##################################################################

import datetime
from datetime import date
import calendar
import math

##################################################################
#                                                           Functions
##################################################################

# Retrieves and sorts budget.txt ; returns tuple (income, expense)
def budget_grabber(scope):
    income = []
    expense = []
    # Note: Not tuples
    budget_tuples = []
    recurring_dates = []
    # Creates budget list without spaces
    with open('budget.txt','r') as f:
        budget_list_0 = f.readlines()
        budget_list_1 = [x.strip('\n') for x in budget_list_0]
    # Makes list into tuples, split at comma
    #####budget_tuples_0 = [tuple(map(str, sub.split(', '))) for sub in budget_list]
    budget_tuples_0 = [list(map(str, sub.split('; '))) for sub in budget_list_1]
    for transaction in budget_tuples_0:
        if iso_checker(transaction[4]) == True:
            budget_tuples.append(transaction)
        else:
            transaction[4] = transaction[4].split(', ')
            transaction[3] = transaction[3].split(', ')
            for date_recur in transaction[4]:
                recurring_dates.append([transaction[0], transaction[1], transaction[2], transaction[3], date_recur])
    for item in recurring_dates:
        budget_tuples.append(item)
    # Makes first entry of tuple (money) a float; includes Descrip. + Tag + Date
    if scope == 'full':
        for transaction in budget_tuples:
            # Populates income list
            if transaction[1] == '+':
                num = float(transaction[0])
                income.append((num, transaction[2], transaction[3], transaction[4]))
            # Populates expense list
            elif transaction[1] == '-':
                num = float(transaction[0])
                expense.append((num, transaction[2], transaction[3], transaction[4]))
        balance = (income, expense)
    # Only populates with Amount/Date
    elif scope == 'short':
        for transaction in budget_tuples:
            # Populates income list
            if transaction[1] == '+':
                num = float(transaction[0])
                income.append((num, transaction[4]))
            # Populates expense list
            elif transaction[1] == '-':
                num = float(transaction[0])
                expense.append((num,    transaction[4]))
        balance = (income, expense)

    return balance

# Performs various calculations; returns float or tuple of float
def budget_calc(action):
    # Retrives and splits the budget into Income / Expense
    budget = budget_grabber('short')
    income = budget[0]
    expense = budget[1]
    budget_list = []
    income_sum = 0
    expense_sum = 0
    balance_sum = 0
    week_delta = []
    week_delta_sum = 0
    # Calculates Menu Quick View
    if action == 'menu_view':
    # Totals Income & Week Delta +
        for transaction in income:
            income_sum+=transaction[0]
            budget_list.append(transaction)
            balance_sum+=transaction[0]
            transaction_date_object = date.fromisoformat(transaction[1])
            transaction_date = int(transaction_date_object.strftime('%j'))
            if (transaction_date <= day_of_year) and (transaction_date >= (day_of_year - 7)):
                week_delta.append(transaction)
                week_delta_sum+=transaction[0]
        # Totals Expense & Week Delta -
        for transaction in expense:
            expense_sum+=transaction[0]
            budget_list.append(transaction)
            balance_sum-=transaction[0]
            transaction_date_object = date.fromisoformat(transaction[1])
            transaction_date = int(transaction_date_object.strftime('%j'))
            if (transaction_date <= day_of_year) and (transaction_date >= (day_of_year - 7)):
                week_delta.append(transaction)
                week_delta_sum-=transaction[0]
        # Truncates values
        balance_sum = truncate(balance_sum, 2)
        week_delta_sum = truncate(week_delta_sum, 2)
        balance = (balance_sum, week_delta_sum)
    # Calculates Quick View
    elif action == 'quick_view':
        balance = 0
    # Calculates Detail View
    elif action == 'detail_view':
        balance = 0

    return balance

# Views Balance (data or visuals)
def budget_viewer():
    balance = budget_grabber('short')
    income = balance[0]
    expense = balance[1]
    print('INCOME\n')
    for item in income:
        print(item)
    print('\n\nEXPENSE\n')
    for item in expense:
        print(item)

# Writes transactions to file
def budget_add():
    print(f'{dash}')
    recur_input = input('Recurring (r) or Single (s) Transaction? :: ')
    try:
        if recur_input[0].lower() == 'r':
            # Calls Value, Amount, Date, and Tag functions seperately
            transaction_value = value_input()
            transaction_amount = amount_input()
            transaction_date = date_input('r')
            transaction_description = input('Short Description :: ')
            # If no description is given, writes '-' so program doesn't break
            if not transaction_description:
                transaction_description = '~'
            print(f'\t$\t{transaction_description}\n')
            transaction_tag = tag_input()
        elif recur_input[0].lower() == 's':
            # Calls Value, Amount, Date, and Tag functions seperately
            transaction_value = value_input()
            transaction_amount = amount_input()
            transaction_date = date_input('s') 
            transaction_description = input('Short Description :: ')
            # If no description is given, writes '-' so program doesn't break
            if not transaction_description:
                transaction_description = '~'
            print(f'\t$\t{transaction_description}\n')
            transaction_tag = tag_input()
        elif recur_input[0].lower() == 'q':
            return
        else:
            print(error_message)
            return budget_add()
    except IndexError:
        print('! No Input !')
        return budget_add()
    input_checker = input('-- Confirm? (n) * ' )
    if not input_checker:
        pass
    elif input_checker.lower() == 'n' or input_checker.lower() == 'no':
        print('\nTrying again...\n')
        budget_add()
    else:
        pass
    try:
        transaction = f'{transaction_amount}; {transaction_value}; {transaction_description}; {transaction_tag}; {transaction_date}\n'
    # Writes transaction to file
        with open('budget.txt','a') as f:
            f.write(transaction)
        print(success_message,'\n')
    except UnboundLocalError:
        print('ERROR -- RESTARTING')
        return budget_add() 

# Takes Date inputs for budget_editor; returns either DateofTransaction or Tuple with Dates of Transactions
def date_input(occurence):
    repeater = True
    repeater2 = True
    repeater3 = True
    
    while repeater == True:
        if occurence == 's':
            # Takes user input
            given_first_date = input('Date of Transaction : ')
            # Checks with date function to determine valid date; returns (boolean, date) with date as 0 if False
            checker_0 = date_checker(given_first_date, 's', big_ole_list)
            if checker_0[0] == True:
                repeater = False
                first_transaction_date = checker_0[1]
                print(f'\t$\t{first_transaction_date}\n')
                return first_transaction_date
            elif checker_0[0] == False:
                print('')
        elif occurence == 'r':
            transaction_dates = []
            # Takes user input
            given_first_date = input('First Date of Transaction : ')
            # Checks with date function to determine valid date; returns (boolean, date) with date as 0 if False
            checker_1 = date_checker(given_first_date, 's', big_ole_list)
            if checker_1[0] == True:
                repeater = False
                first_transaction_date = checker_1[1]
                print(f'\t$\t{first_transaction_date}\n')
            elif checker_1[0] == False:
                print('')
    # If recurring, gets span of dates
    while repeater2 == True and repeater == False:
        if occurence == 's':
            repeater2 = False
            pass
        elif occurence == 'r':
            # Takes user input
            given_last_date = input('Last Date of Transaction : ')
            checker_2 = date_checker(given_last_date, 'r', big_ole_list)
            # Checks with date function to determine valid date; returns (boolean, date) with date as 0 if False
            if checker_2[0] == True:
                repeater2 = False
                last_transaction_date = checker_2[1]
                print(f'\t$\t{last_transaction_date}\n')
            elif checker_2[0] == False:
                print('')
    # Gets No. of days between First and Last transaction
    transaction_date_delta = (last_transaction_date - first_transaction_date).days
    # Gets starting count for recur_date function
    span = 366-transaction_date_delta
    # Populates list of dates; asks for type of Recurrence
    while repeater3 == True and repeater2 == False and occurence == 'r':
        recurrence_input = input('Recurrence : ')
        print('')
        try:
            num_days = (recurrence_input[:-1])
            recur_type = recurrence_input[-1]
        except ValueError:
            pass

        # Creates empty list to put dates into
        trans_empty = []
        transaction_dates = []
        transaction_dates_beta = [] 
        if len(recurrence_input) < 2:
            print(error_message)
            pass
        elif recur_type == 'm':
            trans = recur_dates(span, first_transaction_date, 1, trans_empty)       
            num_days = str(num_days)
            for every_day_obj in trans:
                every_day = str(every_day_obj)
                if num_days in every_day[-2:]:
                    transaction_dates_beta.append(every_day)
            string_LTD = str(last_transaction_date)
            if num_days in string_LTD[-2:]:
                transaction_dates_beta.append(string_LTD)
        elif recur_type == 'd':
            num_days=int(num_days)
            trans = recur_dates(span, first_transaction_date, num_days, trans_empty)
            for entry in trans:
                transaction_dates_beta.append(entry)
        else:
            print(error_message)
        for trans_entry in transaction_dates_beta:
            entry = str(trans_entry)
            print(f'\t$\t{entry}')
            transaction_dates.append(entry)

        check = input('Do these dates seem correct? (n) ')
        if not check:
            trans_dates = ''
            for date_string in transaction_dates:
                trans_dates += f'{date_string}, '
            trans_dates = trans_dates[:-2]
            return trans_dates
        elif check.lower() == 'n' or check.lower() == 'no':
            print('\nTrying again...\n')
        else:
            trans_dates = ''
            for date_string in transaction_dates:
                trans_dates += f'{date_string}, '
            trans_dates = trans_dates[:-2]
            return trans_dates

# Takes date input for BE, checks if date is possible, returns dateObject and boolean as (bool, date)
def date_checker(date_input, occurence, big_ole_list):
    # Variables
    day = int(datetime.date.today().strftime('%d'))
    year = int(datetime.date.today().strftime('%Y'))
    month = int(datetime.date.today().strftime('%m'))
    # Populates Dict of Month Abbr:Numbers
    month_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    for key in month_num.keys():
        month_num[key] = str(month_num[key])
        if len(month_num[key]) == 1:
            month_num[key] = '0'+month_num[key]
        else:
            month_num[key] = month_num[key]
    list_of_year = big_ole_list[1]
    week_list = big_ole_list[0]
    years_list = big_ole_list[2]
 # More variables
    nextmonth = month+1 
    nextyear = year+1

    repeat = True
    repeat2 = True
    repeat3 = True

    current_date = datetime.date.today().strftime('%Y-%m-%d')

    # Single Payments
    if occurence == 's':
        # Makes default an error
        transaction_date_beta = 'error'
        # If no date is given, default = Today
        if not date_input:
            transaction_date_beta = current_date
        # If given as MM-DD or DD
        elif date_input[0].isdigit() == True:
            # MM-DD
            if len(date_input) == 4 or len(date_input)== 5:
                transaction_date_beta = f'{date_input[:2]}-{date_input[-2:]}'
            # DD
            elif len(date_input) == 2:
                transaction_date_beta = f'{year}-{month}-{date_input}' 
            # YYYY-MM-DD
            elif len(date_input) == 10:
                transaction_date_beta = date_input   
            # YYYMMDD
            elif len(date_input) == 8:
                transaction_date_beta = f'{date_input[:4]}-{date_input[4:6]}-{date_input[6:]}'
        else:
            for month_name in month_num.keys():
                # If date given as Month DD
                if date_input[:3].capitalize() == month_name:
                    transaction_date_beta = f'{month_num[month_name]}-{date_input[-2:]}'
                    break
                # If given as weekday
                elif len(date_input) >= 3:
                    for dow in week_list: 
                        dow_str = str(dow)
                        if date_input[:3].capitalize() in dow.strftime('%a'):
                                    transaction_date_beta = dow_str
                                    break
        # Checks date with list for 1yr of dates
        success = False
        for doy in list_of_year:
            doy_str = str(doy)
            if transaction_date_beta in doy_str:
                transaction_date = doy
                success = True
                break

        ## ADD IN MULTI YEAR SUPPORT
        if success == False:
            for doyy in years_list:
                doyy_str = str(doyy)
                if transaction_date_beta in doyy_str:
                    transaction_date = doyy
                    break
        # Checks if above is successful
        try:
            return (True, transaction_date)
        except UnboundLocalError:
            print(error_message, 'Please enter date as MM-DD, Month DD, or DD, or YYYY-MM-DD')
            return (False, 0)
    # Recurring payment last date -
    if occurence == 'r':
        # Makes default an error
        transaction_date_beta = 'error'
        # If no date is given, default = 1yr from Today
        if not date_input:
            transaction_date_beta = f'{nextyear}-{month}-{day}'
        # If given as MM-DD or DD
        elif date_input[0].isdigit() == True:
            # MM-DD
            if len(date_input) == 4 or len(date_input)== 5:
                transaction_date_beta = f'{date_input[:2]}-{date_input[-2:]}'
            # DD
            elif len(date_input) == 2:
                transaction_date_beta = f'{year}-{month}-{date_input}' 
            # YYYY-MM-DD
            elif len(date_input) == 10:
                transaction_date_beta = date_input   
            # YYYMMDD
            elif len(date_input) == 8:
                transaction_date_beta = f'{date_input[:4]}-{date_input[4:6]}-{date_input[6:]}'   
        else:
            for month_name in month_num.keys():
                # If date given as Month DD
                if date_input[:3].capitalize() == month_name:
                    transaction_date_beta = f'{month_num[month_name]}-{date_input[-2:]}'
                    break
                # If given as weekday
                elif len(date_input) >= 3:
                    for dow in week_list: 
                        dow_str = str(dow)
                        if date_input[:3].capitalize() in dow.strftime('%a'):
                                    transaction_date_beta = dow_str
                                    break

        # Checks date with list for 1yr of dates
        success = False
        for doy in list_of_year:
            doy_str = str(doy)
            if transaction_date_beta in doy_str:
                success = True
                transaction_date = doy
                break
        ## ADD IN MULTI YEAR SUPPORT
        if success == False:
            for doyy in years_list:
                doyy_str = str(doyy)
                if transaction_date_beta in doyy_str:
                    transaction_date = doyy
                    break
        # Checks if above is successful
        try:
            return (True, transaction_date)
        except UnboundLocalError:
            print(error_message, 'Please enter date as MM-DD, Month DD, or DD, or YYYY-MM-DD')
            return (False, 0)

# Recurring Date Function Populator; returns List of DateObjects
def recur_dates(count, date_start, no_days, date_list):
    date_list.append(date_start)
    next_date = date_start + datetime.timedelta(days = no_days)
    count+=no_days
    if count >= 366:
        return date_list
    else:
        return recur_dates(count, next_date, no_days, date_list)

# Takes Amount inputs for budget_editor; returns float
def amount_input():
    loop = True
    while loop == True:
        try:
            input_amount0 = float(input('Amount :: '))
            input_amount = truncate(input_amount0, 2)
            print(f'\t$\t{input_amount}\n')
            return input_amount
        except:
            print(error_message)

# Takes value inputs for budget_editor, returns string ('e' or 'i')
def value_input():
    loop = True
    while loop == True:
        transaction_value = str(input('Income (i) or Expense (e)? :: '))
        try:
            if transaction_value[0].lower() == 'i':
                transaction_value = '+'
                print(f'\t$\tIncome\n')
                return transaction_value
            elif transaction_value[0].lower() == 'e':
                transaction_value = '-'
                print(f'\t$\tExpense\n')
                return transaction_value
            else:
                print(error_message)
        except IndexError:
            print('\n! No Input !\n')

# Takes tags for budget_editor; writes to tags.txt, returns string
def tag_input():
    input_tags = []
    export_tag_list = []
    new_tag_list = []
    with open('tags.txt','r') as f:
        tag_list_0 = f.readlines()
        tag_list = [x.strip('\n') for x in tag_list_0]
    repeat = True
    while repeat == True:
        # enter * to view Tags; Commas separate tags
        input_tag0 = input('Tag :: ')
        input_tags = input_tag0.split(',')
        input_tags = [x.strip(' ') for x in input_tags]
        for input_tag in input_tags:
            if not input_tag:
                pass
            elif input_tag == '*':
                print('\nTAGS:\n')
                for tag in tag_list:
                    print(f'$- {tag}')
                print('\n')
            else:
                for tag in tag_list:
                    if input_tag.upper() == tag:
                        repeat = False
                        export_tag_list.append(input_tag.upper())
                        match = 0
                        break
                    else:
                        match = 1
                if match == 0:
                    pass
                elif match == 1:
                    add_tag = input(f"'{input_tag.upper()}' not Found. Add Tag (y/n)? : ")
                    if add_tag.lower() == 'y':
                        new_tag_list.append(input_tag.upper())
                        export_tag_list.append(input_tag.upper())
                    elif add_tag.lower() == 'n':
                        if not export_tag_list:
                            pass
                        else:
                            break
        if not export_tag_list:
            print('Enter at least 1 tag')
            pass
        else:
            break
    with open('tags.txt','a') as g:
        for a_tag in new_tag_list:
            g.write(f'{a_tag}\n')
    for input_tag_f in export_tag_list:
        print(f'\t$\t{input_tag_f}')
    return export_tag_list
# Make a function that handles "accounts" (cash, bank, venmo, etc)
def account_input():
    pass
# Truncates Numbers ; returns float 
def truncate(number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

# Returns True if given date is in ISO format; false if not
def iso_checker(a_date):
    try:
        date.fromisoformat(a_date)
        return True
    except ValueError:
        return False

# Prints out menu of shortcuts/formats
def helper():
    print('')
    print(dash)
    print('\t\t\t\t\t\t\tH E L P')
    print(dash)

# Makes list of 1yr in the past 3yr in the future
def year_maker():
    # Years of Budget
    today = datetime.date.today()
    year_count_past = -1
    year_count_future = 3
    years_p = []
    years_f = []
    years_f2 = []
    year_span = 4
    year_past = today + datetime.timedelta(days = -366)
    year_future = today + datetime.timedelta(days = 366) 
    years = recur_dates(-366, year_past, 1, years_p)
    list_of_years_future = recur_dates(-366, year_future, 1, years_f )
    for year_date in list_of_years_future:
        years.append(year_date)
    #future_2 = recur_dates(-366, year_future, 1, years_f2 )
    return years
##################################################################
#                                               Universal Variables
##################################################################

#MM-DD
now = datetime.datetime.today().strftime('%m-%d')
#DoW
x_day = datetime.datetime.today().strftime('%A')
#Datetime object for Today
today = datetime.date.today()
#Datetime object for tomorrow
tomorrow = today + datetime.timedelta(days = 1)
#Numerical day of year
day_of_year = int(datetime.datetime.today().strftime('%j'))
#List of the following 7 days (excluding today)
week_list_empty = []
week_list = recur_dates(358, tomorrow, 1, week_list_empty)
#List of dates in the next 365+1 days
list_of_year_empty = []
list_of_year = recur_dates(0, today, 1, list_of_year_empty)
# List of Past 1 year and Future 3 years
years = year_maker()
# List with Week and Year as 0 and 1
big_ole_list = [week_list, list_of_year, years]
# Aesthetics# for a 92 x 26 terminal window
dash = ('----'*23)
slash = ('////'*23)
# Error/Success Message
error_message = ('\n! Input Error !\n')
success_message = ('$$ -! Success !- $$')

##################################################################
#                                                   MAIN FUNCTION
##################################################################
def main():
    
    menu_view = budget_calc('menu_view')
    balance = "{:,}".format(menu_view[0])
    week_delta = "{:,}".format(menu_view[1])
    # IDEA : make shortcut for expanded menu (liquid, savings. overall /\)
    #if week_delta
    print (now)
    print(f'{dash}')
    print('\t'*4,'$ $ $ $ Budget $ $ $ $')
    print(f'{dash}')
    print(f'    Balance $ {balance}','\t\t\t\t\t\t',u"Δ",f'Week $ {week_delta}\n')
    print(f'{dash}')
    print('\t\t\t- 1\t Add Transaction')
    print('\t\t\t- 2\t View Balance (data)')
    print('\t\t\t- 3\t View Balance (visuals)')
#    print('\t\t\t- 4\t Edit Transactions/Tags/Accounts')
    print(f'{dash}')
    # Creates count value for errors
    count = True
    while count == True:
        # Catches ValueErrors
        try:
            user_input = int(input('\t\t\t- '))
            # Makes sure input is valid
            if (user_input == 0) or (user_input == 1) or (user_input == 2) or (user_input == 3) or (user_input == 4):
                count = False
            else:
                print('! Invalid Input !')
        except ValueError:
            print('! Invalid Input !')
    if user_input == 1:
        budget_add()
    elif user_input == 2:
        budget_viewer()
    elif user_input == 3:
        pass
    elif user_input == 4:
        pass
    elif user_input == 0:
        helper()
    run_again = input('Run again? (y/n) : ')
    if run_again == 'y':
        print(slash)
        main()
main()

