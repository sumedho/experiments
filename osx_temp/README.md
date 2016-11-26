# OSX Temperatures

Outputs temperature readings for OSX.

## Usage 

### Compiling

```bash
make
```

### Running

```bash
./osx-temp
```

or

```bash
sudo make install # installs to /usr/local/bin
osx-temp
```

### Using clib

```bash
clib install osx-temp
```

### Output example

```
61.8°C
```

### Options

 * `-C` Output temperature in Celsius (default).
 * `-F` Output temperature in Fahrenheit.

## Maintainer 



### Source 

osx-cpu-temp Sébastien Lavoie <sebastien@lavoie.sl>
Apple System Management Control (SMC) Tool 
Copyright (C) 2006

### Inspiration 

 * https://github.com/lavoiesl/osx-cpu-temp
 * https://github.com/beltex/SMCKit
 * http://www.eidac.de/smcfancontrol/
 * https://github.com/hholtmann/smcFanControl/tree/master/smc-command
