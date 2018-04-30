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

class TEDLData(object):
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
        id = 0
        for line in raw:
            id = id +1
            rawrow, pickedrow = self.getrowdata(line,id)
            rawdata.append(rawrow)
            pickeddata.append(pickedrow)
        
        return rawdata, pickeddata

    def getrowdata(self, row,id):
        """ 
        method to deal with a sigle record from the database
        this method would return two dicts, rawrow and pickedrow
        rawrow is crafted from the original rows from the database 
        pickedrow is a subset of the rawrow filtered by user configurated attributes
        """
        rawrow = {
            'id':id,
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
            
        return listdata, self.formula, self.attributes
    
    def dict(self):
        return self.data
        

class Sampling(object):
    def __init__(self,X_attr,Y_attr,filter = None, test_proportion = 0.1,X_normalize = True, Y_normalize = False):
        '''
        '''
        raw_X, raw_X_formula, self.features = TEDLData(X_attr).array()
        raw_Y, raw_Y_formula, self.targets = TEDLData(Y_attr).array()
        if raw_X_formula == raw_Y_formula:
            formula = raw_X_formula
        else:
            raise ValueError
        filter_ind = [i for i in range(len(formula)) if filter_formula(formula[i], filter)]
        
        if len(filter_ind) == 0:
            print("No filtered result.")
            raise ValueError
        self.formula = [formula[x] for x in filter_ind]
        self.raw_X = [raw_X[x] for x in filter_ind]
        self.raw_Y = [raw_Y[x] for x in filter_ind]

        self.norm_X = normalize(self.raw_X,X_normalize)
        self.norm_Y = normalize(self.raw_Y,Y_normalize)
        
        test_index = random.sample(range(len(self.formula)), int(test_proportion*len(self.formula)))
        train_index = [x for x in range(len(self.formula)) if x not in test_index]

        self.train_X = [self.norm_X[x] for x in train_index]
        self.train_y = [self.norm_Y[x] for x in train_index]
        self.train_formula = [self.formula[x] for x in train_index]
        self.test_X = [self.norm_X[x] for x in test_index]
        self.test_y = [self.norm_Y[x] for x in test_index]
        self.test_formula = [self.formula[x] for x in test_index]
                
    #def data(self):
    #    return self.train_X, self.test_X, self.train_Y, self.test_Y, self.test_formula


def filter_formula(formula, filter):
    if filter:
        elements=filter.split()
        for element in elements:
            if element.lower() not in formula.lower():
                return False
        return True
    else:
        return True


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
        if max(raw_tmp)>min(raw_tmp):
            norm_tmp = [(x-min(raw_tmp))/(max(raw_tmp)-min(raw_tmp)) for x in raw_tmp]
        else:
            norm_tmp = raw_tmp
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
            if ex in tmp:
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
    test = Sampling('structure-B', 'B', filter='Al S O', X_normalize = False, Y_normalize = False)
    print(test.formula)
    print(test.train_X)
    print(len(test.formula))
    print(test.features)
    print(test.targets)
