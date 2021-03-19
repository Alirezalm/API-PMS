## Seazone Code Challenge - API integration


The challenge consists in creating a Python script which gets a calendar structure
for all listings available at Seazone using the Stays API and store this information in the form of CSV files.

**Tasks:**


- Acquire the Price Regions we have in the system
- For each region acquire all the Sell Price Rules
- Acquire all Seazone’s listings (there are more than 100)
- For each listing in each region retrieve all the Listings Sell Prices
- Organize a dataframe that contains the price for each listing for each day from
June/2021 to September/2021 (included)

For each item generate a csv with the results. Each different item must be organized in
separated functions in a way that each function can be used alone. If any data is needed
from another function it is imperative that you treat the exceptions

#### Installing and running the application

**Linux Users**

- Give the file `install.sh` execution permission 

    `chmod +x install.sh`
  
- Run the script
  
    `./install.sh`

**Notes**

- Make sure python 3 is installed.
- To run the script an authorization toke is needed.

