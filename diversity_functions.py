

def dc_summarizePoly(poly, lyrPoint, fldSpecies):
    ##############################################################
    #
    # This function takes as inputs the following parameters:
    #     poly       = a single polygon QgsFeature
    #     lyrPoint   = a QgsVectorLayer contaning points. Each 
    #                  point represents a single observation of a 
    #                  species.
    #     fldSpecies = a string contaning the name of the field
    #                  in the points layer that contains the name 
    #                  of the species
    #
    # The purpose of the function is to summarize the number of 
    # observations of each species insedie the polygon in the form
    # of a dictionary containing species as keys and the number of 
    # observations as values.

    dctPoly = {}

    # loop through all the points that intersect the polygons bounding box

    for obs in lyrPoint.getFeatures(poly.geometry().boundingBox()):
        # check to see if the point is actually inside the polygon
        if poly.geometry().contains(obs.geometry()):
            # get the name of the species as a string variable
            sSpecies = obs.attribute(fldSpecies)
            # check to see if the species already has an entry in the dictionary
            if sSpecies in dctPoly.keys():
                # if it does, increas the count to 1
                dctPoly[sSpecies] += 1
            else:
                # if there is no entry for the species, create it and set its
                # initial value to 1
                dctPoly[sSpecies] = 1
    
    return dctPoly


def dc_mergeDictionaries(dMain, cat, dPoly):
    ##############################################################
    #
    # This function takes as inputs the following parameters:
    #     dMain      = a dictionary with categories as the key and another
    #                  dictionary containing summary information as the value 
    #     cat        = a string containing the name of the category to be merged
    #     dPoly      = a dictionary containing summary information for a polygon
    #                  (created by the dc_processPoly function). The keys are the 
    #                  names of the species occuring in the polygon and the values 
    #                  are the number of observations of that species in the polygon
    #
    # The purpose of the function is to merge the species counts from dPoly into
    # the appropriate summary information in dMain.

    # check to see if the category exists in the dMain dictionary

    if cat in dMain.keys():
        # if it does then loop through the summary data in dPoly
        for species, obs in dPoly.items():
            # check to see if there is already an entry for the species in this category
            if species in dMain[cat].keys():
                # if there is then add the number of observations in the summary data
                dMain[cat][species] += obs
            else:
                # if there isn't then create a new entry for the species and set the
                # number of observations as the initial value
                dMain[cat][species] = obs
    else:
        # if it doesn't then create an entry for the category with the summary
        # dictionary as the initial value
        dMain[cat] = dPoly

    return dMain