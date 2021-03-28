# battleship_oop

Second version of my implementation of Battleship game in Python - this version is based on OOP. 
Project was created as extra activity during Codecool bootcamp.

Interesting features:

- validation of user input
- Artificiall Intelligence able to:
  - place ships in correct fields
  - shoot smart: 
      - firstly randomized shots, 
      - when hit successfully, trying to hit fields nearby, also in correct direction when hit more than one field, 
      - analyzing if potential shot field is able to be a ship (ship cannot be in neighbourhood of another ship so it does not shot around sunk ships)
