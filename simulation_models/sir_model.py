
#      _                   _ _
#  _____| |__ ___ _ __  _ __(_| |___ _ _
# (_-/ _` / _/ _ | '  \| '_ | | / -_| '_|
# /__\__,_\__\___|_|_|_| .__|_|_\___|_|
#                      |_|
# Copyright (c) 2013-2020 transentis management & consulting. All rights reserved.
#
    
import numpy as np
from scipy.interpolate import interp1d
from scipy.special import gammaln
from scipy.stats import norm
import math, statistics, random, logging
from datetime import datetime
import re
import itertools
from copy import copy, deepcopy



def cartesian_product(listoflists):
    """
    Helper for Cartesian product
    :param listoflists:
    :return:
    """
    if len(listoflists) == 1:
        return listoflists[0]
    res = list(itertools.product(*listoflists))

    if len(res) == 1:
        return res[0]

    return res

def LERP(x,points):
    """
    Linear interpolation between a set of points
    :param x: x to obtain y for
    :param points: List of tuples containing the graphical function's points [(x,y),(x,y) ... ]
    :return: y value for x obtained using linear interpolation
    """
    x_vals = np.array([ x[0] for x in points])
    y_vals = np.array([x[1] for x in points])

    if x<= x_vals[0]:
        return y_vals[0]

    if x >= x_vals[len(x_vals)-1]:
        return y_vals[len(x_vals)-1]

    f = interp1d(x_vals, y_vals)
    return float(f(x))

class simulation_model():
    def __init__(self):
        # Simulation Buildins
        self.dt = 1.0
        self.starttime = 1
        self.stoptime = 1500
        self.units = 'Days'
        self.method = 'Euler'
        self.equations = {

        # Stocks
        
    
        'deathsD'          : lambda t: ( (0.0) if ( t  <=  self.starttime ) else (self.memoize('deathsD',t-self.dt) + self.dt * ( self.memoize('deathRateDr',t-self.dt) )) ),
        'infectiousPopulationI'          : lambda t: ( (120.0) if ( t  <=  self.starttime ) else (self.memoize('infectiousPopulationI',t-self.dt) + self.dt * ( self.memoize('infectionRateIr',t-self.dt) - ( self.memoize('recoveryRateRr',t-self.dt) + self.memoize('deathRateDr',t-self.dt) ) )) ),
        'recoveredPopulationR'          : lambda t: ( (15.0) if ( t  <=  self.starttime ) else (self.memoize('recoveredPopulationR',t-self.dt) + self.dt * ( self.memoize('recoveryRateRr',t-self.dt) )) ),
        'susceptiblePopulationS'          : lambda t: ( (80000000.0) if ( t  <=  self.starttime ) else (self.memoize('susceptiblePopulationS',t-self.dt) + self.dt * ( -1 * ( self.memoize('infectionRateIr',t-self.dt) ) )) ),
        
    
        # Flows
        'deathRateDr'             : lambda t: max([0 , self.memoize('infectiousPopulationI', t) * self.memoize('lethalityL', t)]),
        'infectionRateIr'             : lambda t: max([0 , ( self.memoize('contactRateC', t) * self.memoize('susceptiblePopulationS', t) * self.memoize('infectivityI', t) ) * ( self.memoize('infectiousPopulationI', t) / self.memoize('totalPopulationTp', t) )]),
        'recoveryRateRr'             : lambda t: max([0 , self.memoize('infectiousPopulationI', t) / self.memoize('averageDurationD', t)]),
        
    
        # converters
        'averageDurationD'      : lambda t: 20.0,
        'contactNumber'      : lambda t: self.memoize('contactRateC', t) * self.memoize('infectivityI', t) * self.memoize('averageDurationD', t),
        'contactRateC'      : lambda t: self.memoize('variableContactRate', t),
        'infectivityI'      : lambda t: 0.02,
        'intensiveCareRate'      : lambda t: 0.002,
        'intensiveCareUnitsAvailable'      : lambda t: 30000.0,
        'intensiveCareUnitsNeeded'      : lambda t: self.memoize('infectiousPopulationI', t) * self.memoize('intensiveCareRate', t),
        'lethalityL'      : lambda t: 0.001,
        'netPopulationN'      : lambda t: self.memoize('totalPopulationTp', t) - self.memoize('deathsD', t),
        'reproductionRate'      : lambda t: self.memoize('contactNumber', t) * ( self.memoize('susceptiblePopulationS', t) / self.memoize('totalPopulationTp', t) ),
        'totalPopulationTp'      : lambda t: self.memoize('susceptiblePopulationS', t) + self.memoize('infectiousPopulationI', t) + self.memoize('recoveredPopulationR', t),
        
    
        # gf
        'variableContactRate' : lambda t: LERP(  t , self.points['variableContactRate']),
        
    
        #constants
        
    
    
        }
    
        self.points = {
            'variableContactRate' :  [(1.0, 20.0), (6.878431372549059, 20.0), (12.756862745098118, 20.0), (18.635294117647177, 20.0), (24.513725490196236, 20.0), (30.392156862745296, 20.0), (36.270588235294355, 20.0), (42.14901960784341, 20.0), (48.02745098039247, 20.0), (53.90588235294153, 20.0), (59.78431372549059, 20.0), (65.66274509803965, 20.0), (71.54117647058871, 20.0), (77.41960784313777, 20.0), (83.29803921568681, 20.0), (89.17647058823587, 20.0), (95.05490196078495, 20.0), (100.933333333334, 20.0), (106.81176470588306, 20.0), (112.69019607843211, 20.0), (118.56862745098118, 20.0), (124.44705882353024, 2.0), (130.3254901960793, 20.0), (136.20392156862837, 20.0), (142.08235294117742, 20.0), (147.96078431372646, 20.0), (153.83921568627554, 20.0), (159.71764705882458, 20.0), (165.59607843137363, 20.0), (171.4745098039227, 20.0), (177.35294117647175, 20.0), (183.23137254902085, 20.0), (189.1098039215699, 20.0), (194.98823529411894, 20.0), (200.866666666668, 20.0), (206.74509803921705, 20.0), (212.62352941176613, 20.0), (218.50196078431517, 20.0), (224.38039215686422, 20.0), (230.2588235294133, 20.0), (236.13725490196236, 20.0), (242.0156862745114, 20.0), (247.89411764706048, 20.0), (253.77254901960953, 20.0), (259.6509803921586, 20.0), (265.5294117647077, 20.0), (271.40784313725675, 20.0), (277.28627450980576, 20.0), (283.16470588235484, 20.0), (289.0431372549039, 20.0), (294.9215686274529, 20.0), (300.800000000002, 20.0), (306.6784313725511, 20.0), (312.5568627451001, 20.0), (318.43529411764916, 20.0), (324.31372549019824, 20.0), (330.19215686274725, 20.0), (336.0705882352963, 20.0), (341.9490196078454, 20.0), (347.8274509803945, 20.0), (353.7058823529435, 20.0), (359.5843137254926, 20.0), (365.4627450980417, 20.0), (371.3411764705907, 20.0), (377.2196078431398, 20.0), (383.09803921568886, 20.0), (388.9764705882379, 20.0), (394.85490196078695, 20.0), (400.733333333336, 20.0), (406.61176470588504, 20.0), (412.4901960784341, 20.0), (418.3686274509832, 20.0), (424.24705882353226, 20.0), (430.1254901960813, 20.0), (436.00392156863035, 20.0), (441.8823529411794, 20.0), (447.76078431372844, 20.0), (453.6392156862775, 20.0), (459.5176470588266, 20.0), (465.39607843137566, 20.0), (471.27450980392473, 20.0), (477.1529411764738, 20.0), (483.0313725490228, 20.0), (488.9098039215719, 20.0), (494.78823529412097, 20.0), (500.66666666667, 20.0), (506.54509803921906, 20.0), (512.4235294117682, 20.0), (518.3019607843172, 20.0), (524.1803921568663, 20.0), (530.0588235294153, 20.0), (535.9372549019644, 20.0), (541.8156862745135, 20.0), (547.6941176470625, 20.0), (553.5725490196115, 20.0), (559.4509803921607, 20.0), (565.3294117647097, 20.0), (571.2078431372587, 20.0), (577.0862745098078, 20.0), (582.9647058823568, 20.0), (588.8431372549059, 20.0), (594.721568627455, 20.0), (600.600000000004, 20.0), (606.478431372553, 20.0), (612.3568627451021, 20.0), (618.2352941176512, 20.0), (624.1137254902002, 20.0), (629.9921568627493, 20.0), (635.8705882352983, 20.0), (641.7490196078473, 20.0), (647.6274509803965, 20.0), (653.5058823529455, 20.0), (659.3843137254945, 20.0), (665.2627450980436, 20.0), (671.1411764705927, 20.0), (677.0196078431418, 20.0), (682.8980392156908, 20.0), (688.7764705882398, 20.0), (694.654901960789, 20.0), (700.533333333338, 20.0), (706.411764705887, 20.0), (712.2901960784361, 20.0), (718.1686274509852, 20.0), (724.0470588235343, 20.0), (729.9254901960834, 20.0), (735.8039215686324, 20.0), (741.6823529411814, 20.0), (747.5607843137306, 20.0), (753.4392156862796, 20.0), (759.3176470588286, 20.0), (765.1960784313777, 20.0), (771.0745098039267, 20.0), (776.9529411764757, 20.0), (782.8313725490249, 20.0), (788.7098039215739, 20.0), (794.5882352941229, 20.0), (800.466666666672, 20.0), (806.345098039221, 20.0), (812.2235294117701, 20.0), (818.1019607843192, 20.0), (823.9803921568682, 20.0), (829.8588235294172, 20.0), (835.7372549019664, 20.0), (841.6156862745154, 20.0), (847.4941176470645, 20.0), (853.3725490196135, 20.0), (859.2509803921625, 20.0), (865.1294117647117, 20.0), (871.0078431372607, 20.0), (876.8862745098097, 20.0), (882.7647058823588, 20.0), (888.6431372549079, 20.0), (894.5215686274569, 20.0), (900.400000000006, 20.0), (906.278431372555, 20.0), (912.156862745104, 20.0), (918.0352941176532, 20.0), (923.9137254902023, 20.0), (929.7921568627513, 20.0), (935.6705882353004, 20.0), (941.5490196078495, 20.0), (947.4274509803985, 20.0), (953.3058823529476, 20.0), (959.1843137254966, 20.0), (965.0627450980456, 20.0), (970.9411764705948, 20.0), (976.8196078431438, 20.0), (982.6980392156928, 20.0), (988.5764705882419, 20.0), (994.454901960791, 20.0), (1000.33333333334, 20.0), (1006.2117647058891, 20.0), (1012.0901960784381, 20.0), (1017.9686274509871, 20.0), (1023.8470588235363, 20.0), (1029.7254901960853, 20.0), (1035.6039215686344, 20.0), (1041.4823529411833, 20.0), (1047.3607843137327, 20.0), (1053.2392156862816, 20.0), (1059.1176470588307, 20.0), (1064.9960784313796, 20.0), (1070.8745098039287, 20.0), (1076.7529411764776, 20.0), (1082.631372549027, 20.0), (1088.509803921576, 20.0), (1094.388235294125, 20.0), (1100.266666666674, 20.0), (1106.145098039223, 20.0), (1112.023529411772, 20.0), (1117.9019607843213, 20.0), (1123.7803921568702, 20.0), (1129.6588235294194, 20.0), (1135.5372549019683, 20.0), (1141.4156862745174, 20.0), (1147.2941176470665, 20.0), (1153.1725490196156, 20.0), (1159.0509803921645, 20.0), (1164.9294117647137, 20.0), (1170.8078431372626, 20.0), (1176.6862745098117, 20.0), (1182.5647058823608, 20.0), (1188.44313725491, 20.0), (1194.3215686274589, 20.0), (1200.200000000008, 20.0), (1206.078431372557, 20.0), (1211.956862745106, 20.0), (1217.8352941176552, 20.0), (1223.7137254902043, 20.0), (1229.5921568627534, 20.0), (1235.4705882353023, 20.0), (1241.3490196078515, 20.0), (1247.2274509804004, 20.0), (1253.1058823529497, 20.0), (1258.9843137254986, 20.0), (1264.8627450980478, 20.0), (1270.7411764705967, 20.0), (1276.6196078431458, 20.0), (1282.4980392156947, 20.0), (1288.376470588244, 20.0), (1294.254901960793, 20.0), (1300.133333333342, 20.0), (1306.011764705891, 20.0), (1311.89019607844, 20.0), (1317.768627450989, 20.0), (1323.6470588235384, 20.0), (1329.5254901960873, 20.0), (1335.4039215686364, 20.0), (1341.2823529411853, 20.0), (1347.1607843137344, 20.0), (1353.0392156862836, 20.0), (1358.9176470588327, 20.0), (1364.7960784313816, 20.0), (1370.6745098039307, 20.0), (1376.5529411764796, 20.0), (1382.4313725490288, 20.0), (1388.309803921578, 20.0), (1394.188235294127, 20.0), (1400.066666666676, 20.0), (1405.945098039225, 20.0), (1411.823529411774, 20.0), (1417.701960784323, 20.0), (1423.5803921568722, 20.0), (1429.4588235294214, 20.0), (1435.3372549019705, 20.0), (1441.2156862745194, 20.0), (1447.0941176470685, 20.0), (1452.9725490196174, 20.0), (1458.8509803921668, 20.0), (1464.7294117647157, 20.0), (1470.6078431372648, 20.0), (1476.4862745098137, 20.0), (1482.3647058823628, 20.0), (1488.2431372549117, 20.0), (1494.121568627461, 20.0), (1500.00000000001, 20.0)]  , 
        }
    
    
        self.dimensions = {
        	'': {
                'labels': [  ],
                'variables': [  ],
            },
        }
                
        self.dimensions_order = {}     
    
        self.stocks = ['deathsD',   'infectiousPopulationI',   'recoveredPopulationR',   'susceptiblePopulationS'  ]
        self.flows = ['deathRateDr',   'infectionRateIr',   'recoveryRateRr'  ]
        self.converters = ['averageDurationD',   'contactNumber',   'contactRateC',   'infectivityI',   'intensiveCareRate',   'intensiveCareUnitsAvailable',   'intensiveCareUnitsNeeded',   'lethalityL',   'netPopulationN',   'reproductionRate',   'totalPopulationTp'  ]
        self.gf = ['variableContactRate'  ]
        self.constants= []
        self.events = [
            ]
    
        self.memo = {}
        for key in list(self.equations.keys()):
          self.memo[key] = {}  # DICT OF DICTS!
          
    
    """
    Builtin helpers
    """
    def ramp(self,slope,start,t):
        if not start:
            start = self.starttime
        if t <= start: return 0
        return (t-start)*slope
        
    def rootn(self,expression,order):
        order = round(order,0)
        if expression < 0 and order % 2 == 0: # Stella does not allow even roots for negative numbers as no complex numbers are supported
            return np.nan
        return -abs(expression)**(1/round(order,0)) if expression < 0 else abs(expression)**(1/round(order,0)) # Stella Logic! No Complex numbers for negative numbers. Hence take the nth root of the absolute value and then add the negativity (if any)
    
    """
    Statistical builtins with Seed
    """
    def pareto_with_seed(self, shape, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.pareto(shape) * scale  
    
    def weibull_with_seed(self, shape, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.weibull(shape) * scale      
    
    def poisson_with_seed(self, mu, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.poisson(mu)   
    
    def negbinomial_with_seed(self, successes, p, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.negative_binomial(successes, p)  
    
    def lognormal_with_seed(self, mean, stdev, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.lognormal(mean, stdev)   
    
    def logistic_with_seed(self, mean, scale, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.logistic(mean, scale)
    
    def random_with_seed(self, seed, t ):
        if t == self.starttime:
            random.seed(int(seed))
        return random.random()

    def beta_with_seed(self, a,b,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.beta(a,b)
        
    def binomial_with_seed(self, n,p,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.binomial(n,p)
        
    def gamma_with_seed(self, shape,scale,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.gamma(shape,scale)
        
    def exprnd_with_seed(self, plambda,seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.exponential(plambda)
        
    def geometric_with_seed(self, p, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.geometric(p)
    
    def triangular_with_seed(self, left, mode, right, seed, t):
        if t == self.starttime:
            np.random.seed(int(seed))
        return np.random.triangular(left, mode, right)
    
    def rank(self, lis, rank):
        rank = int(rank)
        sorted_list = sorted(lis)
        try:
            rankth_elem = sorted_list[rank-1]
        except IndexError as e:
            logging.error("RANK: Rank {} too high for array of size {}".format(rank,len(lis)))
        return lis.index(rankth_elem)+1
        

    def interpolate(self, variable, t, *args):
        """
        Helper for builtin "interpolate". Uses the arrayed variable and args to compute the interpolation
        :param variable:
        :param t:
        :param args: Interpolation weight for each dimension, between one or zero
        :return:
        """
        def compute_x(values): #
            """
            Compute x values for interpolation. Always from 0 to 1. E.g. values = [1,2,3], then x = [0, 0.5, 1.0]
            :param values:
            :return:
            """
            #
            x = [0]
            for i in range(1, len(values)): x += [x[i - 1] + 1 / (len(values) - 1)]
            return x

        def interpolate_values(index, y_val):  # Internal interpolate of a dimension's results
            x_val = compute_x(y_val)
            points = [(x_val[i], y_val[i]) for i in range(0, len(x_val))]
            return LERP(index, points)

        # Fix each weight to a value between 0 and 1
        args = [max(0,min(x,1)) for x in args]

        # Get dimensions of variable (2,3,4 ...)
        dimensions = self.dimensions_order[variable]

        # Get Labels
        labels = {key: dim["labels"] for key, dim in
                  dict(filter(lambda elem: elem[0] in dimensions, self.dimensions.items())).items()}

        # Compute
        results = {}
        if len(labels.keys()) == 1:
            return interpolate_values(args[0], self.equation(variable + "[*]", t))
        for index, dimension in enumerate(dimensions):
            results[dimension] = []
            for label in labels[dimension]:
                indices = ["*" if i != index else label for i in
                           range(0, len(dimensions))]  # Build indices, such as "*,element1" or "1,*"

                results[dimension] += [
                    interpolate_values(args[index], self.equation(variable + "[{}]".format(",".join(indices)), t))]

        return [interpolate_values(args[i], v) for i, v in enumerate(results.values())][0]

    def lookupinv(self,gf, value):
        """
        Helper for lookupinv builtin. Looks for the corresponding x of a given y
        :param gf: Name of graphical function
        :param value: Value we are looking for (y)
        :return:
        """
        def lerpfun(x, points):  # Special lerp function for the reversed points
            from scipy.interpolate import interp1d
            x_vals = np.array([x[0] for x in points])
            y_vals = np.array([x[1] for x in points])
            f = interp1d(x_vals, y_vals)
            return f(x)

        results = []
        for t in np.arange(self.starttime, self.stoptime + self.dt,
                           self.dt):  # Compute all y values for graphical functions using standard interpolate (LERP)
            results += [(LERP(t, self.points[gf]), t)] # y,x

        return np.round(lerpfun(value, results),
                     3)  # Use LERP function for the reversed set of points (y,x) and find the correct value. Cannot use standard LERP here because that would require continuous X (1,2,3..)

    def delay(self, tdelayed, offset, initial, t):
        '''
        Delay builtin
        :param tdelayed: Delayed T
        :param offset: Offset
        :param initial: Initial value
        :param t:
        :return:
        '''
        if (t - self.starttime) < offset: return initial
        else: return tdelayed

    def counter(self,start, interval, t):
        '''
        Counter bultin
        :param start:
        :param interval:
        :param t:
        :return:
        '''
        num_elems = (interval / start / self.dt)
        value = interval / num_elems
        t_copy = copy(t)

        while t >= interval: t = t - interval
        if (t_copy > interval): return (start + (t / self.dt) * value)

        return (t / self.dt * value)

    def npv(self, initial, p, t):
        """
        NPV (Net Present Value) builtin
        :param initial:
        :param p:
        :param t:
        :return:
        """
        rate = 1.0 / (1.0 + p) ** (t - self.dt - self.starttime + self.dt)
        return initial if (t <= self.starttime) else ( self.npv(initial, p, t - self.dt) + (self.dt * rate * initial) )# Recurse

    def irr(self, stock_name, missing, t,myname):
        """
        Approximate IRR (Internal Rate of Return)
        :param stock_name: Identifier of Stock to approximate for
        :param missing: Replace missing values with this value
        :param t:
        :return:
        """

        def compute_npv(stock_name, t, i, missing):
            I = missing if missing else self.equation(stock_name, self.starttime)
            return I + sum( [self.memoize(stock_name, t) / (1 + i) ** t for t in np.arange(self.starttime+self.dt , t, self.dt)])

        i = 0
        try:
            i = 0 if t <= self.starttime + self.dt else self.memo[myname][t-self.dt]
        except:
            pass

        if t == self.starttime: return None

        best_kw = {i : compute_npv(stock_name, t, i, missing)}
        for _ in range(0, 300):
            # Here we approximate the IRR
            kw = compute_npv(stock_name, t, i, missing)

            change = 0.001

            best_kw[i] = kw

            if abs(kw) < self.memoize(stock_name, t)*0.1: change = 0.0001

            if abs(kw) < self.memoize(stock_name, t)*0.05: change = 0.00001

            if abs(kw) < self.memoize(stock_name, t)*0.02: change = 0.000001

            if kw < 0: i -= change
            elif kw > 0:  i += change

            if kw == 0: return i
        best_kw = {k: v for k, v in sorted(best_kw.items(), key=lambda item: item[1])}
        x = {v: k for k, v in sorted(best_kw.items(), key=lambda item: item[1])} # Sort by best npv
        return x[min(x.keys())]

    def normalcdf(self,left, right, mean, sigma):
        import scipy.stats
        right = scipy.stats.norm(float(mean), float(sigma)).cdf(float(right))
        left = scipy.stats.norm(float(mean), float(sigma)).cdf(float(left))
        return round(right - left, 3)

    def cgrowth(self, p):
        from sympy.core.numbers import Float
        import sympy as sy
        z = sy.symbols('z', real=True) # We want to find z
        dt = self.dt

        x = (1 + dt * (1 * z))

        for i in range(1, int(1 / dt)): x = (x + dt * (x * z))

        # Definition of the equation to be solved
        eq = sy.Eq(1 + p, x)

        # Solve the equation
        results = [x for x in (sy.solve(eq)) if type(x) is Float and x > 0] # Quadratic problem, hence usually a positive, negative and 2 complex solutions. We only require the positive one
        return float(results[0])

    def montecarlo(self,probability,seed, t):
        """
        Montecarlo builtin
        :param probability:
        :param seed:
        :param t:
        :return:
        """
        if seed and t==self.starttime:
            random.seed(seed)
        rndnumber = random.uniform(0,100)
        return 1 if rndnumber < (probability*self.dt) else 0


    def derivn(self, equation, order, t):
        """
        nth derivative of an equation
        :param equation: Name of the equation
        :param order: n
        :param t: current t
        :return:
        """
        memo = {}
        dt = 0.25

        def mem(eq, t):
            """
            Memo for internal equations
            :param eq:
            :param t:
            :return:
            """
            if not eq in memo.keys(): memo[eq] = {}
            mymemo = memo[eq]
            if t in mymemo.keys(): return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {}
        s[1] = lambda t: 0 if t <= self.starttime else (self.memoize(equation, t) - self.memoize(equation, t - dt)) / dt

        def addEquation(n):
            s[n] = lambda t: 0 if t <= self.starttime else (mem(n - 1, t) - mem(n - 1, t - dt)) / dt

        for n in list(range(2, order + 1)): addEquation(n)

        return s[order](t) if ( t >= self.starttime + (dt * order) ) else 0

    def smthn(self, inputstream, averaging_time, initial, n, t):
        """
        Pretty complex operator. Actually we are building a whole model here and have it run
        Find info in https://www.iseesystems.com/resources/help/v1-9/default.htm#08-Reference/07-Builtins/Delay_builtins.htm#kanchor364
        :param inputstream:
        :param averaging_time:
        :param initial:
        :param n:
        :param t:
        :return:
        """
        memo = {}
        dt = self.dt
        from copy import deepcopy

        def mem(eq, t):
            """
            Internal memo for equations
            :param eq:
            :param t:
            :return:
            """
            if not eq in memo.keys(): memo[eq] = {}
            mymemo = memo[eq]
            if t in mymemo.keys():return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {}

        def addEquation(n, upper):
            y = deepcopy(n)
            if y == 1:
                s["stock1"] = lambda t: (
                    (max([0, (self.memoize(inputstream, t) if (initial is None) else initial)])) if (
                                t <= self.starttime) else (
                                mem('stock1', t - dt) + dt * (mem('changeInStock1', t - dt))))
                s['changeInStock1'] = lambda t: (self.memoize(inputstream, t) - mem('stock1', t)) / (
                            averaging_time / upper)
            if y > 1:
                s["stock{}".format(y)] = lambda t: (
                    (max([0, (self.memoize(inputstream, t) if (initial is None) else initial)])) if (t <= self.starttime) else (
                                mem("stock{}".format(y), t - dt) + dt * (mem('changeInStock{}'.format(y), t - dt))))
                s['changeInStock{}'.format(y)] = lambda t: (mem("stock{}".format(y - 1), t) - mem("stock{}".format(y),
                                                                                                  t)) / (averaging_time / upper)
        n = int(n)

        for i in list(range(0, n + 1)): addEquation(i, n)

        return s['stock{}'.format(n)](t)

    def forcst(self,inputstream, averaging_time, horizon, initial, t):
        memo = {"change_in_input": {}, "average_input": {}, "trend_in_input": {}, "forecast_input": {}}

        def mem(eq, t):
            """
            Internal memo for equations
            :param eq:
            :param t:
            :return:
            """
            mymemo = memo[eq]
            if t in mymemo.keys(): return mymemo[t]
            else:
                mymemo[t] = s[eq](t)
                return mymemo[t]

        s = {
            "change_in_input": lambda t: max([0, (self.memoize(inputstream,t) - mem('average_input', t)) / averaging_time]),
            "average_input": lambda t: ((self.memoize(inputstream,t)) if (t <= self.starttime) else (
                        mem("average_input", t - self.dt) + self.dt * (mem("change_in_input", t - self.dt)))),
            "trend_in_input": lambda t: (((self.memoize(inputstream,t) - self.memoize('averageInput', t)) / (
                        self.memoize('averageInput', t) * self.memoize('averagingTime', t))) if (
                        self.memoize('averageInput', t) > 0.0) else (np.nan)),
            "forecast_input": lambda t: self.memoize(inputstream,t) * (1.0 + mem("trend_in_input", t) * horizon)
        }

        return s["forecast_input"](t)

    #Helpers for Dimensions (Arrays)

    def find_dimensions(self, stock):
        stockdimensions = {}
        for dimension, values in self.dimensions.items():
            if stock in values["variables"]:
                stockdimensions[dimension] = values["labels"]

        if len(stockdimensions.keys()) == 1:
            return [stock + "[{}]".format(x) for x in stockdimensions[list(stockdimensions.keys())[0]]]

    def get_dimensions(self, equation, t):
        re_find_indices = r'\[([^)]+)\]'
        group = re.search(re_find_indices, equation).group(0).replace("[", "").replace("]", "")
        equation_basic = equation.replace(group, "").replace("[]", "")
        labels = []
        for index, elem in enumerate(group.split(",")):
            if len(elem.split(":")) > 1: # List operator
                try:
                    bounds = [int(x) for x in elem.split(":")]
                except ValueError as e:
                    logging.error(e)
                    continue
                bounds = sorted(bounds)
                if len(bounds) > 2:
                    logging.error("Too many arguments for list operator. Expecting 2, got {}".format(len(bounds)))

                labels += [list(range(bounds[0], bounds[1]+1))]

            elif elem == "*": # Star operator
                dim = self.dimensions_order[equation_basic][index]
                labels += [self.dimensions[dim]["labels"]]
            else:
                if not type(elem) is list:
                    labels += [[elem]]
                else:
                    labels += [elem]

        products = cartesian_product(labels)

        return_list = []

        for product in products:
            prod = str(product).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
            return_list += [self.memoize(equation_basic + "[{}]".format(prod), t)]

        return return_list


    #Access equations API

    def equation(self, equation, arg):
        return self.memoize(equation,arg)


    #Memoizer for equations. Also does most of API work

    def memoize(self, equation, arg):
        if type(equation) is float or type(equation) is int: # Fallback for values
            return equation
        if "*" in equation or ":" in equation:
            return self.get_dimensions(equation,arg)
            
        if not equation in self.equations.keys():

            # match array pattern and find non-arrayed var
            import re
            match = re.findall("\[[a-zA-Z1-9,_]*\]", equation)

            if match:

                equation_replaced = equation.replace(match[0], "")

                if equation_replaced in self.equations:
                    return self.memoize(equation=equation_replaced,arg=arg)
            else:
                logging.error("Equation '{}' not found!".format(equation))

        mymemo = self.memo[equation]

        if arg in mymemo.keys():
            return mymemo[arg]
        else:
            result = self.equations[equation](arg)
            mymemo[arg] = result

        return result


    def setDT(self, v):
        self.dt = v

    def setStarttime(self, v):
        self.starttime = v

    def setStoptime(self, v):
        self.stoptime = v
    
    def specs(self):
        return self.starttime, self.stoptime, self.dt, 'Days', 'Euler'
    