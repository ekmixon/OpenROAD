import opendbpy as odb
import os 

current_dir = os.path.dirname(os.path.realpath(__file__))
tests_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
opendb_dir = os.path.abspath(os.path.join(tests_dir, os.pardir))
data_dir = os.path.join(tests_dir, "data")

db = odb.dbDatabase.create()
lib = odb.read_lef(db, os.path.join(data_dir, "gscl45nm.lef"))
if lib is None:
    exit("Lib not created")

tech = db.getTech()
if tech is None:
    exit("Tech not created")

via_rules = tech.getViaRules()

if via_rules is None:
    exit("Via rules not found")
