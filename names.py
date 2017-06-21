# names.py
# Dula Gender Project
# NaLette Brodnax
# www.nalettebrodnax.com
# June 14, 2017


import csv
import re
import string


def main():
    # columns for input files
    name_fields = ["id", "ez_file", "name", "title", "source_file"]
    org_fields = ["org_id", "ez_file", "ein", "fy", "org_name", "city",
                  "state", "zip", "contributions", "revenue", "grants",
                  "compensation", "fundraising", "expenses", "year_excess",
                  "assets_eoy"]

    # columns for output file
    out_fields = ["id", "ez_file", "name", "title", "source_file",
                  "salutation", "first_name", "last_name", "suffix",
                  "org_name", "fy"]

    # combine data sets
    with open("personnel.csv", 'r') as name_file, \
            open("orgs.csv", 'r') as org_file, \
            open("output.csv", 'w') as out_file:

        writer = csv.DictWriter(out_file, fieldnames=out_fields)
        writer.writeheader()

        org_reader = csv.DictReader(org_file, fieldnames=org_fields)
        next(org_reader, None)
        orgs = {}
        for rowdict in org_reader:
            if None in rowdict:
                del rowdict[None]
            org_id = rowdict.pop("org_id")
            orgs[org_id] = rowdict

        name_reader = csv.DictReader(name_file, fieldnames=name_fields)
        next(name_reader, None)
        row_counter = 0
        error_counter = 0
        key_error_counter = 0
        for row in name_reader:
            crosswalk = row["id"]
            try:
                names = format_name(row["name"])
                row["salutation"] = names[0]
                row["first_name"] = names[1]
                row["last_name"] = names[2]
                row["suffix"] = names[3]
            except IndexError:
                error_counter += 1
                row["salutation"] = ""
                row["first_name"] = ""
                row["last_name"] = ""
                row["suffix"] = ""
            try:
                row["org_name"] = orgs[crosswalk]["org_name"]
                row["fy"] = orgs[crosswalk]["fy"]
            except KeyError:
                key_error_counter += 1

            writer.writerow(row)
            row_counter += 1
        print("Rows processed: " + str(row_counter))
        print("Format errors: " + str(error_counter))
        print("Key errors: " + str(key_error_counter))

        # test the name formatting functions
        test = ['NaLette M. Brodnax', 'Dr N Brodnax',
                'NaLette Michelle Brodnax', 'David Brodnax, Jr.',
                'Dr Patty Cunningham, Jr', 'N. M. Brodnax',
                'Brodnax, NaLette', 'Brodnax, Jr, David',
                'Brodnax, NaLette M.']
        # format_name_test(test)
        for name in test:
            print(format_name(name))


def split_reversed_name(name_string):
    re_comma = r'(\w+),( \w+\.?,)? (.*)'
    comma_match = re.match(re_comma, name_string, re.I)
    if comma_match:
        last = comma_match.group(1)
        suffix = comma_match.group(2)
        remainder = comma_match.group(3)
        return [last, suffix, remainder]
    else:
        return []


def split_salutation(name_string):
    re_salutation = r'(mr|mrs|ms|miss|rev|dr)\.? (.*)'
    salutation_match = re.match(re_salutation, name_string, re.I)
    # identify first name and remove punctuation if necessary
    if salutation_match:
        salutation = salutation_match.group(1)
        remainder = salutation_match.group(2)
        return [salutation, remainder]
    else:
        return []


def split_suffix(name_string):
    re_suffix = r'(.*) (jr|sr|i+)\.?'
    suffix_match = re.match(re_suffix, name_string, re.I)
    if suffix_match:
        suffix = suffix_match.group(2)
        remainder = suffix_match.group(1)
        return [suffix, remainder]
    else:
        return []


def remove_punctuation(name_list):
    new_name_list = []
    for name in name_list:
        if name:
            new_name_list.append(re.sub('['+string.punctuation+']', '', name))
        else:
            new_name_list.append("")
    return new_name_list


def format_name(name_string):
    """Returns a list with first and last name
    str -> list of str"""
    reverse_check = split_reversed_name(name_string)
    if len(reverse_check) > 0:
        last_name = reverse_check[0]
        suffix = reverse_check[1]
        sal_check = split_salutation(reverse_check[2])
        if len(sal_check) > 0:
            salutation = sal_check[0]
            remainder = sal_check[1]
        else:
            salutation = None
            remainder = reverse_check[2]
        first_name = remainder.split()[0]
    else:
        suffix_check = split_suffix(name_string)
        if len(suffix_check) > 0:
            suffix = suffix_check[0]
            name_string = suffix_check[1]
        else:
            suffix = None
        sal_check = split_salutation(name_string)
        if len(sal_check) > 0:
            salutation = sal_check[0]
            name_string = sal_check[1]
        else:
            salutation = None
        first_name = name_string.split()[0]
        last_name = name_string.split()[-1]
    return remove_punctuation([salutation, first_name, last_name, suffix])


def format_name_test(name_list):
    for name in name_list:
        print("Reverse: " + name + ":" + str(split_reversed_name(name)))
        print("Salutation: " + name + ": " + str(split_salutation(name)))
        print("Suffix: " + name + ": " + str(split_suffix(name)))
        names = name.split()
        print("Punctuation: " + name + ": " + str(remove_punctuation(names)))


if __name__ == '__main__':
    # pass
    main()
