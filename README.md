<p align="center">
  <img src=https://github.com/AeroMAPS/AeroSCOPE/assets/97613437/1824dcdd-1c25-489c-96e0-4897a0773b7c />
</p>


# Welcome 
AeroSCOPE is a project that aims to bring together various open data sources on air transport in order to better understand the geographical distribution of air transport.
More details on data collection and compilation can be found in the article accompanying this work: https://journals.open.tudelft.nl/joas/article/view/7201

AeroSCOPE is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.  
*Please contact us if your use case of the dataset it outside the academic framework: Although all sources used are open to everyone, the Eurocontrol database is only freely available to academic researchers. It is used in this dataset in a very aggregated way and under several levels of abstraction. As a result, it is not distributed in its original format as specified in the contract of use. As a general rule, we decline any responsibility for any use that is contrary to the terms and conditions of the various sources that are used. In case of commercial use of the database, please contact us in advance.*


## Setup - app only  

It is suggested to use a new [conda](https://docs.conda.io/en/latest/miniconda.html) virtual environment to install the required packages.
Python 3.10 is recommended, although older versions may work.

In the new virtual environment, navigate to the project folder. Most installations are done using poetry, except for poetry itself, which can be installed using pip or conda.

```bash
pip install aeroscope (soon)
```

## Usage
AeroSCOPE can be used in two different ways.

* Simple usage: just using the graphical interface or downloading the final database, no external input is required. This use case is directly addressed to this repository. 
* Advanced usage: to run all data collection and processing notebooks and to perform more complex analysis on the file. The GUI is an input to this mode (soon). External data inputs that are too large to be stored on git or whose distribution is restricted are required.
  This mode is described in https://github.com/AeroMAPS/AeroSCOPE_dataset.

Please read the dedicated paper to understand the global data collection and aggregation process.  
The idea behind the project is to collect all open-source air traffic data to build an extended air traffic route database for a given year, 2019.  
Due to the limited coverage of these sources, especially in Asia-Pacific, South America and Africa, a methodology has been developed to estimate the data in this case. 
Wikipedia airport pages are automatically parsed to find information on the route network from each airport. This newly created database is merged with the previously mentioned open source data and a regressor is trained.
Traffic (seats offered) is then estimated on the remaining routes before all sources are aggregated into a single file.
It is then analysed and can be explored using a simple user interface. 

### Simple usage

__AeroSCOPE app:__
To run the simple web app designed to explore the data, one can either visit www.aeromaps.eu/aeroscope (soon) or navigate to the 04_app folder using a terminal and run the app using voila.

```bash
aeroscope run (soon)
```

### Advanced usage 
This mode is described in https://github.com/AeroMAPS/AeroSCOPE_dataset.

__Raw database csv file:__ 
_**If you simply want to access the compiled database; The last version of the processed database is stored on zenodo under the following doi: [10.5281/zenodo.10143773](). Make sure to download v1.0.1.**_  
Be sure to replace default NaN (such as 'NA') when reading the csv, to avoid mistakingly considering North America and Namibia codes as NaN.

## Authors

Antoine Salgas, Junzi Sun <br>
Contact: [antoine.salgas@isae-supaero.fr]
