import streamlit as st
import torch
import random
import re
import math
import copy
from Transformer import Transformer
import matplotlib.pyplot as plt

# Load model
src_vocab_size = 29
tgt_vocab_size = 29
d_model = 256
num_heads = 8
num_layers = 6
d_ff = 1024
max_seq_length = 30
dropout = 0.1

transformer = Transformer(src_vocab_size, tgt_vocab_size, d_model, num_heads, 
                         num_layers, d_ff, max_seq_length, dropout)

PATH = "transformer_model.pth"
state_dict = torch.load(PATH, map_location=torch.device('cpu'))
transformer.load_state_dict(state_dict)
transformer.eval()

# Vocabulary
int_to_str = {0: '_', 1: '<sos>', 2: 'a', 3: 'b', 4: 'c',5: 'd', 6: 'e',
              7: 'f', 8: 'g', 9: 'h', 10: 'i', 11: 'j', 12: 'k', 13: 'l',
              14: 'm', 15: 'n', 16: 'o', 17: 'p', 18: 'q', 19: 'r', 20: 's',
              21: 't', 22: 'u', 23: 'v', 24: 'w', 25: 'x', 26: 'y', 27: 'z',
              28: '<PAD>'}

str_to_int = {v:k for k,v in int_to_str.items()}

# Helper functions
def tokenize_word(word):
    encoded = [str_to_int.get(c, 0) for c in word]
    if len(encoded) < 29:
        encoded = [str_to_int['<PAD>']]*(29-len(encoded)) + encoded
    elif len(encoded) > 29:
        encoded = encoded[:29]
    return torch.tensor(encoded + [str_to_int['<sos>']], dtype=torch.long)

def decode(embed):
    return int_to_str.get(embed, '_')

# Game parameters
MAX_LIVES = 6

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = {
        'target_word': '',
        'guessed_letters': [],
        'current_state': [],
        'lives_remaining': MAX_LIVES,
        'game_over': False,
        'status': ''
    }

# Load sample dictionary
with open("words_250000_train.txt") as f:  # Replace with your word list
    full_dictionary = [word.strip().lower() for word in f.readlines()]

def start_new_game():
    st.session_state.game = {
        'target_word': random.choice(full_dictionary),
        'guessed_letters': [],
        'current_state': ['_']*len(st.session_state.game['target_word']),
        'lives_remaining': MAX_LIVES,
        'game_over': False,
        'status': ''
    }

def make_guess():
    if st.session_state.game['game_over']:
        return
    
    # Prepare input
    masked_word = ''.join(st.session_state.game['current_state'])
    guessed_letters = st.session_state.game['guessed_letters']
    
    # Transform input
    encoded_word = tokenize_word(masked_word)
    input_tensor = encoded_word.unsqueeze(0)
    
    # Get model output
    with torch.no_grad():
        output = transformer(input_tensor, input_tensor[:, 1:])
    
    logits = output[:, -1, :]
    
    # Mask already guessed letters
    for letter in guessed_letters:
        logits[0, str_to_int[letter]] = -float('inf')
    
    # Apply regex filtering
    pattern = masked_word.replace('_', '.')
    candidates = [word for word in full_dictionary 
                 if re.fullmatch(pattern, word) and len(word) == len(masked_word)]
    
    # Find valid prediction
    while True:
        pred_idx = torch.argmax(logits, dim=1).item()
        predicted_char = decode(pred_idx)
        
        valid = any(predicted_char in word for word in candidates)
        if valid or (logits == -float('inf')).all():
            break
        logits[0, pred_idx] = -float('inf')
    
    # Update game state
    st.session_state.game['guessed_letters'].append(predicted_char)
    
    if predicted_char in st.session_state.game['target_word']:
        # Reveal letters
        new_state = list(st.session_state.game['current_state'])
        for i,c in enumerate(st.session_state.game['target_word']):
            if c == predicted_char:
                new_state[i] = predicted_char
        st.session_state.game['current_state'] = new_state
    else:
        st.session_state.game['lives_remaining'] -= 1
    
    # Check game over
    if '_' not in st.session_state.game['current_state']:
        st.session_state.game['game_over'] = True
        st.session_state.game['status'] = 'won'
    elif st.session_state.game['lives_remaining'] <= 0:
        st.session_state.game['game_over'] = True
        st.session_state.game['status'] = 'lost'

# Streamlit UI
st.title("🤖 Transformer Hangman AI")

col1, col2 = st.columns([3, 1])
with col1:
    st.header("Game Board")
with col2:
    if st.button("New Game"):
        start_new_game()

if st.session_state.game['target_word']:
    # Display game state
    st.subheader("Word: " + " ".join(st.session_state.game['current_state']))
    st.write(f"Lives remaining: {st.session_state.game['lives_remaining']}")
    st.write(f"Guessed letters: {', '.join(sorted(st.session_state.game['guessed_letters']))}")

    if not st.session_state.game['game_over']:
        if st.button("Make AI Guess"):
            make_guess()
    else:
        if st.session_state.game['status'] == 'won':
            st.success("🎉 AI won! The word was: " + st.session_state.game['target_word'])
        else:
            st.error("💀 AI lost! The word was: " + st.session_state.game['target_word'])

else:
    st.write("Click 'New Game' to start!")

# Visualization
st.markdown("---")
st.subheader("Game Progress")
if st.session_state.game['target_word']:
    progress = 1 - (st.session_state.game['current_state'].count('_') / len(st.session_state.game['target_word']))
    st.progress(progress)
    
    fig, ax = plt.subplots()
    ax.barh(['Lives'], [st.session_state.game['lives_remaining']], color='green')
    ax.set_xlim(0, MAX_LIVES)
    st.pyplot(fig)