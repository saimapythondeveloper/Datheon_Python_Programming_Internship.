# Python Hangman Game 🎮

A console-based Hangman Word Guessing Game built with Python as part of my internship task at Datheon.

## Features

- Random word selection from a text file
- Interactive letter-by-letter guessing
- ASCII Hangman art that updates after incorrect guesses
- Maximum of 6 incorrect guesses
- Tracks previously guessed letters
- Prevents duplicate guesses from consuming attempts
- Input validation
- Victory and defeat messages

## Technologies Used

- Python 3
- Random module
- File handling
- Functions, loops, conditions, and sets

## Project Structure

```text
python-hangman-game/
├── hangman.py
├── words.txt
└── README.md
```

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Make sure `hangman.py` and `words.txt` are in the same folder.
4. Open the terminal in the project folder.
5. Run:

```bash
python hangman.py
```

## How to Play

- Guess the hidden word one letter at a time.
- Correct guesses reveal letters.
- Each incorrect guess updates the Hangman drawing.
- You can make up to 6 incorrect guesses.
- Repeated guesses do not consume attempts.

## Author

Created as a Python internship project at Datheon.
