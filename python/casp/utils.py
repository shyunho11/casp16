import re

def parse_stoichiometry(stoichiometry):
    matches = re.findall(r'([A-Z])(\d+)', stoichiometry)
    return [(ord(letter)-65, int(count)) for letter, count in matches]


if __name__ == "__main__":
    stoich = 'A1B1C1D1E1F1G2H1I1'
    print('  '+''.join(f"{c}  {'  ' * (i % 2)}" for i, c in enumerate(stoich)))
    print(parse_stoichiometry(stoich))