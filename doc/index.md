The input of the datagenerator are CSV files, that contain real world seed data. The data generator can be separated into two components. Its structure is described in Figure \ref{fig:Structure_data generator}. In the first component - the "Data Preparation and Processing", the data gets processed and extended. In the second component, the Outputfeature Generation", the output is calculated and added as an output feature to the other input features. It is determined by a function influenced by the input parameters. Similarly any other feature that depends on the input parameters, could be generated, like the roughness of the surface. The output of the datagenerator is a csv file of a timeseries with the transformed data and the new feature.

![Structure Datagenerator](images/Structure_Datagenerator.png)

Components:
seeddatareater
baseeditor
pattern generator

elevation profile generator
