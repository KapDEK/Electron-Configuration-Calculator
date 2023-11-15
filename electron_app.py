from flask import Flask, request, render_template_string 
from flask import Flask, request, render_template

app = Flask(__name__)

atomic_symbols = {
'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Ni': 27, 'Co': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 
    # Add other elements as needed
    # ...
}


def calculate_electrons_in_sublevel(sublevel):
    """
    Calculates the maximum number of electrons that can be present in a given sublevel.
    """
    orbital_max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
    return orbital_max_electrons.get(sublevel[-1], 0)

def get_electron_configuration(atomic_number):
    orbitals = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p']
    orbital_max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}

    configuration = []
    remaining_electrons = atomic_number

    for orbital in orbitals:
        if remaining_electrons <= 0:
            break

        orbital_type = orbital[-1]
        max_electrons_in_orbital = orbital_max_electrons[orbital_type]
        electrons_in_orbital = min(remaining_electrons, max_electrons_in_orbital)
        configuration.append(f"{orbital}{electrons_in_orbital}")
        remaining_electrons -= electrons_in_orbital

    return ' '.join(configuration)


def get_valence_electrons(atomic_number):
    """
    Determines the number of valence electrons for an element based on its atomic number.
    """
    configuration = get_electron_configuration(atomic_number).split()
    valence_shell = max(int(orbital[0]) for orbital in configuration)
    valence_electrons = sum(int(orbital[2:]) for orbital in configuration if int(orbital[0]) == valence_shell)
    return valence_electrons

    

# Examples
sublevel_example = '2p'  # Calculate the number of electrons in the 2p sublevel
valence_electrons_example = get_valence_electrons(11)  # Sodium has an atomic number of 11

calculate_electrons_in_sublevel(sublevel_example), valence_electrons_example  # Returns max electrons in 2p and valence electrons of Sodium

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        atomic_input = request.form.get('atomic_input', '').strip()
        atomic_number = None

        if atomic_input.isdigit():
            atomic_number = int(atomic_input)
        elif atomic_input.capitalize() in atomic_symbols:
            atomic_number = atomic_symbols[atomic_input.capitalize()]

        if atomic_number is not None:
            config = get_electron_configuration(atomic_number)
            valence_electrons = get_valence_electrons(atomic_number)
            results = {'type': 'config', 'config': config, 'valence_electrons': valence_electrons}
        elif 'sublevel' in request.form:
            sublevel = request.form['sublevel']
            electrons = calculate_electrons_in_sublevel(sublevel)
            results = {'type': 'sublevel', 'sublevel': sublevel, 'electrons': electrons}

        
    return render_template('index.html', results=results)


if __name__ == '__main__':

    app.run(debug=True)
