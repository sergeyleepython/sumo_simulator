1. Install SUMO

http://sumo.dlr.de/wiki/Installing

2. Get road data

```
netconvert --osm-files map.osm -o map.net.xml
polyconvert --net-file map.net.xml --osm-files map.osm --type-file typemap.xml -o map.poly.xml
sumo-gui map.sumo.cfg
```

