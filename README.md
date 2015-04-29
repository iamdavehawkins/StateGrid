# StateGrid

For plotting data by state on a simple grid rather than a map. Especially useful when the geographic area of the state is not relevant to the data being presented. Hopefully, also a bit quicker and easier than a full blown chloropleth.

#### Sample Use

```python
from stategrid.statedata import StateData

data_path = './your_data.csv'
sd = StateData(data_path)
sd.plot_grid('medianincome', cmap=cm.rainbow, fname='./plots/medianincome.png')
sd.plot_grid('elec2012', cmap=cm.bwr, fname='./plots/elec2012.png')
```

#### Sample Output
######2013 Median Income
<img src="http://imgur.com/z9PzYrx.png" alt="Median Income 2013", width="420">
######2012 Election Results
<img src="http://imgur.com/yHTlW58.png" alt="2012 Election Results", width="420">

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
