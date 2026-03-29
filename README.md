# Python Chess AI (Wooden Edition)

A fully interactive Chess game built with Python, Pygame, and the python-chess library. This project features a custom-built AI opponent that utilizes advanced search algorithms to simulate intelligent gameplay.

## Algorithms Used

This engine is powered by the **Minimax Algorithm** enhanced with **Alpha-Beta Pruning**. Minimax allows the AI to evaluate the best possible move by simulating future game states, while Alpha-Beta Pruning significantly optimizes performance by discarding branches of the search tree that do not influence the final decision.

## Features

- **Custom AI Engine:** Play against an AI that evaluates thousands of possible move combinations.
- 
- **Variable Difficulty:** Toggle between Easy, Medium, and Hard modes in real-time.
- 
- **Classic Aesthetic:** A wooden-themed board with top-left algebraic coordinates (a1-h8).
- 
- **Tactile Feedback:** Integrated sound effects for standard moves and piece captures.
- 
- **Human-Like Pacing:** An artificial thinking delay ensures the AI doesn't move instantly, making the game feel more natural.
- 
- **Smart Selection:** Highlights the currently selected piece to prevent misclicks.
- 
- **Game Over Interface:** Clear visual overlay for Checkmate, Stalemate, or Draw results with a quick "Press R to Restart" feature.

## Technical Overview

The core of the computer's intelligence is a Minimax Search Tree.

1. **Evaluation:** The AI calculates a score for the board by weighing the material value of pieces (e.g., Queen = 90, Pawn = 10).

2. **Recursive Search:** It simulates its own best moves while assuming the human player will also play optimally.
 
3. **Alpha-Beta Pruning:** To keep the game fast, the AI prunes (ignores) branches of the move tree that it knows will lead to a worse outcome than moves already calculated.
   
4. **Difficulty Scaling:**
   
   - **Easy:** Looks 1 move ahead (shallow search).
     
   - **Hard:** Looks 3+ moves ahead (deep strategic search).

## Installation and Setup

### 1. Clone the Repository

git clone https://github.com/yourusername/minimax-chess-engine.git

cd minimax-chess-engine

### 2. Install Dependencies

This project requires pygame for the interface and python-chess for move validation.

pip install pygame python-chess

### 3. Organize Assets

Ensure your directory looks like this:

• main.py

• assets/

   • Piece images: wP.png, bK.png, etc.

   • Sounds: move.wav, capture.wav
   
### 4. Run the Game

python main.py

