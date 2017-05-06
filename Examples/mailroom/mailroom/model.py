#!/usr/bin/env python
"""
models for the mailroom program.

This is where the programlogic is.

This version has been made mroe Object oriented.
"""

import sys
import math

# handy utility to make pretty printing easier
from textwrap import dedent


# In memory representation of the donor database
# using a tuple for each donor
# -- kind of like a record in a database table
# using a dict with a lower case version of the donor's name as the key
# This makes it easier to have a 'normalized' key.
#  you could get a bit fancier by having each "record" be a dict, with
#   "name" and "donations" as keys.

def get_sample_data():
    """
    returns a list of donor objects to use as sample data

    """
    return [Donor("William Gates III", [653772.32, 12.17]),
            Donor("Jeff Bezos", [877.33]),
            Donor("Paul Allen", [663.23, 43.87, 1.32]),
            Donor("Mark Zuckerberg", [1663.23, 4300.87, 10432.0]),
            ]


class Donor:
    """
    class to hold the information about a single donor
    """

    def __init__(self, name, donations=None):
        """
        create a new Donor object
        
        :param name: the full name of the donor

        :param donations=None: iterable of past donations
        """

        self.norm_name = self._normalize_name(name)
        self.name = name
        if donations is None:
            self.donations = []
        else:
            self.donations = list(donations)


    @staticmethod
    def _normalize_name(name):
        """
        return a normalized version of a name to use as a comparison key

        simple enough to not be in a method now, but maybe you'd want to make it fancier later.
        """
        return name.lower()

    @property
    def last_donation(self):
        """
        The most recent donation made
        """
        return self.donations[-1]

    def add_donation(self, amount):
        """
        add a new donation
        """
        # fixme: this would be a good palce to do some error checking!
        self.donations.append(float(amount))


class DonorDB:
    """
    encapsulation of the entire database of donors and data associated with them.
    """

    def __init__(self, donors=None):
        """
        Initialize a new donor database

        :param donors=None: iterable of Donor objects
        """
        if donors is None:
            self.donor_data = {}
        else:
            self.donor_data = {d.norm_name:d for d in donors}


    def list_donors(self):
        """
        creates a list of the donors as a string, so they can be printed

        Not calling print from here makes it more flexible and easier to
        test
        """
        listing = ["Donor list:"]
        for donor in self.donor_data.values():
            listing.append(donor.name)
        return "\n".join(listing)


    def find_donor(self, name):
        """
        find a donor in the donor db

        :param: the name of the donor

        :returns: The donor data structure -- None if not in the self.donor_data
        """
        key = name.strip().lower()
        return self.donor_data.get(key)


    def add_donor(self, name):
        """
        Add a new donor to the donor db

        :param: the name of the donor

        :returns: the new Donor data structure
        """
        name = name.strip()
        donor = (name, [])
        self.donor_data[name.lower()] = donor
        return donor


    def gen_letter(self, donor):
        """
        Generate a thank you letter for the donor

        :param: donor tuple

        :returns: string with letter

        note: This doesn't actually write to a file -- that's a separate
              function. This makes it more flexible and easier to test.
        """
        return dedent('''Dear {0:s},

              Thank you for your very kind donation of ${1:.2f}.
              It will be put to very good use.

                             Sincerely,
                                -The Team
              '''.format(donor.name, donor.last_donation)
              )



    @staticmethod
    def sort_key(item):
        # used to sort on name in self.donor_data
        return item[1]


    def generate_donor_report(self):
        """
        Generate the report of the donors and amounts donated.

        :returns: the donor report as a string.
        """
        # First, reduce the raw data into a summary list view
        report_rows = []
        #fixme - make the donor db directly iterable?
        for donor in self.donor_data.values():
            name = donor.name
            gifts = donor.donations
            total_gifts = sum(gifts)
            num_gifts = len(gifts)
            avg_gift = total_gifts / num_gifts
            report_rows.append((name, total_gifts, num_gifts, avg_gift))

        # sort the report data
        report_rows.sort(key=self.sort_key)
        report = []
        report.append("{:25s} | {:11s} | {:9s} | {:12s}".format("Donor Name",
                                                                "Total Given",
                                                                "Num Gifts",
                                                                "Average Gift"))
        report.append("-" * 66)
        for row in report_rows:
            report.append("{:25s}   ${:10.2f}   {:9d}   ${:11.2f}".format(*row))
        return "\n".join(report)


    def save_letters_to_disk(self):
        """
        make a letter for each donor, and save it to disk.
        """
        for donor in self.donor_data.values():
            print("donor:", donor)
            letter = self.gen_letter(donor)
            # I don't like spaces in filenames...
            filename = donor.name.replace(" ", "_") + ".txt"
            open(filename, 'w').write(letter)