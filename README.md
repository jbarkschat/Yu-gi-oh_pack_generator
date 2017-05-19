# Yu-gi-oh_pack_generator
Python program to generate yu-gi-oh booster packs for use in tabletop simulator.

Warning: Extremely alpha software, many bugs present.

Usage: Download the zipped program from releases.
       Unzip into the location of your choice(Desktop works fine)
       Run Yu-gi-oh_pack_generator_alpha.exe
       Choose booster packs(Other options do not currently work correctly)
       Choose which booster pack you want to generate
       Give it a minute, on slower connections the program may act like it is frozen while downloading the images
       Check the results folder for the composite_image.png, this file can be imported into tabletop simulator
       For now, all booster packs generate 9 cards, so when making a custom deck in tabletop sim, settings should be:
          Face: link or local path
          Unique backs: unchecked
          Back: link or local path(find an image of the back of a yu-gi-oh card online)
          Width: 3
          Height 3
          Number: 9
          Sideways:unchecked
          Back is hidden: checked
          
This program uses BeautifulSoup to access the official site for yu-gi-oh and pull information about booster packs from it.
It then pulls images from the yu-gi-oh wiki using BS and stitches them together using Pillow.
The composite image it produces can then be uploaded to a file sharing site, or used locally in tabletop simulator as a booster pack.
