# SPADE
[MED] SPADE implementation based on Zaki, 2001

## Directory /spade

Contains our implementation of the SPADE agorithm. Code is split in two files:

 - utils.py - functions and classes
 - miner.py - main implementation

 Run ```python miner.py``` with arguments:

  - ```--dataset``` STR Path to dataset
  - ```--support``` INT Minimum support
  - ```--max-depth``` INT Maximum lenght

## Directory /datasets

Contains test datasets:

 - dataset_online_retail_II.csv - 'Online Retail Dataset II' - our test dataset in csv format 
 - retail_zaki_formatted.txt - 'Online Retail Dataset II' - in whitespace separated format supported by zaki C++ implementation
 - retail_zaki_formatted_small.txt - 'Online Retail Dataset II' - in whitespace separated format supported by zaki C++ implementation (first 3000 rows)

## Directory /original 

Contains code to test and compare performance between implemenatations and to convert dataset to other formats.