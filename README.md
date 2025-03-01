# Materials Research Aggregator

A Python tool designed for chemists to easily search, retrieve, and analyze materials research data from the Materials Project database.

## Features

- **Search Materials**: Find materials containing specific elements with customizable property output
- **Phase Diagram Generation**: Create phase diagrams for multi-element systems
- **Stable Materials Identification**: Discover thermodynamically stable materials with specific properties
- **Property Correlation Analysis**: Explore correlations between different material properties
- **Material Comparison**: Compare properties of multiple materials side-by-side
- **Detailed Material Summaries**: Generate comprehensive reports for specific materials
- **Data Export**: Save results to CSV files for further analysis

## Quick Installation

We've provided simple installation scripts for both Unix/Mac and Windows systems:

### Unix/Mac
```bash
# Clone the repository
git clone https://github.com/your-username/materials-research-aggregator.git
cd materials-research-aggregator

# Run the quickstart script
chmod +x quickstart.sh
./quickstart.sh
```

### Windows
```cmd
# Clone the repository
git clone https://github.com/your-username/materials-research-aggregator.git
cd materials-research-aggregator

# Run the quickstart script
quickstart.bat
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/your-username/materials-research-aggregator.git
cd materials-research-aggregator

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package and dependencies
pip install -e .
```

## Dependencies

The quickstart script will automatically install all required dependencies:

- **pymatgen** - Core Materials Project API access and analysis
- **pandas** - Data manipulation and analysis
- **matplotlib & seaborn** - Visualization capabilities
- **plotly** - Interactive visualizations
- **tabulate** - Formatted table output
- **numpy & scipy** - Scientific computing

## API Key Setup

The Materials Project API key can be set up in several ways:

### Option 1: Using a .env file (Recommended)
Create a `.env` file in your project directory:

```
# .env file
MATERIALS_PROJECT_API_KEY=your_api_key_here
```

A `.env.example` file is provided as a template. Just copy it and add your key:

```bash
cp .env.example .env
# Then edit .env with your API key
```

The `.env` file is included in `.gitignore` to prevent accidentally sharing your API key.

### Option 2: Environment variable
```bash
# On Linux/Mac
export MATERIALS_PROJECT_API_KEY='your_api_key'

# On Windows (Command Prompt)
set MATERIALS_PROJECT_API_KEY=your_api_key

# On Windows (PowerShell)
$env:MATERIALS_PROJECT_API_KEY='your_api_key'
```

### Getting an API Key
1. Register at [Materials Project](https://materialsproject.org/)
2. Go to your dashboard and get your API key

### Basic Usage

Search for materials containing specific elements:

```bash
python materials_aggregator.py search Li,Fe,O --limit 20 --output li_fe_o_materials.csv
```

Find thermodynamically stable materials:

```bash
python materials_aggregator.py stable Si,O --hull 0.05 --band-gap 1.0
```

Get detailed information about a specific material:

```bash
python materials_aggregator.py summary mp-149
```

Compare multiple materials:

```bash
python materials_aggregator.py compare mp-149,mp-1143,mp-554
```

## Example Use Cases

### Battery Materials Screening

Researchers looking for new battery cathode materials can quickly:
1. Search for materials containing Li, Mn, O with `search Li,Mn,O`
2. Filter for stable candidates using `stable Li,Mn,O --hull 0.02`
3. Compare the most promising materials to existing ones like LiCoO₂ (mp-22526)

### Photovoltaic Materials Discovery

For solar cell applications:
1. Find stable semiconductors with appropriate band gaps: `stable Si,Ge --band-gap 1.0`
2. Generate detailed reports on promising candidates
3. Export data for further processing in other tools

### Structural Materials Analysis

For mechanical applications:
1. Search for materials with high elastic moduli
2. Compare mechanical properties between different structural materials
3. Analyze correlations between density and mechanical properties

## Advanced Usage

### Programmatic API

The tool can also be used as a Python library:

```python
from materials_aggregator import MaterialsResearchAggregator

# Initialize with your API key
aggregator = MaterialsResearchAggregator(api_key='your_api_key')

# Search for materials
df = aggregator.search_materials(['Li', 'Fe', 'O'], num_results=20)

# Analyze property trends
fig = aggregator.analyze_property_trends(df, 'formation_energy_per_atom', 'band_gap')
fig.savefig('energy_vs_bandgap.png')

# Find stable materials
stable_df = aggregator.find_stable_materials(['Si', 'O'], energy_above_hull_max=0.05)
```

### Customizing Properties

You can specify which properties to retrieve:

```python
properties = [
    "material_id", 
    "formula", 
    "formation_energy_per_atom", 
    "energy_above_hull", 
    "band_gap", 
    "elasticity.K_VRH", 
    "elasticity.G_VRH"
]

df = aggregator.search_materials(['Ti', 'O'], properties=properties)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The [Materials Project](https://materialsproject.org/) for providing the API and database
- [Pymatgen](https://pymatgen.org/) for materials analysis capabilities