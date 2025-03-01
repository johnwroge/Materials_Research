import os
import json
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymatgen.ext.matproj import MPRester
from pymatgen.core import Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
from tabulate import tabulate
from mp_api.client import MPRester


class MaterialsResearchAggregator:
    """
    A tool for chemists to aggregate and analyze materials research data
    from the Materials Project database.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Materials Research Aggregator.
        
        Args:
            api_key (str): Materials Project API key. If None, will try to use
                        the MATERIALS_PROJECT_API_KEY environment variable.
        """
        if api_key is None:
            # First try environment variable
            api_key = os.environ.get('MATERIALS_PROJECT_API_KEY')
            
            # If not found, try to read from .env file directly
            if api_key is None:
                try:
                    # Try current directory
                    env_path = os.path.join(os.getcwd(), '.env')
                    if os.path.exists(env_path):
                        with open(env_path, 'r') as f:
                            for line in f:
                                if line.startswith('MATERIALS_PROJECT_API_KEY='):
                                    api_key = line.strip().split('=', 1)[1]
                                    # Remove quotes if present
                                    api_key = api_key.strip("'").strip('"')
                                    break
                except Exception as e:
                    print(f"Error reading .env file: {e}")
                    
            if api_key is None:
                raise ValueError(
                    "No API key provided. Either pass an API key or set the "
                    "MATERIALS_PROJECT_API_KEY environment variable or create a .env file."
                )
        
        self.mpr = MPRester(api_key)


    def search_materials(self, elements, properties=None, num_results=10):
        """
        Search for materials containing specific elements using the MP API.
        
        Args:
            elements (list): List of element symbols to search for
            properties (list): List of properties to retrieve (default: None)
            num_results (int): Maximum number of results to return
            
        Returns:
            pandas.DataFrame: Materials data
        """
        # These are the fields that are actually available according to the error message
        if properties is None:
            properties = [
                "material_id",
                "formula_pretty",  # Instead of "formula"
                "formation_energy_per_atom",
                "energy_above_hull",
                "band_gap",
                "density",
                "bulk_modulus",    # Instead of "elasticity.k_vrh"
                "shear_modulus",   # Instead of "elasticity.g_vrh"
                "total_magnetization",
                "e_electronic",
                "ordering"         # Instead of "magnetic_ordering"
            ]
        
        # Create a chemsys string (e.g., "Li-Fe-O")
        chemsys = "-".join(elements)
        
        # Fetch data using the API with correct field names
        docs = self.mpr.materials.summary.search(
            chemsys=chemsys,
            fields=properties
        )
        
        # Convert documents to dictionaries and limit results
        results = [doc.dict() for doc in docs][:num_results]
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        return df

    def get_phase_diagram(self, elements):
        """
        Generate a phase diagram for a set of elements.
        
        Args:
            elements (list): List of element symbols
            
        Returns:
            tuple: (PhaseDiagram object, PDPlotter object)
        """
        entries = self.mpr.get_entries_in_chemsys(elements)
        pd_obj = PhaseDiagram(entries)
        plotter = PDPlotter(pd_obj, show_unstable=True)
        return pd_obj, plotter
    
    def analyze_property_trends(self, df, property_x, property_y):
        """
        Analyze trends between two properties.
        
        Args:
            df (pandas.DataFrame): Materials data
            property_x (str): Property for x-axis
            property_y (str): Property for y-axis
            
        Returns:
            matplotlib.figure.Figure: Plot of the property trends
        """
        # Create a new figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a scatter plot
        sns.scatterplot(data=df, x=property_x, y=property_y, ax=ax)
        
        # Calculate and display correlation
        correlation = df[property_x].corr(df[property_y])
        ax.set_title(f'Correlation: {correlation:.2f}')
        
        # Add labels and grid
        ax.set_xlabel(property_x.replace('_', ' ').title())
        ax.set_ylabel(property_y.replace('_', ' ').title())
        ax.grid(True, linestyle='--', alpha=0.7)
        
        return fig
    
    def compare_materials(self, material_ids, properties=None):
        """
        Compare properties of multiple materials side by side.
        
        Args:
            material_ids (list): List of material IDs
            properties (list): List of properties to compare (default: None)
            
        Returns:
            pandas.DataFrame: Comparison data
        """
        if properties is None:
            properties = [
                "material_id",
                "formula",
                "formation_energy_per_atom",
                "energy_above_hull",
                "band_gap",
                "density",
                "elasticity.K_VRH",
                "elasticity.G_VRH"
            ]
        
        # Get data for each material
        data = []
        for mid in material_ids:
            material_data = self.mpr.query({"material_id": mid}, properties)[0]
            
            # Handle nested properties
            for prop in properties:
                if "." in prop:
                    base, nested = prop.split(".", 1)
                    if base in material_data and isinstance(material_data[base], dict):
                        material_data[prop] = material_data[base].get(nested)
            
            data.append(material_data)
        
        return pd.DataFrame(data)
    
    def find_stable_materials(self, elements, energy_above_hull_max=0.05, band_gap_min=None):
        """
        Find thermodynamically stable materials containing specific elements.
        
        Args:
            elements (list): List of element symbols
            energy_above_hull_max (float): Maximum energy above hull (eV/atom)
            band_gap_min (float): Minimum band gap (eV), or None to ignore
            
        Returns:
            pandas.DataFrame: Stable materials data
        """
        # Create base criteria
        criteria = {
            "elements": {"$all": elements},
            "energy_above_hull": {"$lte": energy_above_hull_max}
        }
        
        if band_gap_min is not None:
            criteria["band_gap"] = {"$gte": band_gap_min}
        
        properties = [
            "material_id",
            "formula",
            "formation_energy_per_atom",
            "energy_above_hull",
            "band_gap",
            "density",
            "elasticity.K_VRH",
            "spacegroup.symbol"
        ]
        
        results = self.mpr.query(criteria, properties)
        df = pd.DataFrame(results)
        
        # Handle nested properties
        if "spacegroup.symbol" in df.columns:
            df["spacegroup"] = df["spacegroup"].apply(lambda x: x.get("symbol") if x else None)
        
        for col in df.columns:
            if "." in col:
                base, nested = col.split(".", 1)
                if base in df.columns and isinstance(df[base].iloc[0], dict):
                    df[col] = df[base].apply(lambda x: x.get(nested) if x else None)
        
        return df
    
    def export_to_csv(self, df, filename):
        """
        Export dataframe to CSV file.
        
        Args:
            df (pandas.DataFrame): Data to export
            filename (str): Output filename
        """
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
    
    def display_material_summary(self, material_id):
        """
        Display a detailed summary of a specific material.
        
        Args:
            material_id (str): Material Project ID
            
        Returns:
            dict: Material data
        """
        # Get comprehensive data for the material using the new API
        try:
            # Fetch the material using the new API
            material_doc = self.mpr.materials.summary.get_data_by_id(material_id)
            material_data = material_doc.dict()
            
            # Print basic information
            print("\n" + "="*50)
            print(f"Material ID: {material_id}")
            print(f"Formula: {material_data.get('formula_pretty', 'N/A')}")
            if 'symmetry' in material_data and material_data['symmetry']:
                print(f"Spacegroup: {material_data['symmetry'].get('symbol', 'N/A')}")
                print(f"Crystal System: {material_data['symmetry'].get('crystal_system', 'N/A')}")
            print("-"*50)
            
            # Print thermodynamic properties
            print("Thermodynamic Properties:")
            print(f"  Formation Energy per Atom: {material_data.get('formation_energy_per_atom', 'N/A')} eV/atom")
            print(f"  Energy Above Hull: {material_data.get('energy_above_hull', 'N/A')} eV/atom")
            print(f"  Density: {material_data.get('density', 'N/A')} g/cm³")
            print("-"*50)
            
            # Print electronic properties
            print("Electronic Properties:")
            print(f"  Band Gap: {material_data.get('band_gap', 'N/A')} eV")
            print(f"  Is Metal: {'Yes' if material_data.get('is_metal', False) else 'No'}")
            print("-"*50)
            
            # Print mechanical properties if available
            if 'bulk_modulus' in material_data and material_data['bulk_modulus']:
                print("Mechanical Properties:")
                print(f"  Bulk Modulus: {material_data.get('bulk_modulus', 'N/A')} GPa")
                print(f"  Shear Modulus: {material_data.get('shear_modulus', 'N/A')} GPa")
            print("="*50)
            
            return material_data
            
        except Exception as e:
            print(f"Error retrieving material data: {e}")
            print("Try using the Materials Project website to view details: https://materialsproject.org/materials/{material_id}")
            return None


def main():
    
    parser = argparse.ArgumentParser(description='Materials Research Aggregator')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for materials')
    search_parser.add_argument('elements', type=str, help='Comma-separated list of elements')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum number of results')
    search_parser.add_argument('--output', type=str, help='Output CSV filename')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare materials')
    compare_parser.add_argument('material_ids', type=str, help='Comma-separated list of material IDs')
    compare_parser.add_argument('--output', type=str, help='Output CSV filename')
    
    # Stable command
    stable_parser = subparsers.add_parser('stable', help='Find stable materials')
    stable_parser.add_argument('elements', type=str, help='Comma-separated list of elements')
    stable_parser.add_argument('--hull', type=float, default=0.05, help='Maximum energy above hull')
    stable_parser.add_argument('--band-gap', type=float, help='Minimum band gap')
    stable_parser.add_argument('--output', type=str, help='Output CSV filename')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show material summary')
    summary_parser.add_argument('material_id', type=str, help='Material ID')
    
    args = parser.parse_args()
    
    # Initialize the aggregator
    try:
        aggregator = MaterialsResearchAggregator()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your Materials Project API key using the environment variable:")
        print("export MATERIALS_PROJECT_API_KEY='your_api_key'")
        return
    
    if args.command == 'search':
        elements = [e.strip() for e in args.elements.split(',')]
        df = aggregator.search_materials(elements, num_results=args.limit)
        
        print(f"\nFound {len(df)} materials containing {', '.join(elements)}:")
        # Use formula_pretty instead of formula
        print(tabulate(df[['material_id', 'formula_pretty', 'formation_energy_per_atom', 
                         'energy_above_hull', 'band_gap']], 
                       headers='keys', tablefmt='psql'))
        
        if args.output:
            aggregator.export_to_csv(df, args.output)
    
    elif args.command == 'compare':
        material_ids = [mid.strip() for mid in args.material_ids.split(',')]
        df = aggregator.compare_materials(material_ids)
        
        print("\nMaterial Comparison:")
        print(tabulate(df, headers='keys', tablefmt='psql'))
        
        if args.output:
            aggregator.export_to_csv(df, args.output)
    
    elif args.command == 'stable':
        elements = [e.strip() for e in args.elements.split(',')]
        df = aggregator.find_stable_materials(
            elements, 
            energy_above_hull_max=args.hull,
            band_gap_min=args.band_gap
        )
        
        print(f"\nFound {len(df)} stable materials containing {', '.join(elements)}:")
        # Use formula_pretty instead of formula
        print(tabulate(df[['material_id', 'formula_pretty', 'formation_energy_per_atom', 
                         'energy_above_hull', 'band_gap']], 
                       headers='keys', tablefmt='psql'))
        
        if args.output:
            aggregator.export_to_csv(df, args.output)
    
    elif args.command == 'summary':
        aggregator.display_material_summary(args.material_id)


if __name__ == "__main__":
    main()