import pydivide 


insitu = pydivide.read('2015-4-26', instruments=['lpw', 'mag'])
pydivide.altplot(insitu, parameter=['LPW.ELECTRON_TEMPERATURE'], title='ELECTRON TEMEPRATRUE')
pydivide.map2d(insitu, 'MAG.MSO_X', title='MSO_X')