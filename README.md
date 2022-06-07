# SPADE

[MED] SPADE implementation based on (Zaki, M. J. 2001):
Agorithm finds frequent sequences in transaction list.

## Algorithm structure

1. Identification of single frequent elements.
2. Identification of frequent two-element sequences.
3. Identification of frequent sequences containing three or more elements.

## Directory /spade

Contains our implementation of the SPADE agorithm. Code is split in two files:

- utils.py - functions and classes
- miner.py - main implementation

 Run ```python miner.py``` with arguments:

- ```--dataset``` STR Path to dataset
- ```--support``` INT Minimum support
- ```--max-depth``` INT Maximum lenght of candidate sequence
- ```--min-gap``` INT Minimum time difference between consecutive elements of a sequence
- ```--max-gap``` INT Maximum time difference between consecutive elements of a sequence

## Directory /datasets

Contains test datasets:

- dataset_online_retail_II.csv - 'Online Retail Dataset II' - our test dataset in csv format
- retail_zaki.txt - 'Online Retail Dataset II' - in whitespace separated format supported by zaki C++ implementation
- retail_zaki_small.txt - 'Online Retail Dataset II' - in whitespace separated format supported by zaki C++ implementation (first 50 rows)
- products_map.json - map Id's to product names

## Directory /original

Contains code to test and compare performance between implemenatations and to convert dataset to other formats.

## Results

To shorten computation time test were performed on first 50 rows.

### Original implementation

```pre
   Occurs     Accum   Support    Confid      Lift       Sequence
       10        28 0.5263158       N/A       N/A          (POSTAGE)
        6         6 0.3157895 0.6000000 1.1400000   (POSTAGE)->(POSTAGE)
        5         5 0.2631579       N/A       N/A          (SWEETHEART CERAMIC TRINKET BOX)
        6         6 0.3157895       N/A       N/A          (STRAWBERRY CERAMIC TRINKET BOX)
        6         6 0.3157895       N/A       N/A          (PINK HEART SHAPE EGG FRYING PAN)
        4         4 0.2105263       N/A       N/A          (BIG DOUGHNUT FRIDGE MAGNETS)
        4         4 0.2105263 1.0000000 1.9000000   (BIG DOUGHNUT FRIDGE MAGNETS)->(POSTAGE)
        4         4 0.2105263       N/A       N/A          (PLASTERS IN TIN VINTAGE PAISLEY )
        4         4 0.2105263 1.0000000 1.9000000   (PLASTERS IN TIN VINTAGE PAISLEY )->(POSTAGE)
        4         4 0.2105263       N/A       N/A          (ROUND SNACK BOXES SET OF4 WOODLAND )
        4         4 0.2105263       N/A       N/A          (CERAMIC STRAWBERRY CAKE MONEY BANK)
        4         4 0.2105263       N/A       N/A          (CERAMIC CAKE BOWL + HANGING CAKES)
        4         4 0.2105263       N/A       N/A          (CERAMIC CAKE STAND + HANGING CAKES)
        4         4 0.2105263       N/A       N/A          (SPACEBOY BIRTHDAY CARD)
        4         4 0.2105263 1.0000000 1.9000000   (SPACEBOY BIRTHDAY CARD)->(POSTAGE)
        4         4 0.2105263       N/A       N/A          (SPACEBOY LUNCH BOX )
        4         4 0.2105263       N/A       N/A           (SPACEBOY GIFT WRAP)
        4         4 0.2105263       N/A       N/A           (REGENCY CAKESTAND 3 TIER)
```

### Our Results


Frequent single sets:
<span style="color:red">(('SPACEBOY GIFT WRAP',),)</span>
<span style="color:red">(('REGENCY CAKESTAND 3 TIER',),)</span>
<span style="color:red">(('POSTAGE',),)</span>
<span style="color:red">(('SWEETHEART CERAMIC TRINKET BOX',),)</span>
<span style="color:red">(('STRAWBERRY CERAMIC TRINKET BOX',),)</span>
<span style="color:red">(('PINK HEART SHAPE EGG FRYING PAN',),)</span>
<span style="color:red">(('BIG DOUGHNUT FRIDGE MAGNETS',),)</span>
<span style="color:red">(('PLASTERS IN TIN VINTAGE PAISLEY ',),)</span>
<span style="color:red">(('ROUND SNACK BOXES SET OF4 WOODLAND ',),)</span>
<span style="color:red">(('CERAMIC STRAWBERRY CAKE MONEY BANK',),)</span>
<span style="color:red">(('CERAMIC CAKE BOWL + HANGING CAKES',),)</span>
<span style="color:red">(('CERAMIC CAKE STAND + HANGING CAKES',),)</span>
<span style="color:red">(('SPACEBOY BIRTHDAY CARD',),)</span>
<span style="color:red">(('SPACEBOY LUNCH BOX ',),)</span>
Frequent pairs:
(('STRAWBERRY CERAMIC TRINKET BOX',), ('PINK HEART SHAPE EGG FRYING PAN',))
(('PINK HEART SHAPE EGG FRYING PAN',), ('STRAWBERRY CERAMIC TRINKET BOX',))
(('SWEETHEART CERAMIC TRINKET BOX',), ('ROUND SNACK BOXES SET OF4 WOODLAND ',))
(('ROUND SNACK BOXES SET OF4 WOODLAND ',), ('SWEETHEART CERAMIC TRINKET BOX',))
(('POSTAGE',), ('ROUND SNACK BOXES SET OF4 WOODLAND ',))
(('ROUND SNACK BOXES SET OF4 WOODLAND ',), ('POSTAGE',))
(('PLASTERS IN TIN VINTAGE PAISLEY ',), ('ROUND SNACK BOXES SET OF4 WOODLAND ',))
(('STRAWBERRY CERAMIC TRINKET BOX',), ('CERAMIC STRAWBERRY CAKE MONEY BANK',))
(('CERAMIC STRAWBERRY CAKE MONEY BANK', 'STRAWBERRY CERAMIC TRINKET BOX'),)
(('STRAWBERRY CERAMIC TRINKET BOX',), ('ROUND SNACK BOXES SET OF4 WOODLAND ',))
(('ROUND SNACK BOXES SET OF4 WOODLAND ',), ('STRAWBERRY CERAMIC TRINKET BOX',))
(('REGENCY CAKESTAND 3 TIER',), ('REGENCY CAKESTAND 3 TIER',))
(('SPACEBOY LUNCH BOX ',), ('REGENCY CAKESTAND 3 TIER',))
(('POSTAGE',), ('SPACEBOY LUNCH BOX ',))
(('SPACEBOY LUNCH BOX ',), ('POSTAGE',))
(('POSTAGE',), ('SPACEBOY GIFT WRAP',))
(('SPACEBOY GIFT WRAP',), ('POSTAGE',))
(('PLASTERS IN TIN VINTAGE PAISLEY ',), ('SPACEBOY LUNCH BOX ',))
(('SWEETHEART CERAMIC TRINKET BOX',), ('POSTAGE',))
(('POSTAGE',), ('SWEETHEART CERAMIC TRINKET BOX',))
(('STRAWBERRY CERAMIC TRINKET BOX', 'SWEETHEART CERAMIC TRINKET BOX'),)
(('STRAWBERRY CERAMIC TRINKET BOX',), ('SWEETHEART CERAMIC TRINKET BOX',))
(('SWEETHEART CERAMIC TRINKET BOX',), ('STRAWBERRY CERAMIC TRINKET BOX',))
(('SPACEBOY BIRTHDAY CARD',), ('SPACEBOY LUNCH BOX ',))
(('SWEETHEART CERAMIC TRINKET BOX',), ('PLASTERS IN TIN VINTAGE PAISLEY ',))
(('PLASTERS IN TIN VINTAGE PAISLEY ',), ('SWEETHEART CERAMIC TRINKET BOX',))
(('POSTAGE',), ('SPACEBOY BIRTHDAY CARD',))
<span style="color:red">(('SPACEBOY BIRTHDAY CARD',), ('POSTAGE',))</span>
<span style="color:red">(('POSTAGE',), ('POSTAGE',))</span>
(('STRAWBERRY CERAMIC TRINKET BOX',), ('POSTAGE',))
(('POSTAGE',), ('STRAWBERRY CERAMIC TRINKET BOX',))
<span style="color:red">(('BIG DOUGHNUT FRIDGE MAGNETS',), ('POSTAGE',))</span>
(('POSTAGE',), ('BIG DOUGHNUT FRIDGE MAGNETS',))
<span style="color:red">(('PLASTERS IN TIN VINTAGE PAISLEY ',), ('POSTAGE',))</span>
(('POSTAGE',), ('PLASTERS IN TIN VINTAGE PAISLEY ',))

