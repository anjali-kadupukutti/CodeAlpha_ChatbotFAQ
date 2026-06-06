import tkinter as tk
from tkinter import scrolledtext
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)

# FAQ Data
faq_data = {
    "What is artificial intelligence?": "Artificial Intelligence (AI) is the simulation of human intelligence by machines to perform tasks like learning, reasoning, and problem-solving.",
    "What is machine learning?": "Machine Learning is a subset of AI where machines learn from data and improve their performance without being explicitly programmed.",
    "What is deep learning?": "Deep Learning is a subset of machine learning that uses neural networks with many layers to learn complex patterns from data.",
    "What is Python?": "Python is a popular high-level programming language widely used in AI, machine learning, web development, and data science.",
    "What is NLP?": "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language.",
    "What is a neural network?": "A neural network is a series of algorithms that mimic the human brain to recognize patterns and solve complex problems.",
    "What is data science?": "Data Science is a field that uses statistics, programming, and machine learning to extract insights from data.",
    "What is computer vision?": "Computer Vision is a field of AI that enables computers to interpret and understand visual information from images and videos.",
    "What is reinforcement learning?": "Reinforcement Learning is a type of machine learning where an agent learns by interacting with an environment and receiving rewards or penalties.",
    "What is a chatbot?": "A chatbot is an AI program that simulates conversation with humans using natural language processing techniques.",
    "What is data mining?": "Data Mining is the process of discovering patterns and insights from large datasets using statistical and machine learning techniques.",
    "What is a dataset?": "A dataset is a collection of data used to train, test, and evaluate machine learning models.",
    "What is overfitting?": "Overfitting occurs when a machine learning model learns the training data too well and performs poorly on new unseen data.",
    "What is a algorithm?": "An algorithm is a set of step-by-step instructions given to a computer to solve a problem or perform a task.",
    "What is big data?": "Big Data refers to extremely large datasets that cannot be processed using traditional methods and require special tools and techniques."
}

questions = list(faq_data.keys())
answers = list(faq_data.values())

def get_response(user_input):
    temp_questions = questions + [user_input]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(temp_questions)
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]
    if best_score < 0.2:
        return "❌ Sorry, I don't have an answer for that. Please ask something related to AI!"
    return answers[best_match_index]

def send_message(event=None):
    user_input = entry.get().strip()
    if user_input == "":
        return
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "🧑 You: " + user_input + "\n", "user")
    response = get_response(user_input)
    chat_box.insert(tk.END, "🤖 Bot: " + response + "\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)
    entry.delete(0, tk.END)

# Window setup
root = tk.Tk()
root.title("AI FAQ Chatbot")
root.geometry("700x550")
root.config(bg="#0f0f1a")
root.resizable(False, False)

# Title bar
title_frame = tk.Frame(root, bg="#1a1a2e", pady=10)
title_frame.pack(fill=tk.X)
tk.Label(title_frame, text="🤖 AI FAQ Chatbot", font=("Arial", 20, "bold"), bg="#1a1a2e", fg="#00d4ff").pack()
tk.Label(title_frame, text="Ask me anything about Artificial Intelligence!", font=("Arial", 10), bg="#1a1a2e", fg="#888888").pack()

# Chat box
chat_frame = tk.Frame(root, bg="#0f0f1a")
chat_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

chat_box = scrolledtext.ScrolledText(chat_frame, height=22, width=75, state=tk.DISABLED, bg="#1a1a2e", fg="#ffffff", font=("Arial", 11), bd=0, relief=tk.FLAT, wrap=tk.WORD)
chat_box.pack()
chat_box.tag_config("user", foreground="#00d4ff", font=("Arial", 11, "bold"))
chat_box.tag_config("bot", foreground="#00ff99", font=("Arial", 11))

# Input area
input_frame = tk.Frame(root, bg="#0f0f1a")
input_frame.pack(pady=10)

entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bg="#1a1a2e", fg="white", insertbackground="white", relief=tk.FLAT, bd=5)
entry.pack(side=tk.LEFT, padx=5, ipady=8)
entry.bind("<Return>", send_message)

tk.Button(input_frame, text="Send 🚀", command=send_message, bg="#00d4ff", fg="#0f0f1a", font=("Arial", 12, "bold"), relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT)

# Welcome message
chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END, "🤖 Bot: Hello! I am your AI FAQ Chatbot! Ask me anything about AI, Machine Learning, Python and more!\n\n", "bot")
chat_box.config(state=tk.DISABLED)

root.mainloop()
