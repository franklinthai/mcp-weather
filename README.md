# MCP Weather

A weather information service built with the Model Control Protocol (MCP) framework that provides access to National Weather Service (NWS) data.

## Overview

MCP Weather is a Python application that serves as an MCP tool, allowing AI assistants to access real-time weather information from the National Weather Service API. The service provides two main functionalities:

1. **Weather Alerts**: Get active weather alerts for any US state
2. **Weather Forecasts**: Get detailed weather forecasts for any location in the US by latitude and longitude

## Features

- Retrieve active weather alerts by US state code
- Get detailed weather forecasts for specific locations
- Clean, formatted output for easy reading
- Built as an MCP tool for seamless integration with AI assistants

## Requirements

- Python 3.13 or higher
- Dependencies:
  - httpx
  - mcp[cli]

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jpan8866/mcp-weather.git
   cd mcp-weather
   ```
2. You will need the python package manager `uv` to run the server
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Usage

### Running as an MCP Service

To test the server, run 
```
uv run weather.py
```

If the server runs successfully without errors, you can make the tool available with the following command:
```
PATH/uv --directory ABSOLUTE_PATH/mcp-weather run weather.py
```

### Available Tools

#### Get Weather Alerts

Retrieves active weather alerts for a specified US state.

Parameters:
- `state`: Two-letter US state code (e.g., CA, NY)

#### Get Weather Forecast

Retrieves a detailed weather forecast for a specific location.

Parameters:
- `latitude`: Latitude of the location
- `longitude`: Longitude of the location

## API Reference

The application uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) to fetch weather data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- National Weather Service for providing the weather data API
- MCP framework for enabling AI tool integration
- Documentation on Model context protocol: https://modelcontextprotocol.io/quickstart/server#test-with-commands
