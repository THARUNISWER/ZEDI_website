import os
from datetime import date, time, timedelta, datetime


# flags
ERROR_range_very_big = 0
ERROR_data_not_available = 0

def create_file_1s(start_date_time, end_date_time, params, node):
    # start_date_time = datetime(2021, 3, 18, 19, 29, 50)
    # end_date_time = datetime(2021, 3, 30, 19, 29, 52)
    start_date = start_date_time.date()
    end_date = end_date_time.date()
    end_file = open("data1s.csv", "w")
    end_file.write("sep=,")
    end_file.write("\n")
    NODE_ID = int(node)
    directory = "D:\\1_second_data\\"

    delta = end_date_time - start_date_time
    if delta.days > 30:
        ERROR_range_very_big = 1

    end_file.write("DATE_TIME,")

    VOLTAGE = params[1]
    CURRENT = params[0]
    FREQUENCY = params[2]
    POWER = params[3]

    if CURRENT == 1:
        end_file.write("CURRENT_R,CURRENT_Y,CURRENT_B,")
    if VOLTAGE == 1:
        end_file.write("VOLTAGE_R,VOLTAGE_Y,VOLTAGE_B,")
    if FREQUENCY == 1:
        end_file.write("FREQUENCY_R,FREQUENCY_Y,FREQUENCY_B,")
    if POWER == 1:
        end_file.write("POWER_R,POWER_Y,POWER_B,POWER_TOTAL,")

    end_file.write("\n")

    FILE_NAME_FORMAT_1S = "%Y-%m-%d"
    EXTENSION = ".csv"

    DELIM = ","


    def output_line_get_1s(words):
        out_line = words[0] + DELIM
        if CURRENT == 1:
            out_line += (words[1] + DELIM + words[2] + DELIM + words[3] + DELIM)
        if VOLTAGE == 1:
            out_line += (words[4] + DELIM + words[5] + DELIM + words[6] + DELIM)
        if FREQUENCY == 1:
            out_line += (words[7] + DELIM + words[8] + DELIM + words[9] + DELIM)
        if POWER == 1:
            try:
                out_line += (words[10] + DELIM + words[11] + DELIM + words[12] + DELIM + words[13] + DELIM)
            except:
                out_line += ("" + DELIM + "" + DELIM + "" + DELIM + "" + DELIM)
        return out_line


    FORMAT = "%Y-%m-%d %H:%M:%S"

    delta = timedelta(days=1)
    curr_date = start_date
    while curr_date <= end_date:
        file_path = directory + curr_date.strftime(FILE_NAME_FORMAT_1S) + EXTENSION
        if os.path.exists(file_path) is False:
            curr_date += delta
            continue
        file = open(file_path)
        lines = file.readlines()
        lines = lines[1:]
        for line in lines:
            line = line.strip()
            words = line.split(DELIM)
            curr_date_time = datetime.strptime(words[0], FORMAT)
            if curr_date_time < start_date_time:
                continue
            if curr_date_time > end_date_time:
                break
            out_line = output_line_get_1s(words)
            end_file.write(out_line)
            end_file.write("\n")
        file.close()
        curr_date += delta
    end_file.close()

