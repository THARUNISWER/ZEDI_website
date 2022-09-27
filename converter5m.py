import os
from datetime import date, time, timedelta, datetime

# flags
ERROR_out_of_range = 0

def create_file_5m(start_date_time, end_date_time, params, node):
    # start_date_time = datetime(2021, 3, 1, 19, 29, 50)
    # end_date_time = datetime(2021, 3, 25, 19, 29, 52)
    start_date = start_date_time.date()
    end_date = end_date_time.date()
    end_file = open("data5m.csv", "w")
    NODE_ID = int(node)
    end_file.write("sep=,")
    end_file.write("\n")
    directory = "D:\\5_minute_data\\"

    end_file.write("DATE_TIME,")

    TEMPERATURE = params[0]
    HUMIDITY = params[1]
    PRESSURE = params[2]
    AQI = params[3]
    CO2 = params[4]
    PIR1 = params[5]
    PIR2 = params[6]

    if TEMPERATURE == 1:
        end_file.write("TEMPERATURE,")
    if HUMIDITY == 1:
        end_file.write("HUMIDITY,")
    if PRESSURE == 1:
        end_file.write("PRESSURE,")
    if AQI == 1:
        end_file.write("AQI,")
    if CO2 == 1:
        end_file.write("CO2,")
    if PIR1 == 1:
        end_file.write("PIR1,")
    if PIR2 == 1:
        end_file.write("PIR2,")


    end_file.write("\n")

    delta = end_date_time - start_date_time
    if delta.days > 365:
        ERROR_out_of_range = 1

    FILE_NAME_FORMAT_5M = "%Y-%m"
    EXTENSION = ".csv"
    DELIM = ","


    def output_line_get_5m(words):
        out_line = words[0] + DELIM
        if TEMPERATURE == 1:
            out_line += (words[1] + DELIM)
        if HUMIDITY == 1:
            out_line += (words[2] + DELIM)
        if PRESSURE == 1:
            out_line += (words[3] + DELIM)
        if AQI == 1:
            out_line += (words[4] + DELIM)
        if CO2 == 1:
            out_line += (words[5] + DELIM)
        if PIR1 == 1:
            out_line += (words[6] + DELIM)
        if PIR2 == 1:
            out_line += (words[7] + DELIM)
        return out_line


    def add_one_month(orig_date):
        # advance year and month by one month
        new_year = orig_date.year
        new_month = orig_date.month + 1
        # note: in datetime.date, months go from 1 to 12
        if new_month > 12:
            new_year += 1
            new_month -= 12

        new_day = orig_date.day
        # while day is out of range for month, reduce by one
        new_date = date(new_year, new_month, new_day)
        return new_date


    curr_date = start_date
    while curr_date < end_date:
        file_path = directory + curr_date.strftime(FILE_NAME_FORMAT_5M) + EXTENSION
        if os.path.exists(file_path) is False:
            curr_date = add_one_month(curr_date)
            continue
        file = open(file_path)
        lines = file.readlines()
        lines = lines[1:]
        for line in lines:
            line = line.strip()
            words = line.split(DELIM)
            FORMAT = "%Y-%m-%d %H:%M:%S"
            curr_date_time = datetime.strptime(words[0], FORMAT)
            if curr_date_time < start_date_time:
                continue
            if curr_date_time > end_date_time:
                break
            out_line = output_line_get_5m(words)
            end_file.write(out_line)
            end_file.write("\n")
        file.close()
        curr_date = add_one_month(curr_date)

    end_file.close()

