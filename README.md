# mediarr-seerr-sync
Automatically sync media from *arr with seerr when deleted.

## Installation
### Pre-requisites
- python 3.x
- pip

#### Native
1. Install the requirements
```
pip install -r requirements.txt
```
2. Configure the `config.py` file to your needs
3. Edit the `forwarder.sh`, replace ip with the ip of the machine running the `main.py`
4. Add the `forwarder.sh` script script with On Movie/Series delete trigger of *arr
5. Run with `python main.py` or `nohup python main.py &`(detached)

#### Docker
1. Copy the `config.py` to where you would like and edit the file to your needs
2. Run the docker container with the `config.py` file passed in (add `-d` to run detached)
```
docker run --name arr_sync -v /Path/to/config.py:/app/config.py -p 5000:5000 fallenbagel/arr_sync
```
3. Edit the `forwarder.sh`, replace ip with the ip of the docker container (hostname would work too if in the same docker network)
4. Add the `forwarder.sh` script script with On Movie/Series delete trigger of *arr

## Special thanks to:
- [arr_syncseerr](https://github.com/GHYAKIMA/arr_syncseerr)