# battleship_oop

Second implementation of Battleship game in Python - OOP version. Created as extra activity during Codecool bootcamp.

Interesting features:

- validation of user input
- Artificiall Intelligence able to:
  - place ships in correct fields
  - shoot smart: 
      - firstly randomized shots, 
      - when hit trying to hit in correct direction, 
      - analyzing if potential shot field is able to be a ship (ship cannot be in neighbourhood of another ship so it does not shot around sunk ships)
