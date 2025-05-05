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

## Execution

Before the server is running, you gotta start the docker-compose

```
cd calculator
docker-compose up -d
```

If you have trouble starting the docker-compose, execute this

```
docker-compose down && docker-compose up -d
```

Once the docker compose is running, run the server

```
ssdd-calculator --Ice.Config=config/calculator.config
```

## Client

Once the server is started, you can try it with the client included in this repository. In another terminal, execute this

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
