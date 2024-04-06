def log_print(text):
    with open("log.txt", "a+") as f:
        f.write(f"{text}\n")