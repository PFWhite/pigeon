# pigeon 1.0.0
Pigeon brings your records to redcap.

It is able to take both json and csv flat records and upload them to redcap.

# installation
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
