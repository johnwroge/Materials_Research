# Search for materials containing Li and O
python materials_aggregator.py search Li,O --limit 15 --output li_o_materials.csv

# Find stable Li-Mn-O materials for battery applications
python materials_aggregator.py stable Li,Mn,O --hull 0.02 --output li_mn_o_stable.csv

# Compare specific materials of interest
python materials_aggregator.py compare mp-1143,mp-554,mp-540772

# Get detailed summary of a specific material
python materials_aggregator.py summary mp-1143