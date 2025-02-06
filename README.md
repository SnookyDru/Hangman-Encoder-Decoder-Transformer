# Hangman-Encoder-Decoder-Transformer

[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-green)](https://hangman-transformer.streamlit.app/)

Hangman Transformer AI is an interactive web application that uses a custom encoder–decoder Transformer model to play the game of Hangman. The app is deployed on Streamlit and demonstrates state-of-the-art sequence prediction techniques with a novel twist: the model is designed not to guess letters that have already been revealed or previously guessed.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Model Architecture](#model-architecture)
- [Data Preparation](#data-preparation)
- [Usage](#usage)
- [Installation](#installation)
- [Deployment](#deployment)
- [License](#license)

## Overview

This project leverages an encoder–decoder Transformer architecture to play Hangman. The model was trained on a specially prepared dataset, where every word from a provided dictionary was converted into multiple masked states along with the optimal guess letter as the target. In addition to the transformer prediction, the system integrates a candidate frequency analysis mechanism to further refine the guess. The end result is a robust AI that achieves a prediction accuracy exceeding 50% on the Hangman challenge.

The application features a user-friendly Streamlit interface that displays the current masked word, the remaining lives, and the letters already guessed. The AI automatically makes guesses when prompted, and the game state is updated in real time.

## Features

- **Interactive UI:** A modern Streamlit interface for live gameplay.
- **Custom Transformer Model:** An encoder–decoder architecture that processes masked word states.
- **Inference-Time Masking:** The model masks out letters that are already revealed or previously guessed.
- **Candidate Frequency Analysis:** Combines the transformer’s probability distribution with candidate frequency statistics from a full dictionary to choose the best guess.
- **Game Visualization:** Displays a progress bar, lives remaining, and guessed letters.
- **Deployed Online:** Accessible at [https://hangman-transformer.streamlit.app/](https://hangman-transformer.streamlit.app/)

## Model Architecture

The Transformer model used in this project includes:
- **Encoder:**  
  - Embedding layer to convert source tokens into dense vectors.
  - Positional encoding to incorporate token order.
  - Multiple encoder layers featuring multi-head self-attention and feed-forward networks.
- **Decoder:**  
  - Embedding and positional encoding for target tokens.
  - Multiple decoder layers that employ both self-attention and cross-attention with the encoder output.
  - A final linear projection layer to predict logits over the target vocabulary.

### Hyperparameters

- **Vocabulary Size:** 29 tokens (includes letters, `<sos>`, and `<PAD>`)
- **Model Dimension (`d_model`):** 256
- **Number of Attention Heads (`num_heads`):** 8
- **Number of Layers:** 6 encoder and 6 decoder layers
- **Feed-Forward Dimension (`d_ff`):** 1024
- **Maximum Sequence Length:** 30
- **Dropout:** 0.1
- **Optimizer:** Adam (learning rate: 0.0001, betas: (0.9, 0.98), epsilon: 1e-9)

## Data Preparation

The training dataset was created from a word dictionary by generating every possible masked state of each word along with the corresponding optimal guess letter. The dataset was preprocessed as follows:

- **Masked Variants:** Each word was converted into multiple masked states (with unknown letters as “_”).
- **Target Generation:** The ideal next-letter guess was paired with each masked state.
- **Left Padding:** Sequences were left-padded to a fixed length (based on the longest word) for consistency.
- **Tokenization:** A custom mapping was used to convert letters (a–z) and special tokens (`<sos>`, `<PAD>`) into numerical indices.

## Usage

To play a game of Hangman with the AI:

1. Visit the deployed Streamlit app at [https://hangman-transformer.streamlit.app/](https://hangman-transformer.streamlit.app/).
2. Click on **New Game** to start a new session.
3. The game board displays the masked word, the number of remaining lives, and previously guessed letters.
4. Click **Make AI Guess** to have the Transformer model generate the next guess.
5. The game will update in real time, displaying a progress bar and a visual of remaining lives.

## Installation

To run this project locally:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/hangman-encoder-decoder-transformer.git
    cd hangman-transformer-ai
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit App:**

    ```bash
    streamlit run hangman_app.py
    ```

Make sure you have the following files in your repository:
- `hangman_app.py`: The main Streamlit application code.
- `transformer_model.pth`: The trained transformer model weights.
- `words.txt`: The dictionary of words used for game initialization.
- All transformer model source code (or a module) included in your project.

## Deployment

This project is deployed on Streamlit and is accessible at:  
[https://hangman-transformer.streamlit.app/](https://hangman-transformer.streamlit.app/)

---

Feel free to reach out with any questions or feedback.

Best regards,

Dhruv Kumar  
Global Alpha Researcher, India  
+91 9560623783  
[LinkedIn](#) | [GitHub](#)

---