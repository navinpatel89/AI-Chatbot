from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Model name
model_name = "facebook/blenderbot-400M-distill"

# Load model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Chatbot ready! (type 'exit' to quit)\n")

# Store conversation history
conversation_history = []

while True:
    # Keep only recent conversation
    conversation_history = conversation_history[-6:]

    # Convert conversation history to a string
    history_string = "\n".join(conversation_history)

    # Get user input
    input_text = input("> ")

    # Exit chatbot
    if input_text.lower() == "exit":
        break

    # Build prompt
    prompt = history_string + f"\nUser: {input_text}\nBot:"

    # Tokenize input
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate response
    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        no_repeat_ngram_size=3,
        repetition_penalty=1.3,
        do_sample=True,
        temperature=0.6,
        top_p=0.85
    )

    # Decode response
    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    # Display response
    print("Bot:", response)

    # Save conversation
    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot: {response}")