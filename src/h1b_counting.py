from csv      import DictReader, QUOTE_MINIMAL  # I'm considering csv to be internal.
from operator import itemgetter
from sys      import argv


def sort_dict(input_dict):
    ''' Sort contents of input_dict.
        Sort by number of certified occurrences. If there are ties, sort by number of appearances of keys,
        *alphabetically* by key name. '''

    # Have to copy the dict into a list, because we're unable to retrieve the keys if we sort by the values.
    # After that sorting is simple. Sorting two lists sorts by first item, then second, etc.
    to_be_sorted = []
    for key in input_dict.keys():
        to_be_sorted = [(key, input_dict[key])] + to_be_sorted
    intermediate_sort = sorted(to_be_sorted, key=itemgetter(0))
    final_sort = sorted(intermediate_sort, key=itemgetter(1), reverse=True)

    return final_sort



def output_results(filename, final_sort, total_certs, is_states):
    ''' Output `final_sort` to `filename`. `total_certs` is used to compute percentage of certified for this
        key out of all certified items. `is_state` determines value of first column in first row. '''
    if is_states:
        first_column = 'TOP_STATES'
    else:
        first_column = 'TOP_OCCUPATIONS'

    # Follow this output format description:
    #     First line:
    #         TOP_OCCUPATIONS or TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
    #     Subsequent lines:
    #         occupation or state;number certified applications;percentage of applications
    #     where percentage of applications = those certified / total_certs rounded to tenths and
    #     formatted to one decimal point.
    with open(filename, 'w') as outfile:
        outfile.write(first_column + ';NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for (key, value) in final_sort[:10]:
            ## Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and
            ## 1.04% should be rounded to 1.0%.
            # Add .00009 to try to ensure that rounding works. It won't affect actual rounding, but ought to
            # ensure things don't round down when they shouldn't: vagueries of floats.
            percentage = round(value[0] / total_certs + .000009, 3) * 100

            # Have to add formatting on percentage because every once in a while
            # the rounding leaves some horrible 15-digit floating point stuff.
            outfile.write( '{};{};{:.1f}%\n'.format(key, value[0], percentage) ) # 1% should be represented by 1.0%



def main():
    ''' Get input from `input_filename`, count both soc's and states, also count number of each that is certified.
        Keep track of total certifications. Call `sort_dict()` and `output_results()` to output results to `occup_output_filename` and
        `state_output_filename`. See docs in `sort_dict()` and `output_results()` for sorting and output instructions. '''
    input_filename        = argv[1]
    occup_output_filename = argv[2]
    state_output_filename = argv[3]

# # Input Dataset

    # states and soc_names are dictionaries with
    #   key:   state names or occupation, respectively
    #   value: list of lenth 2: [total certifications for this key, number of occurences of this key]
    # order of items in list is for sorting, as sort procedes in order of items in list.
    states      = dict()
    soc_names   = dict()
    total_certs = 0

    with open(input_filename) as input_stream:
        # Note: Each year of data can have different columns. Check **File Structure** docs before development.
        # Because of this I am using DictReader, which references by header name.
        # If I were worried that the headers might sometimes be lowercase I'd need to use csv.reader and capture
        # the first line as column headers to get column indices
        reader = DictReader(input_stream, delimiter=';')
        for row in reader:
            # For each row, collect soc name, state, and status. Store total number of certified cases in accumulator.
            # Following code is duped, but seems reasonable to avoid extra fn calls.
            try:
                soc_names[row['SOC_NAME']][1] += 1
            except:
                soc_names[row['SOC_NAME']] = [0,1] # 0 certs, 1 soc
            try:
                states[row['WORKSITE_STATE']][1] += 1
            except:
                states[row['WORKSITE_STATE']] = [0,1] # 0 certs, 1 state

            # I know I've created the appropriate lists at this point, so I can just add to certification counts.
            if row['CASE_STATUS'].lower() == 'certified':
                soc_names[row['SOC_NAME']][0]    += 1
                states[row['WORKSITE_STATE']][0] += 1
                total_certs                      += 1

    to_output = sort_dict(states)
    output_results(state_output_filename, to_output, total_certs, True)
    to_output = sort_dict(soc_names)
    output_results(occup_output_filename, to_output, total_certs, False)


def main2():
    ''' More flexible version of main(), where we can't use the header names in csv library because they vary by year. In this
        case we need to find the index of each header first, then pull those indices on each read. Rest is same:
        Get input from `input_filename`, count both soc's and states, also count number of each that is certified.
        Keep track of total certifications. Call `sort_dict()` and `output_results()` to output results to `occup_output_filename` and
        `state_output_filename`. See docs in `sort_dict()` and `output_results()` for sorting and output instructions. '''
    input_filename        = argv[1]
    occup_output_filename = argv[2]
    state_output_filename = argv[3]

# # Input Dataset

    # states and soc_names are dictionaries with
    #   key:   state names or occupation, respectively
    #   value: list of lenth 2: [total certifications for this key, number of occurences of this key]
    # order of items in list is for sorting, as sort procedes in order of items in list.
    states      = dict()
    soc_names   = dict()
    total_certs = 0

    # Multiple years have different headers. I need to read the headers and find the correct header names.
    # This is a little dicey, as they change year to year, see for instance the state. This works for
    # 2013 forward.
    with open(input_filename) as input_stream:
        first_line = input_stream.readline()
    first_line = first_line.split(';')
    for position in first_line:
        position = position.lower() # Saves an infinitesimal amount of time, but also code is cleaner.
                                    # And maybe some years are in lowercase?
        # print(position)
        if position.find('soc_name') >= 0:
            # print('soc_name', position)
            soc_name = position.upper()
        elif position.find('state') >= 0:
            # print('state', position)
            if position.find('worksite') >= 0 or position.find('workloc1') >= 0:
                # print('state', position)
                state = position.upper()
        elif position.find('status') >= 0:
            # print('soc_status', position)
            soc_status = position.upper()

    with open(input_filename) as input_stream:
        # Note: Each year of data can have different columns. Check **File Structure** docs before development.
        # Because of this I am using DictReader, which references by header name.
        # If I were worried that the headers might sometimes be lowercase I'd need to use csv.reader and capture
        # the first line as column headers to get column indices
        reader = DictReader(input_stream, delimiter=';')
        for row in reader:
            # For each row, collect soc name, state, and status. Store total number of certified cases in accumulator.
            # Following code is duped, but seems reasonable to avoid extra fn calls.
            try:
                soc_names[row[soc_name]][1] += 1
            except:
                soc_names[row[soc_name]] = [0,1] # 0 certs, 1 soc
            try:
                states[row[state]][1] += 1
            except:
                states[row[state]] = [0,1] # 0 certs, 1 state

            # I know I've created the appropriate lists at this point, so I can just add to certification counts.
            if row[soc_status].lower() == 'certified':
                soc_names[row[soc_name]][0] += 1
                states[row[state]][0]       += 1
                total_certs                 += 1

    to_output = sort_dict(states)
    output_results(state_output_filename, to_output, total_certs, True)
    to_output = sort_dict(soc_names)
    output_results(occup_output_filename, to_output, total_certs, False)


if __name__ == "__main__": main()
