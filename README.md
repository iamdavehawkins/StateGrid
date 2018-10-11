# StateGrid

For plotting data by state on a simple grid rather than a map. Especially useful when the geographic area of the state is not relevant to the data being presented. Hopefully, also a bit quicker and easier than a full blown choropleth.

#### Sample Use

```python
from stategrid.statedata import StateData

data_path = './your_data.csv'
sd = StateData(data_path)
sd.plot_grid('medianincome', cmap=cm.rainbow, fname='./plots/medianincome.png')
sd.plot_grid('elec2012', cmap=cm.bwr, fname='./plots/elec2012.png')
```

#### Sample Output
###### 2013 Median Income
![Median Income 2013](http://imgur.com/z9PzYrx.png)
###### 2012 Election Results
![2012 Election Results](http://imgur.com/yHTlW58.png)

#### Input Data Format (*.csv)
|State _(required)_ | medianincome  | elec2012 |
|----------------   |---------------|----------|
|Michigan		    | 50056         | 0 	   |
|Texas			    | 52169         | 1        |
|Indiana 		    | 47805         | 1        |
|Nebraska           | 54777         | 1        | 
|...|...|...|

State abbreviations may be used instead (MI, TX, IN, NE)



#### Requirements
- Pandas 0.15.2+
- Numpy 1.9.2+
- Matplotlib 1.4.2+

#### TODO:
- Support for factor data
- Invert text color of state label when the background is 'too dark'
- Better color bar formatting
	- Lose scientific notation
