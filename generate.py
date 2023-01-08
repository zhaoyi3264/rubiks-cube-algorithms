import json
import os

import cairosvg
import requests
import pandas as pd

url = 'http://cubiclealgdbimagegen.azurewebsites.net/generator'

with open('config.json', 'r') as f:
    puzzles = json.load(f)

def generate_png(row, generator_params, path):
    os.makedirs(path, exist_ok=True)
    generator_params['case'] = row['Algorithm']
    response = requests.get(url, params=generator_params, timeout=10)
    svg = bytes(response.text, 'utf-8')
    write_to = os.path.join(path, f'{row["Algorithm"]}.png')
    cairosvg.svg2png(svg, scale=100, dpi=800, write_to=write_to)

for puzzle in puzzles:
    sheets = pd.read_excel(f'https://docs.google.com/spreadsheets/d/e/2PACX-{puzzle["sheet_id"]}/pub?output=xlsx', sheet_name=None)
    for algo_set in puzzle['algorithm_sets']:
        sheet = sheets[algo_set['sheet_name']]
        sheet.apply(generate_png, axis='columns', generator_params={
            'puzzle': puzzle['puzzle'],
            'view': algo_set['view'],
            'stage': algo_set['stage'],
        }, path=os.path.join(puzzle['dir'], algo_set['sub_dir']))
