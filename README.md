# OpenFLDashboard

OpenFLDashboard is an open-source, non-biased, dashboard for monitoring COVID-19 in Florida.  

  - Covers resident and non-resident information for all possible fields
  - Includes vaccine information
  - Provides explanation for calculations

### Installation

AutoMagic requires Python 3.x.
A requirements.txt is provided generated from pip freeze

```sh
$ pip install -r requirements.txt
```

A copy of a matching database is also required. This can be done by running createDB.py, followed by dailyUpdate.py
dailyUpdate.py can be run at anytime to check for new information to be added to the DB
To run, execute server.py

```sh
$ python3 createDB.py
$ python3 dailyUpdate.py
```

Here is a list of the major libraries being used:

```
ChartJS - For the wonderful charts
Flask - For providing a web frontend
Requests - For loading URLs efficiently
Bootstrap - Works with Flask to display pages
```
Some other resources used:

```
Florida Department of Health Database: https://open-fdoh.hub.arcgis.com/search?q=covid19
```