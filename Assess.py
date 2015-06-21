from __future__ import division
import fpformat
import csv

"""
A simple module to assess a dataset of census tracts in Oakland, CA
for Code for America.

Expects the "tracts.txt" file to be located in the same folder.

Returns the list of densities in a CSV file named "densities.txt", tab-delimited.
Returns the densest/sparsest tracts in a txt file named "minMaxDensities.txt".
by Giovanni Prinzivalli
"""

def assessDataset(fn):
    """
    Assesses the csv file provided by CFA.
    Returns the population and housing densities of each place by name,
    as well as the sparsest and densest places.
    """
    
    places = []
    sparsestH = None
    densestH = None
    sparsestP = None
    densestP = None
    
    with open(fn) as f:
        txtReader = csv.DictReader(f, delimiter = "\t")
        for row in txtReader:
            place = evalRow(row)
            places.append(place)
            if sparsestH is None or float(sparsestH[2]) < float(place[2]):
                sparsestH = place
            if sparsestP is None or float(sparsestP[1]) < float(place[1]):
                sparsestP = place
            if densestH is None or float(densestH[2]) > float(place[2]):
                if place[2] == '0.00':
                    pass
                else:
                    densestH = place
            if densestP is None or float(densestP[1]) > float(place[1]):
                if place[1] == '0.00':
                    pass
                else:
                    densestP = place

        return [places, sparsestP, densestP, sparsestH, densestH]


def evalRow(row):
    """
    Finds and returns the housing and population densities
    for a given place along with the place's name.
    
    Density is given in feet per person.
    """
    if row["Population"] == '0':
        densityP = 0
    else:
        densityP = int(row["Land Area"])/int(row["Population"])
    
    if row["Housing Units"] == '0':
        densityH = 0
    else:
        densityH = int(row["Land Area"])/int(row["Housing Units"])
    
    return [row["Name"], fpformat.fix(densityP, 2), fpformat.fix(densityH, 2)]
    
    
if __name__ == "__main__":
    data = assessDataset("tracts.txt")
    with open("minMaxDensities.txt", 'w') as wf:
        wf.write("The sparsest poplation density is at %s with %s square feet per person.\n" % (data[1][0], data[1][1]))
        wf.write("The densest population density is at %s with %s square feet per person.\n" % (data[2][0], data[2][1]))
        wf.write("The sparsest housing density is at %s with %s square feet per house.\n" % (data[3][0], data[3][2]))
        wf.write("The densest housing density is at %s with %s square feet per house.\n" % (data[4][0], data[4][2]))
    with open("densities.txt", 'w') as wf:
        txtWriter = csv.writer(wf, delimiter = "\t")
        txtWriter.writerow(["Name", "Population Density", "Housing Density"])
        for row in data[0]:
            txtWriter.writerow(row)