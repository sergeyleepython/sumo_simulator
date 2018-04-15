## Installation
1. Install SUMO

http://sumo.dlr.de/wiki/Installing

2. Clone this repo

3. Install requirements.txt (`pip3 install -r requirements.txt`). Use Python3. Maybe use `virtualenv`.

2. Download this archive with road data and extract it into the project folder.
[the Link](https://drive.google.com/file/d/1JwASG37-3QIbCukNzEn9j3OrjiG_Hyuz/view?usp=sharing)

3. In `settings.py` change `TOOLS_DIR` path.

## Ignore this

```
netconvert --osm-files map.osm -o map.net.xml
polyconvert --net-file map.net.xml --osm-files map.osm --type-file typemap.xml -o map.poly.xml
sumo-gui map.sumo.cfg
```

