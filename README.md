# Pigeon
Pigeon brings your records to redcap. Pigeon will print its log to stdout by default and any errors it comes across to stderr.
It is able to take both json and csv flat records and upload them to redcap.

```
  _____ _____ _____ ______ ____  _   _
 |  __ \_   _/ ____|  ____/ __ \| \ | |
 | |__) || || |  __| |__ | |  | |  \| |
 |  ___/ | || | |_ |  __|| |  | | . ` |
 | |    _| || |__| | |___| |__| | |\  |
 |_|   |_____\_____|______\____/|_| \_|

```                                     

# Installation and first use
Pigeon is a python3 application so make sure that you are utilizing the correct
python and pip.

Note that you need a redcap project with an API token and data to import into.

Finally you 

1. `$ git clone https://github.com/ctsit/cappy.git`
2. `$ pip install ./cappy`
3. `$ git clone pigeon`
4. `$ pip install ./pigeon`
5. `$ cp pigeon/pigeon/pigeon.example.conf.yaml my_redcap_pigeon_conf.yaml`
6. `$ pigeon my_redcap_data.json my_redcap_pigeon_conf.yaml -o pigeon_output.json`

Alternatively 6 can be replaced with
`$ pigeon my_redcap_data.json REDCAPTOKEN REDCAPURL -o pigeon_output.json`

# Usage Examples
    Pigeon is used to load data into redcap. It is able to use various formats of data and 
    various upload strategies, batches of varying size, and also pigeon will always upload everything it can.
    Running pigeon after installation gives help text on how to use it.
    
    `$ pigeon my_redcap_data.json my_redcap_pigeon_conf.yaml -o pigeon_output.json`
    `$ pigeon my_redcap_data.json REDCAPTOKEN REDCAPURL -o pigeon_output.json`

# Development setup
    ## TODO: Write Here

# Release History
    ## TODO: Write Here

# License
    ## TODO: Write Here

# Author(s)
    ## TODO: Write Here

# Issues
    ## TODO: Write Here

# Wiki  
    ## TODO: Write Here
