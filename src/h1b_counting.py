# A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visas.

# As a data engineer, you are asked to create a mechanism to analyze past years' data, specificially calculate two metrics:
# **Top 10 Occupations** and
# **Top 10 States** for **certified** visa applications.

# Your code should be modular and reusable for future. If the newspaper gets data for the year 2019
# (with the assumption that the necessary data to
# calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script
# should produce the results in the `output` folder
# without needing to change the code.

from csv      import DictReader, QUOTE_MINIMAL  # I'm considering csv to be internal.
from sys      import argv
# ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt

def output_to_file(filename, input_dict, total_certs, is_states):
    ''' Output contents of `dictionary` to output file denoted by `filename`.
        This is O(1) memory because all Python argument passing is by reference and the output to a
        stream is buffered and the buffer is cleared at consistent sizes.
        Follow this output format description:
        First line:
            TOP_OCCUPATIONS for TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        Subsequent lines:
            occupation or state;number certified applications;percentage of applications
        where percentage of applications = those certified / total_certs rounded to tenths and
        formatted to one decimal point. '''
    if is_states:
        first_column = 'TOP_STATES'
    else:
        first_column = 'TOP_OCCUPATIONS'
    with open(filename) as outfile:
        outfile.write(first_column + ';NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for i in soc_names.keys():
            # Here I do some "fancy" math to make sure rounding is correct. I'm truncating at 2 decimal places
            # before rounding.
            intermediate = int(input_dict[i][1] / total_certs * 100)
            percentage   = round(intermediate / 100, 1)
            outfile.write( '{};{};{};{f.1}%'.format(input_dict[i][0], input_dict[i][1], percentage) )
        print('\noccupations:')
        print('{:>35}{:>10}{:>10}{:>16}'.format('occupation','how many', 'certs', 'certs ratio'))
        for i in soc_names.keys():
            print( '{:>35}{:>10}{:>10}{:>15}%'.format(i, soc_names[i][0], soc_names[i][1], soc_names[i][1] / total_certs) )
        print('\nstates:')
        print('{:>5}{:>10}{:>10}{:>16}'.format('state','how many', 'certs', 'certs ratio'))
        for i in states.keys():
            print( '{:>5}{:>10}{:>10}{:>15}%'.format(i, states[i][0], states[i][1], states[i][1] / total_certs) )
        print( '\ntotal certs:' + str(total_certs) )
        # print(row['SOC_NAME'], row['WORKSITE_STATE'], row['CASE_STATUS'])



def main():
    input_filename        = argv[1]
    # occup_output_filename = argv[2]
    # state_output_filename = argv[3]

# # Input Dataset

    # states and soc_names are dictionaries with
    #   key:   state names or occupation, respectively
    #   value: list of lenth 2: [number of occurences of this key, total certifications for this key]
    # categories, respectively. Each
    states      = dict()
    soc_names   = dict()
    total_certs = 0
    with open(input_filename) as input_stream:
        # **Note:** Each year of data can have different columns. Check **File Structure** docs before development.
        # Because of this I am using DictReader, which references by header name.
        # If I was worried that the headers might sometimes be lowercase I'd need to use csv.reader and capture
        # the first line as column headers to get column indices
        reader = DictReader(input_stream, delimiter=';')
        for row in reader:
            # For each row, collect soc name, state, and status. Store total number of certified cases in accumulator.
            # Following code is duped, but seems reasonable to avoid extra fn calls.
            try:
                soc_names[row['SOC_NAME']][0] += 1
            except:
                soc_names[row['SOC_NAME']] = [1,0]
            try:
                states[row['WORKSITE_STATE']][0] += 1
            except:
                states[row['WORKSITE_STATE']] = [1,0]

            # I know I've created the appropriate lists at this point, so I can just add to certification counts.
            if row['CASE_STATUS'].lower() == 'certified':
                soc_names[row['SOC_NAME']][1]    += 1
                states[row['WORKSITE_STATE']][1] += 1
                total_certs                      += 1

    # Each line of the `top_10_occupations.txt` file should contain these fields in this order:
    # 1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's
    #       Standard Occupational Classification (SOC) code
    # 2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation.
    #       An application is considered certified if it has a case status of `Certified`
    # 3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified
    #       applications regardless of occupation.
    print('\noccupations:')
    print('{:>35}{:>10}{:>10}{:>16}'.format('occupation','how many', 'certs', 'certs ratio'))
    for i in soc_names.keys():
        intermediate = int(soc_names[i][1] / total_certs * 100)
        percentage   = round(intermediate / 100, 1)
        print( '{:>35}{:>10}{:>10}{:>15}%'.format(i, soc_names[i][0], soc_names[i][1], percentage) )
    print('\nstates:')
    print('{:>5}{:>10}{:>10}{:>16}'.format('state','how many', 'certs', 'certs ratio'))
    for i in states.keys():
        intermediate = int(states[i][1] / total_certs * 100)
        percentage   = round(intermediate / 100, 1)
        print( '{:>5}{:>10}{:>10}{:>15}%'.format(i, states[i][0], states[i][1], percentage) )
    print( '\ntotal certs:' + str(total_certs) )
    # print(row['SOC_NAME'], row['WORKSITE_STATE'], row['CASE_STATUS'])


# Instructions

# Only use the default data structures that come with Python.
# For example, you should not use Pandas or other external libraries.

# # Output

# Your program must create 2 output files:
# * `top_10_occupations.txt`: Top 10 occupations for certified visa applications
# * `top_10_states.txt`: Top 10 states for certified visa applications

# Each line holds one record and each field on each line is separated by a semicolon (;).

# Each line of the `top_10_occupations.txt` file should contain these fields in this order:
# 1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's
#       Standard Occupational Classification (SOC) code
# 2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation.
#       An application is considered certified if it has a case status of `Certified`
# 3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified
#       applications regardless of occupation.

# The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie,
# alphabetically by __`TOP_OCCUPATIONS`__.

# Each line of the `top_10_states.txt` file should contain these fields in this order:
# 1. __`TOP_STATES`__: State where the work will take place
# 2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state.
#       An application is considered certified if it has a case status of `Certified`
# 3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of
#       certified applications regardless of state.

# The records in this file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__ field, and in case of a tie,
# alphabetically by __`TOP_STATES`__.

# Depending on the input (e.g., see the example below), there may be fewer than 10 lines in each file.
# There, however, should not be more than 10 lines in each file. In case of ties, only list the top 10
# based on the sorting instructions given above.

# Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and
# 1.04% should be rounded to 1.0%.
# Also, 1% should be represented by 1.0%

if __name__ == "__main__": main()
