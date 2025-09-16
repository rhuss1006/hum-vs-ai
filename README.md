# Human vs. AI Dashboard Comparison

A project comparing human-generated and AI-generated data visualization dashboards using RWHAP (Ryan White HIV/AIDS Program) funding recipient data.

⚠️ WARNING ⚠️ This dataset predates the Trump administration's cuts to HIV/AIDS funding. The data shown in these dashboards reflects funding allocations from before these policy changes and may not represent current funding levels or recipient statuses. 

## Overview

This project demonstrates the differences between manually coded dashboards and AI-generated dashboards for analyzing healthcare funding data. Both dashboards visualize the same dataset but with different approaches to complexity and functionality.

## Files

- **`human.py`** - Human-generated dashboard with basic functionality
  - Simple state and year filtering
  - Provider type bar chart
  - Data table view
  
- **`ai.py`** - AI-generated dashboard with advanced features
  - Multi-select filtering (states, providers, regions)
  - Multiple visualization types (bar, pie, scatter, geographic map)
  - Services analysis
  - Funding pattern analysis
  - Summary statistics

- **`api.py`** - API utilities for data processing
  - Data loading and transformation functions
  - Geographic coordinate extraction
  - State and city-level aggregations

- **`subrecipient_data.csv`** - RWHAP funding recipient data
  - 2,200 records with 60 columns
  - Provider information, funding indicators, geographic data
  - Service types and congressional district information

## Requirements

```
panel
pandas
numpy
holoviews
plotly
```

## Usage

Run either dashboard:

```bash
# Human-generated dashboard
python human.py

# AI-generated dashboard
python ai.py
```

Both dashboards will launch in your default web browser.

## Key Differences

### Human Dashboard
- Minimalist approach
- Single-select filters
- One chart type
- Focus on essential functionality

### AI Dashboard
- Comprehensive filtering options
- Multiple visualization types
- Advanced analytics (services, funding patterns)
- Interactive geographic mapping
- Tabbed interface for different analyses

## Data Source

The dataset contains information about Ryan White HIV/AIDS Program funding recipients, including provider types, funding parts (A-D), geographic locations, and services provided.

## Author

Rayd Hussain - May 23, 2025
