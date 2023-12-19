<p align="center">
  <img src=https://github.com/AeroMAPS/AeroSCOPE/assets/97613437/1824dcdd-1c25-489c-96e0-4897a0773b7c />
</p>


# Welcome 
AeroSCOPE is a project that aims to bring together various open data sources on air transport in order to better understand the geographical distribution of air transport.
More details on data collection and compilation can be found in the article accompanying this work: https://journals.open.tudelft.nl/joas/article/view/7201

AeroSCOPE is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.  
*Please contact us if your use case of the dataset it outside the academic framework: Although all sources used are open to everyone, the Eurocontrol database is only freely available to academic researchers. It is used in this dataset in a very aggregated way and under several levels of abstraction. As a result, it is not distributed in its original format as specified in the contract of use. As a general rule, we decline any responsibility for any use that is contrary to the terms and conditions of the various sources that are used. In case of commercial use of the database, please contact us in advance.*


## Setup

It is suggested to use a new [conda](https://docs.conda.io/en/latest/miniconda.html) virtual environment to install the required packages.
Python 3.10 is recommended, although older versions may work.

In the new virtual environment, navigate to the project folder. Most installations are done using poetry, except for poetry itself, which can be installed using pip or conda.



```bash
pip install poetry 
poetry install 
```

## Usage
AeroSCOPE can be used in two different ways.

* Simple usage: just to use the graphical interface or to download the final database, no external input is required.
* Advanced usage: to run all data collection and processing notebooks. External data inputs that are too large to be stored on git or whose distribution is restricted are required.

Please read the dedicated paper to understand the global data collection and aggregation process.  
The idea behind the project is to collect all open source air traffic data to build an extended air traffic route database for a given year, 2019.  
Due to the limited coverage of these sources, especially in Asia-Pacific, South America and Africa, a methodology has been developed to estimate the data in this case. 
Wikipedia airport pages are automatically parsed to find information on the route network from each airport. This newly created database is merged with the previously mentioned open source data and a regressor is trained.
Traffic (seats offered) is then estimated on the remaining routes before all sources are aggregated into a single file.
It is then analysed and can be explored using a simple user interface. 

### Simple usage

__Raw database csv file:__ 
_**The last version of the processed database is stored on zenodo under the following doi: [10.5281/zenodo.10143773](). Make sure to download v1.0.1.**_  
Be sure to replace default NaN (such as 'NA') when reading the csv, to avoid mistakingly considering North America and Namibia codes as NaN.

__AeroSCOPE app:__
To run the simple web app designed to explore the data, one can either visit www.aeromaps.eu/aeroscope (soon) or navigate to the 04_app folder using a terminal and run the app using voila.

```bash
cd (path to 04_app) 
voila AeroSCOPE.ipynb
```

### Adavanced usage

The process data collection is widely described in each notebook. Here, the articulation of the different notebooks and folders is described.  

The first folder ([01_wikipedia_parser](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/01_wikipedia_parser)) stores the data and the notebooks used to parse Wikipedia for airport information and flight routes. **In case the user wants to re-run the notebooks, please be aware that without precautions, the most recent version of wikipedia will be parsed, thus erasing the data collected for this work.**   
- [01-airport_parsing.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/01_wikipedia_parser/01-airport_parsing.ipynb) is used to retreive all airports pages urls and then to parse their wikipedia and wikidata informations.
- [02-routes_parsing.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/01_wikipedia_parser/02-routes_parsing.ipynb) is used to retreive all routes starting from each of the previously found airport. Note that this notebook would be particularly sensitive to a new run, as routes are constantly updated by the community.
- [03-routes_processing.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/01_wikipedia_parser/03-routes_processing.ipynb) is essentially a processing notebook, building on the results from the two previous notebooks.

The second folder ([02_airport_features](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/02_airport_features)) is used to add external features to each airport such as population, economical or geographical data.
- [00_kontur_loading](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/02_airport_features/00_kontur_loading.ipynb) is a side-notebook, to load and process a very large, density base population dataset. Since the input dataset weighs 6 Gb (compressed in *.gpkg*), it isn not worth it to store an version it => download it at [Kontur 400m Data](https://geodata-eu-central-1-kontur-public.s3.amazonaws.com/kontur_datasets/kontur_population_20220630.gpkg.gz) and put it in the data folder. Similarly, the output *.csv* file weighs 916 Mo, so it is not stored either. **Therefore this notebook should be run before 01_airport_features_construction**.  
- [01_airport_features_construction.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/02_airport_features/01_airport_features_construction.ipynb) adds the informations described before to the wikipedia-parsed airport database.

The third folder ([03_routes_schedule](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule)) is used to store the notebooks compiling the various datasets, to perform the learning and estimation on routes where the traffic is unknown and finally also the notebooks to test the final dataset.
- [00_oag_preprocessing.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule/00_oag_preprocessing.ipynb) is a side-notebook used to load and preprocess OAG dataset, that is used in the test notebook as a comparison source. Unfortunately, this data being proprietary, it is impossible to disclose neither the source file nor the process oag file.
- [01_routes_preparation.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule/01_routes_preparation.ipynb) is used to merge the route database with the completed airport informations. Traffic information (number of seats availabe) is added to each route existing open source databases onto the route database. 
Most input files are included in the repository, excepted:
  - BTS/T_T100_SEGMENT_ALL_CARRIER_2019.csv -> dowloadable on [US BTS](https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FMG)
  - Eurocontrol -> four month of 2019 data, downloadable for the reasearch community [Eurocontrol](https://ext.eurocontrol.int/prisme_data_provision_hmi/) (requires account creation). The processed file (ectrl_to_prod_ipynb.csv) is also toot large for git storage so this notebook should be run before the following notebooks.
  - OpenSky -> 12 months of 2019 data, processed in [osky_data_extraction.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/Utilities/osky_data_extraction.ipynb) and downloadable at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7923702.svg)](https://doi.org/10.5281/zenodo.7923702). The notebbok gather the months together and filter the data to flight were the final data point is below 1000ft.
  - Planespotters -> [planespotters.net](https://planespotters.net) graciously gave a crowdsourced aircraft registry, including most of aircraft capacity. Data is available for research purposes upon request.
- [02_routes_estimation.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule/02_routes_estimation.ipynb) is used to test several estimation technique and finally estimates the traffic using XGBoost regressor.
- [03_routes_product.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule/03_routes_product.ipynb) is the 'production' dataset creation notebook. It is similar in many ways to the first notebook of the folder but follows a different aggregation logic (not built on wikipedia database anymore). Airport passenger traffic information is used to scale estimated routes to minimize airport-level error.
- [04_final_testing.ipynb](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/03_routes_schedule/04_final_testing.ipynb) is used to perform tests at different levels (airport, route, country, flows), using various comparison sources detailled in the notebook. **Do not run this notebook withouth having OAG data. The dataset evaluation is presented as the notebbok output. Running it would clear those outputs.**

The fourth folder ([04_app](https://github.com/AeroMAPS/AeroSCOPE/tree/main/aeroscope/04_app)) contains the app notebook, that **is designed to run with *voila*, not as a standard notebook**. Several .py files used for plots. The preprocess.py file should be run if the source file is modified to adequately modify the processd data storage file , used for a faster *voila* execution.
  
## Authors

Antoine Salgas, Junzi Sun <br>
Contact: [antoine.salgas@isae-supaero.fr]
