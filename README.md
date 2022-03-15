# Heegaard-SVG

This .py code generates .svg files showing genus-zero Heegaard diagrams for the 3-sphere adapted to any specified pretzel link, shown in bridge position.  These can be changed to higher genus diagrams manually by replacing basepoint pairs with handle attachments.  All user input (twist coefficients, stylistic choices) is taken at the top of the code.

"hexagons=False" will introduce finger moves as needed (i.e., any time twist coefficient parity changes) to ensure that the polar region is the only elementary region that is not a 2-gon or 4-gon.  "hexagons=True" will leave the hexagons there.
