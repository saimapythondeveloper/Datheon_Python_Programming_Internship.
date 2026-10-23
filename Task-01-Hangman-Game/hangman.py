
import random

# Read words from words.txt
with open("words.txt", "r") as file:
    words = [
        line.strip().lower()
        for line in file
        if line.strip().isalpha()
    ]

if not words:
    raise ValueError("No valid words found in words.txt")


# ASCII art: starting stage + 6 incorrect guesses
stages = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


def display_word(secret_word, guessed_letters):
    """Show guessed letters and hide the remaining letters."""
    display = []

    for letter in secret_word:
        if letter in guessed_letters:
            display.append(letter.upper())
        else:
            display.append("_")

    return " ".join(display)


def play_hangman():
    secret_word = random.choice(words)
    guessed_letters = set()
    wrong_guesses = set()
    max_attempts = 6

    print("\nWelcome to Hangman!")
    print("Guess the hidden word one letter at a time.")
    print(f"You have {max_attempts} incorrect guesses.")

    # Continue only while fewer than 6 incorrect guesses have occurred
    while len(wrong_guesses) < max_attempts:

        # Show the current stage
        print(stages[len(wrong_guesses)])
        print("\nWord:", display_word(secret_word, guessed_letters))

        # Check whether the player has won
        if all(letter in guessed_letters for letter in secret_word):
            print("\nCongratulations! You guessed the word!")
            print("The word was:", secret_word.upper())
            return

        print("Incorrect guesses left:", max_attempts - len(wrong_guesses))
        print(
            "Guessed letters:",
            ", ".join(sorted(guessed_letters))
            if guessed_letters else "None"
        )

        guess = input("\nEnter a letter: ").strip().lower()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one alphabetic letter.")
            continue

        # Duplicate guesses do not use an attempt
        if guess in guessed_letters:
            print("You already guessed that letter. Try another.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
        else:
            wrong_guesses.add(guess)
            print("Wrong guess!")

            # Display the updated drawing immediately
            print(stages[len(wrong_guesses)])

            # Stop immediately on the sixth incorrect guess
            if len(wrong_guesses) == max_attempts:
                print("\nGame over! You ran out of attempts.")
                print("The hidden word was:", secret_word.upper())
                return


# Start the game
play_hangman()
