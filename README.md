# Eric Ford
## Insight H1B solution

## Problem

### Overview

Allow quick identification of top occupations and most popular states for approved for H1B visas. csv files can be found here [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years.

In a nutshell, compile **Top 10 Occupations** and **Top 10 States** for **certified** visa applications from semicolon delineated csv files formatted as above.

### Requested output format

The output should be of the following format:

Two output files:
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications

Each line holds one record and each field on each line is separated by a semicolon (;).

Each line of the `top_10_occupations.txt` file should contain these fields in this order:
1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's Standard Occupational Classification (SOC) code
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `Certified`
3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation.

The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__. Recall that `TOP_OCCUPATIONS` is the total number of applications for that occupation, _not_ the number of certified applications.

Each line of the `top_10_states.txt` file should contain these fields in this order:
1. __`TOP_STATES`__: State where the work will take place
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state. An application is considered certified if it has a case status of `Certified`
3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of certified applications regardless of state.

The records in this file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__ field, and in case of a tie, alphabetically by __`TOP_STATES`__. Recall that `TOP_STATES` is the total number of applications for that state, _not_ the number of certified applications.

There should be at most 10 lines in each file. In case of ties, only list the top 10 based on the sorting instructions given above.

Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and 1.04% should be rounded to 1.0%. Also, 1% should be represented by 1.0%



## Approach

1. Use two hash tables (dictionaries), one with states as keys, one with occupations.
    For each key store a list with values [total certs for this key, number of occurences of this key]
1. Read data stream from file(s) one row at a time.
1. Gather three fields for each row: `CASE_STATUS`, `SOC_NAME`, `WORKSITE_STATE`.
1. Add new keys to hashes if `SOC_NAME` or `WORKSITE_STATE` has not been encountered.
1. Increment if `CASE_STATUS` is certified, accumulate into hash values and total certs.
1. When end of file is reached, sort alphabetically by name, then by key in order of occurences, then by key in order of number of certs.
1. Output first ten items in sorted list to files in appropriate format.

### Issues

1. Proper use of the provided `run.sh` script does not allow for one request, which is that any files put into the input folder should be run without modifications to the code. However, `run.sh`, itself, would need to be modded. Is that correct usage?
1. Cannot use requested directory structure, as any additional directories placed in `insight_testsuite > tests` will also run with the provided testing shell script and fail.

Neither of these issues was resolved, as the time involved in (re)learning shell scripting was deemed excessive.


## To run

1. Put input file(s) into `input` directory.
1. Edit shell script `run.sh` to have correct input and output file names.
1. Run shell script.
