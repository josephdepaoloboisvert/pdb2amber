import os, sys

# USAGE quick_xml.py yourpdb.pdb net_charge_as_int
#ASSUMING YOU ALREADY HAVE A LIGAND WITH HYDROGENS
#USE A FULL PATH
try:
    my_pdb = sys.argv[1]
    name = my_pdb.replace('.pdb','')
    nc = int(sys.argv[2])
except:
    raise Exception("Check Usage")

if os.path.isfile(f"{name}.ff.xml"):
    raise Exception("xml already exist")

s_ante = f"antechamber -fi pdb -fo mol2 -i {name}.pdb -o {name}.mol2 -c bcc -pf y -nc {nc}"

os.system(s_ante)

s_parm = f"parmchk2 -i {name}.mol2 -o {name}.frcmod -f mol2"

os.system(s_parm)

s_leap = f"""source leaprc.gaff2
mol = loadmol2 {name}.mol2
loadamberparams {name}.frcmod
saveamberparm mol {name}.prmtop {name}.inpcrd
quit"""

with open('run_tleap.in', 'w') as f:
    f.write(s_leap)

os.system("tleap -s -f run_tleap.in")

s_json = ["{",
         f'    "fname_prmtop" : "{name}.prmtop",',
         f'    "fname_xml" : "{name}.ff.xml",',
          '    "ff_prefix" : "lig"',
          '}']

with open('run_python.json', 'w') as g:
    g.writelines(s_json)

os.system("python /ocean/projects/che210038p/josephdb/NQR_2022_B/pdb2amber/build_forcefield/write_xml_pretty.py -i run_python.json")
