TEDL package
=


Introduction
------------
The TEDL package is the comprehensive Python tool for accessing compound datasets on Tedesignlab.org.




Install
-------
For Python 2.7:
```
pip install -e git+https://github.com/kevgao/TEDL.git#egg=TEDL
```
For Python 3:
```
pip3 install -e git+https://github.com/kevgao/TEDL.git#egg=TEDL
```



How to Use
-----------
In python, you can import the package like this:

```
from TEDL.data import Sampling
```

If you want to retrive samples from TEDL, you can use the Sampling class like this:
```
samples = Sampling('structure-B', 'B', filter='Al S O', split = False, X_normalize = False, Y_normalize = False)
print(samples.X)
print(samples.y)
print(samples.formula)
print(samples.features)
print(samples.targets)
```



If you are using the dataset for train/test experiments, the Sampling class is right for you:
```
samples = Sampling('structure-B', 'B', filter='Al S O', split = True, X_normalize = False, Y_normalize = False)
```
You can easily use the data like:
```
print(samples.formula) # formulas of sample compounds
print(samples.features) 
print(samples.targets) 

print(samples.train_X)
print(samples.train_y)
print(samples.test_X)
print(samples.test_y)
```