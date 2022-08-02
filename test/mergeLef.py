#!/usr/bin/env python3
import re
import sys
import os
import argparse  # argument parsing

# WARNING: this script expects the tech lef first

# Parse and validate arguments
# ==============================================================================
parser = argparse.ArgumentParser(
    description='Merges lefs together')
parser.add_argument('--inputLef', '-i', required=True,
                    help='Input Lef', nargs='+')
parser.add_argument('--outputLef', '-o', required=True,
                    help='Output Lef')
args = parser.parse_args()


print(os.path.basename(__file__),": Merging LEFs")

with open(args.inputLef[0]) as f:
  content = f.read()
# Using a set so we get unique entries
propDefinitions = set()

# Remove Last line ending the library
content = re.sub("END LIBRARY","",content)

# Iterate through additional lefs
for lefFile in args.inputLef[1:]:
  with open(lefFile) as f:
    snippet = f.read()
  # Match the sites
  pattern = r"(^SITE (\S+).*?END\s\2)"
  m = re.findall(pattern, snippet, re.M | re.DOTALL)

  print(f"{os.path.basename(lefFile)}: SITEs matched found: {len(m)}")
  for groups in m:
    content += "\n" + groups[0]


  # Match the macros
  pattern = r"(^MACRO (\S+\s).*?END\s\2)"
  m = re.findall(pattern, snippet, re.M | re.DOTALL)

  print(f"{os.path.basename(lefFile)}: MACROs matched found: {len(m)}")
  for groups in m:
    content += "\n" + groups[0]

  # Match the property definitions
  pattern = r"^(PROPERTYDEFINITIONS)(.*?)(END PROPERTYDEFINITIONS)"
  if m := re.search(pattern, snippet, re.M | re.DOTALL):
    print(f"{os.path.basename(lefFile)}: PROPERTYDEFINITIONS found")
    propDefinitions.update(map(str.strip, m[2].split("\n")))


# Add Last line ending the library
content += "\nEND LIBRARY"

# Update property definitions

# Find property definitions in base lef
pattern = r"^(PROPERTYDEFINITIONS)(.*?)(END PROPERTYDEFINITIONS)"
if m := re.search(pattern, content, re.M | re.DOTALL):
  print(f"{os.path.basename(lefFile)}: PROPERTYDEFINITIONS found in base lef")
  propDefinitions.update(map(str.strip, m[2].split("\n")))


replace = r"\1" + "\n".join(propDefinitions) + r"\n\3"
content = re.sub(pattern, replace, content, 0, re.M | re.DOTALL)

with open(args.outputLef, "w") as f:
  f.write(content)
print(os.path.basename(__file__),": Merging LEFs complete")
