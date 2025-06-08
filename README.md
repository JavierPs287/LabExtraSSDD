# calculator repository template

Template for the extra SSDD laboratory 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Server

To run the server, in the root directory of this project we execute

```
ssdd-calculator --Ice.Config=config/calculator.config
```

## Comunicator

After the server is running, we should open another terminal and move to the directory

```
cd comunicador_kafka
```

First, we have to start the docker-compose

```
docker-compose up -d
```

If you have trouble starting the docker-compose, execute this

```
docker-compose down && docker-compose up -d
```

Before running the comunicator, we need to slice the file .ice

```
slice2py remotecalculator.ice
```

Once the docker-compose is running and the file .ice is sliced, we can start running the comunicator

```
python consumer_servidor.py
```

## Client

Once the server and the comunicator are running, you can try it with the client included in this repository. In another terminal, execute this

```
cd cliente_kafka
python producer_cliente.py
```

## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/calculator.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
calculator.Endpoints=tcp -p 10000
```

## Slice usage

The Slice file is provided inside the `calculator` directory. It is only loaded once when the `calculator`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.
