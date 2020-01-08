# adafruit-fingerprint
> This library enables you communicate and with the r305 Fingerprint Identification Module via serial connection with upper computer.

The library enables you to  to communicate with the r305 fingerprint module from upper computer (your laptop, a raspberry pi etc), rather than the arduino which it was built for by default. The module communicates via TTL, therefore, to communicate you need a _USB - TTL converter_ connected to the module.

It provides a class that exposes methods you can call to perform serial read/write actions with the module, these methods are implemented according to the datasheet specification, which you can download from the repo [here].


## Installation

```sh
pip install adafruit-fingerprint
```

## Usage example

There is a section on the [docs - hardware section] with pictures and explanations on how to setup the hardware needed for these examples to work.

Visit the [Examples Codes] section on the [docs] to view all examples.


## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
pip install
python -m unittest discover tests
```

## Release History

* 1.0.0
  * 

## Meta

This package is heavily inspired by the [finger_sphinx] project, found during our search for a way to get the fingerprint template to upper computer, rather than have it stored in flash library.

> Faith Odonghanro – [@toritsejuFO](https://twitter.com/toritsejuFO) (twitter), [toritsejuFO](https://github.com/toritsejuFO/) (github)

> Nwanozie Promise – [@PNwanozie](https://twitter.com/PNwanozie) (twitter), [iotstudent](https://github.com/iotstudent/) (github)

> Adegoke Joshua – [@iAmCodedebugger](https://twitter.com/iAmCodedebugger) (twitter), [Ade-Joshe](https://github.com/Ade-Joshe/) (github)

Distributed under the XYZ license. See ``LICENSE`` for more information.

## Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[finger_sphinx]: https://fingerprint-module-r305-python-and-mysql.readthedocs.io/en/latest/
[docs - hardware section]: harwawresetuplink
[Examples Codes]: examplelink
[docs]: docslinks
[here]: https://github.com/cerebrohivetech/adafruit-fingerprint/raw/master/finger-print-module.pdf
