#!/bin/bash

# Define lists of main coordinates, linked coordinates, and the color to check
main_coords=(
#1st field
"448,126"
"404,127"
"362,125"
"444,163"
"403,163"
"361,161"
"445,205"
"404,205"
"364,204"
#2nd field
"446,294"
"404,291"
"363,294"
"446,334"
"404,332"
"364,333"
"450,375"
"405,373"
"362,375"
#3d field
"487,460"
"447,460"
"404,461"
"486,499"
"445,499"
"406,497"
"487,541"
"444,538"
"407,542"
#4th field
"489,630"
"447,629"
"405,629"
"489,667"
)

linked_coords=(
#1st field
"438,141"
"395,140"
"353,141"
"437,183"
"395,182"
"354,181"
"436,224"
"395,226"
"354,224"
#2nd field
"436,309"
"392,308"
"354,308"
"437,352"
"395,351"
"351,350"
"435,394"
"392,393"
"351,392"
#3rd field
"477,475"
"436,477"
"392,477"
"478,519"
"434,518"
"393,519"
"478,561"
"435,561"
"391,560"
#4th field
"479,646"
"438,647"
"394,646"
"479,688"
)

target_color="255 255 255"
target_color1="252 254 251"
target_color2="251 253 254"

# Loop through the coordinates
for i in "${!main_coords[@]}"; do
  main_coord="${main_coords[$i]}"
  linked_coord="${linked_coords[$i]}"

  # Get the color at the linked coordinate
  color=$(cliclick cp:$linked_coord)

  echo "Checking color at $linked_coord: $color"

  # Compare the color with the target color
  if [ "$color" == "$target_color" ]||[ "$color" == "$target_color1" ]||[ "$color" == "$target_color2" ]; then
    echo "Color matches at $linked_coord. Skipping click at $main_coord."
  else
    echo "Color does not match. Clicking at $main_coord."
    cliclick c:$main_coord
  fi

done