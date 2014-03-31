MTG Pricer
=========

Automatically prices your inventory based on the market.

## Usage

Mtgpricer is a console application which can be invoked from the command line. Mtgpricer reads an input file containing
stock entries (qty, set, cardname, condition) and uses a local price database to automatically price each. The result
is then saved in an output priced stock file.
The price database is initialized and updated from online sources periodically.


### Input stock files

#### Excel

Check template.xls.
The stock file consists of four columns, each must have the header name, so keep that row.
The headers:

 * qty: how many of the card you've got, a number, if omitted, the default value will be one
 * set: the edition of the card. See: Set abbreviations for further info
 * name: the name of the card
 * condition: the condition of the card See: Conditions for futher info.

NOTE: DO NOT MIX SETS AND CONDITIONS IN ONE LINE

#### Plain text

TBD


#### Set abbreviations

The res subfolder contains a file named sets. This is a plain text file which contains such lines as:

    Alliances#Alliances,al

The lookup mechanism tries to find the sets online based on the name before the hash (in this case, Alliances).
To make things more convenient it is possible to use abbreviations in the stock file.
By default, each entry contains the full name of the set and the common abbreviation of the set with two letters
and three letters. It is possible to add more, just make sure that the new entry doesn't contain comma (,) and the
separator between the abbreviations is comma (,).
You will be warned on the console and the log file (See: Logging) if an abbreviation belongs to more than one sets.


#### Conditions

Another file in the res subfolder is conds. This is a plain text file with the following entries:

    NM: 1
    EX: 0.9

Where the part before the colon is the condition name and the number after is the price modifier. Feel free to modify
and amend it to meet your needs if required.

### Running the program: the easy way (Win only for now)

The source is compiled into one executable. Either invoke it direclty with the appropriate parameters or write a batch
script as quick launcher. See: How to customize the example script

##### How to customize the example script

The launher mtgpricer.bat (or mtgpricer.sh for other platforms) is in the root folder of the installation. Open it with
your favorite text editor and replace c:\here\comes\your\file.xls with the real path to the stock file.

### Running the program: for pros

Check out the sources. The program will run as-is, if you invoke mtgpricer.py.
The code is written with python 2.7, so 2to3 if you insist.
The additional dependencies to resolve:

* xlrd
* xlwt
- sqlalchemy
- requests

Everything (i.e. arguments ) else applies normally.


## Command line arguments

Run mtgpricer -h or --help to get the full picture anytime.

###Positional arguments

* stock file: mandatory, and must be the full or relative path to the input file
* priced stock: optional, if given, it should be the full or relative path for the priced output if not set, the default
will be <input>_priced.<ext>


###Optional arguments

<dl>
<dt>
-m, --modes
</dt>
<dd>
    Sets the reader and writer modes defined by a two letter code e.g.: xx or xt.
    The reader mode is the first letter of the code and determines the type of the input file which can be an excel
    document or a plain text file(currently unsupported).
    The writer mode is the second letter of code determines the format of the output file.
    This also can be excel (.xls) or plain text.
    In both positions, writing 'x' sets excel and 't' sets plain text.
    The default value is xx, i.e. both the input and the aoutput format are excel.
</dd>
<dt>
    -r, --refreshdb
</dt>
    Forces the refresh of the card database. This might take a while and won't work offline (of course...)
    By default, the price db is refreshed every 7 days.
</dd>
</dl>

## Logging, testing

## Feedback, bugs, enhancements

You can reach me



