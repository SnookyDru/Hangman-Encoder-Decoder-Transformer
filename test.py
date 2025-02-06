import tiktoken
enc = tiktoken.get_encoding("gpt2")
print(enc.n_vocab)
print(enc.encode("hii world"))
print(enc.encode("hello there hii"))
