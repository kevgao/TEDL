#!/usr/bin/python

"""TEDL.data 

This module is used as the data retrival module for all TEDL coding.

"""
__author__ = "Duanfeng Gao"
__email__ = "kevgao@live.com"


import requests
import random
import numpy as np

COM_ATTR = [
    'id',
    'formula',
    'icsd',
    'spacegroup',
    'numofatoms',
    'volume',
    'density',
    'bandgap',
    'B',
    'nbvb',
    'nbcb',
    'dosmassvb',
    'dosmasscb',
    'bandmassvb',
    'bandmasscb',
    'Vol',
    'mass',
    'kappaacoustic',
    'kappaoptical',
    'kappatotal',
    'hmobility',
    'emobility',
    'betasep',
    'betasen',
]

class ComputedData(object):
    """ComputedData Object
    
    Object covering 
    """
    def __init__(self, attr=None):
        """ 
        init method 
        """
        self.attributes = getattributes(attr)
        self.rawdata, self.data = self.getdata()
        self.formula = [x['formula'] for x in self.rawdata]

    def getdata(self):
        """ 
        Get data from database and generate two lists of data points represented by dicts.
        - rawdata: data points consisting of all attributes
        - pickeddata: data points consisting of selected attributes
        """
        rawdata = []
        pickeddata = []
        raw = requests.get('http://tedesignlab.org/plot?elements=').json()
        for line in raw:
            rawrow, pickedrow = self.getrowdata(line)
            rawdata.append(rawrow)
            pickeddata.append(pickedrow)
        
        return rawdata, pickeddata

    def getrowdata(self, row):
        """ 
        method to deal with a sigle record from the database
        this method would return two dicts, rawrow and pickedrow
        rawrow is crafted from the original rows from the database 
        pickedrow is a subset of the rawrow filtered by user configurated attributes
        """
        rawrow = {
            'id':int(0),
            'formula':row['formula'],
            'icsd':row['icsd'],
            'spacegroup':int(row['spacegroup']),
            'numofatoms':int(row['numofatoms']),
            'volume':float(row['volume']),
            'density':float(row['density']),
            'bandgap':float(row['bandgap']),
            'B':float(row['b']),
            'nbvb':float(row['nbvb']),
            'nbcb':float(row['nbcb']),
            'dosmassvb':float(row['dosmassvb']),
            'dosmasscb':float(row['dosmasscb']),
            'bandmassvb':float(row['bandmassvb']),
            'bandmasscb':float(row['bandmasscb']),
            'Vol':float(row['vol']),
            'mass':float(row['mass']),
            'kappaacoustic':float(row['kappaacoustic']),
            'kappaoptical':float(row['kappaoptical']),
            'kappatotal':float(row['kappa']),
            'hmobility':float(row['hmobility']),
            'emobility':float(row['emobility']),
            'betasep':float(row['betasep']),
            'betasen':float(row['betasen']),
            'atomnumdensity':float(row['atomnodensity']),
            'avgatomno':float(row['avgatomno']),
            'avgelectroneg':float(row['avgelectron']),
            'avgmassperatom':float(row['avgmassperatom']),
            'avgnn':float(row['avgnn']),
            'formulaunit':int(row['formulaunit']),
            'heaviestelementmass':float(row['heaviestelementmass']),
            'highestatomno':int(row['highestatomno']),
            'leastelectroneg':float(row['leastelectron']),
            'lightestelementmass':float(row['lightestelementmass']),
            'lowestatomno':int(row['lowestatomno']),
            'maxdiffatomno':float(row['maxdiffatomno']),
            'maxelectronegdiff':float(row['maxelectrondiff']),
            'maxmassdiff':float(row['maxmassdiff']),
            'maxnn':int(row['maxnn']),
            'maxwyckoff':int(row['maxwyckoff']),
            'minnn':int(row['minnn']),
            'minwyckoff':int(row['minwyckoff']),
            'molweight':float(row['molweight']),
            'mostelectroneg':float(row['mostelectron']),
            'stddevelectroneg':float(row['stddevelectron']),
            'stddevmass':float(row['stddevmass']),
            'unitcellmass':float(row['unitcellmass']),
            'anglealpha':float(row['anglealpha']),
            'anglebeta':float(row['anglebeta']),
            'anglegamma':float(row['anglegamma']),
            'latta':float(row['latta']),
            'lattb':float(row['lattb']),
            'lattc':float(row['lattc']),
            
        }
        pickedrow = {}
        for attribute in self.attributes:
            pickedrow[attribute] = rawrow.get(attribute, 0) 
        return rawrow, pickedrow
    
    def array(self):
        """
        Output the array type(list of lists) of the picked data
        """
        listdata = []
        for row in self.data:
            listrow = []
            for attr in self.attributes:
                listrow.append(row[attr])
            listdata.append(listrow)
            
        return listdata,self.formula
    
    def dict(self):
        return self.data

    def attributes(self):
        return self.attributes

class Sample(object):
    def __init__(self,X_attr,Y_attr,test_proportion = 0.1,X_normalize = True, Y_normalize = False):
        self.raw_X,self.formula = ComputedData(X_attr).array()
        self.raw_Y, = ComputedData(Y_attr).array()

        self.norm_X = normalize(self.raw_X,X_normalize)
        self.norm_Y = normalize(self.raw_Y,Y_normalize)
        
        self.train_X = []
        self.train_Y = []
        self.test_X = []
        self.test_Y = []
        self.test_formula=[]

        for i in range(len(self.raw_X)):
            if random.random() <= test_proportion:
                self.test_X.append(self.norm_X[i])
                self.test_Y.append(self.norm_Y[i])
                self.test_formula.append(self.formula[i])
            else:
                self.train_X.append(self.norm_X[i])
                self.train_Y.append(self.norm_Y[i])
                
    def data(self):
        return self.train_X, self.test_X, self.train_Y, self.test_Y, self.test_formula
        

def normalize(raw,normalize):
    if not normalize:
        return raw
    if normalize == 'minmax':
        return minmaxnorm(raw)
    if normalize == 'z-index':
        return minmaxnorm(raw)
    if normalize == True:
        return minmaxnorm(raw)

def minmaxnorm(raw):
    norm = []
    for i in range(len(raw[0])):
        raw_tmp = [x[i] for x in raw]
        norm_tmp = [(x-min(raw_tmp))/(max(raw_tmp)-min(raw_tmp)) for x in raw_tmp]
        norm.append(norm_tmp)
    norm2 = []
    for j in range(len(norm[0])):
        tmp = [x[j] for x in norm]
        norm2.append(tmp)
    return norm2
                
def getattributes(attrstr):
    """ 
    Get the attributes 
    """
    if attrstr == None:
        attr = combineattributes([getpartialattributes('parent'), getpartialattributes('beta')])
    elif isinstance(attrstr, str):
        cstr = attrstr.split('-')
        if(len(cstr) == 1):
            ex = None
        else:
            ex = cstr[1]
        confstr = cstr[0].split('+')
        confs = []
        for conf in confstr:
            tmp=getpartialattributes(conf)
            if ex:
                tmp.remove(ex)
            if tmp:
                confs.append(tmp)
        attr = combineattributes(confs)
    elif isinstance(attrstr, list):
        attr = getpartialattributes(attrstr)

    return attr

def getpartialattributes(attributes):
    """ 
    Get the attributes 
    """
    if attributes == None:
        attr = []
    elif attributes == 'parent':
        attr = [
            'spacegroup',
            'numofatoms',
            'volume',
            'density',
            'bandgap',
            'B',
            'nbvb',
            'nbcb',
            'dosmassvb',
            'dosmasscb',
            'bandmassvb',
            'bandmasscb',
            'Vol',
            'mass',
            'kappaacoustic',
            'kappaoptical',
            'kappatotal',
            'hmobility',
            'emobility',
        ]
        
    elif attributes == 'structure':
        attr = [
            'latta',
            'lattb',
            'lattc',
            'anglealpha',
            'anglebeta',
            'anglegamma',
            'atomnumdensity',
            'avgatomno',
            'avgelectroneg',
            'avgmassperatom',
            'avgnn',
            'formulaunit',
            'heaviestelementmass',
            'heaviestatomno',
            'leastelectroneg',
            'lightestelementmass',
            'lowestatomno',
            'maxdiffatomno',
            'maxelectronegdiff',
            'maxmassdiff',
            'maxnn',
            'maxwyckoff',
            'minnn',
            'minwyckoff',
            'molweight',
            'mostelectroneg',
            'stddevelectroneg',
            'stddevmass',
            'unitcellmass',
        ]
        
    elif attributes == 'beta':
        attr = [
            'betasep',
            'betasen',
        ]
    elif attributes in COM_ATTR:
        attr = [
            attributes,
        ]
    else:
        attr = []
        
    return attr

def combineattributes(attrparts):
    """
    Combine multiple  attribute configuration lists into one single list of configuration.
    """
    attr = []
    for part in attrparts:
        for attrstr in part:
            if attrstr not in attr:
                attr.append(attrstr)
    return attr
    
    
    
    
if __name__ == '__main__':
    test = ComputedData()
