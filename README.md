# Grupal Practise 1 - Data Typology and Life Cycle
Subject: M2.851 / Semester: 2024-1 / Date: 11-02-2024

## Authors
1) Marina Fernández Delgado - mfernandezdelg@uoc.edu
2) César Alvarez Mendoza - 

## Chosen Website

https://www.tecnocasa.es/

## DOI Zenodo Link

The dataset has been published in Zenodo with DOI: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14028180.svg)](https://doi.org/10.5281/zenodo.14028180)

## Description
This project is based on a Web Scraping process to extract property data from specific cities or all cities available 
in Spain from the Tecnocasa website.

The project is divided into 6 parts:
1) Reading robots.txt file of Tecnocasa website.
2) Showing the User Agent used to scrap
3) Obtaining all available cities urls from Tecnocasa website 
4) Scrapping of one property url to demonstrate whether the process works
5) Scrapping of one single city url to demonstrate whether the process works and reads all posibilities of this city
6) Scrapping of entire Tecnocasa Website

## Project structure
The project files are organized as follows:

1) *source* folder: 
    - **main.py**. It is the main file where all the project functions are executed, which have been created in other files and are imported into this one.
    - **functions.py**. It is the functions file needed to run the project. 
    - **requirements.txt**. This is the file where the list of used packages is located (Python 3.12).


2) *dataset* folder:
    - **dataset/apartment_valladolid.csv** contains the data of one property of Valladolid
    - **dataset/properties_valladolid.csv** contains the data of all available properties of Valladolid
    - **dataset/properties_Spain.csv** contains the data of all available properties of Spain. This dataset is the one that has been published in Zenodo.

## Installation
To start this project, the following steps must be followed:
1) **Clone the repository**: Open a terminal and run the following command to clone the repository to your local machine
2) **Navigate to the project directory**: Change to the directory of the cloned project
3) **Install Dependencies**: Before running the code, make sure to install all the necessary dependencies. 
This can be easily done using the **requirements.txt** file included in the project. The command that should be used is:
``` pip install -r requirements.txt ```
This command will install all the specific libraries and versions necessary to run the project correctly.
4) **Configure environment variables** (optional): If your project requires environment variables, create a .env file 
in the root of the project and add the necessary variables. You can use the .env.example file as a reference.
5) **Run main.py**: Once the dependencies are installed, you can run the **main.py** file to start the analysis.
    - To run the script from the main folder (project), use ``python source/main.py ``. This will allow the script to run correctly and export the CSV file to the dataset folder.

## Uses

This project is designed to extract and compile data on properties available for sale or rent from the Tecnocasa sales web portal. By leveraging web scraping techniques, the objective is to create a comprehensive list of all properties that can be purchased or rented, ensuring that users can easily access all relevant information. The key uses are the following:

1) **Data Extraction**: The project systematically retrieves information from the Tecnocasa portal, including property details such as location, price, size, number of rooms, and other relevant characteristics.
2) **Comprehensive Listings**: By aggregating data from multiple pages of listings, the project provides a complete overview of the available properties, facilitating informed decision-making for potential buyers and renters.
3) **User-Friendly Output**: The extracted data is organized in a structured format, making it easy to analyze, share, or import into other applications.
4) **Automatic Updates**: The scraper can be scheduled to run at regular intervals, ensuring that the property listings remain up-to-date with the latest available information from Tecnocasa.
5) **Data Analysis**: In addition to extraction, the project can incorporate basic data analysis features, allowing users to filter properties by specific criteria such as price range, location, or number of bedrooms.



## License
This project is distributed under the MIT License. This means that you are free to use, copy, modify and distribute 
this software, as long as you include the original license text in any copy or version of the software.

For more details, see the **LICENSE** file included in this project.