import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime


class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Загрузка данных
        self.quotes = self.load_quotes()
        self.history = self.load_history()

        # Переменные для фильтрации
        self.filter_author = tk.StringVar()
        self.filter_topic = tk.StringVar()

        # Настройка интерфейса
        self.setup_ui()

        # Обновление списка истории при запуске
        self.update_history_list()

    def load_quotes(self):
        """Загрузка цитат из JSON-файла или создание стандартных"""
        if os.path.exists("quotes.json"):
            with open("quotes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Стандартные цитаты
            default_quotes = [
                {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
                {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "мотивация"},
                {"text": "Нет ничего невозможного для того, кто пробует.", "author": "Александр Македонский", "topic": "успех"},
                {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "знание"},
                {"text": "Единственный способ сделать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "работа"},
                {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "успех"},
                {"text": "В двух словах я расскажу вам о жизни: она продолжается.", "author": "Роберт Фрост", "topic": "жизнь"},
                {"text": "Никогда не поздно стать тем, кем ты мог бы стать.", "author": "Джордж Элиот", "topic": "мотивация"},
                {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "знание"},
                {"text": "Трудности — это возможности.", "author": "Сенека", "topic": "жизнь"}
            ]
            self.save_quotes(default_quotes)
            return default_quotes

    def save_quotes(self, quotes):
        """Сохранение цитат в JSON"""
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)

    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        """Сохранение истории в JSON"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def setup_ui(self):
        # Верхняя панель с цитатой
        self.quote_frame = tk.LabelFrame(self.root, text="Случайная цитата", padx=10, pady=10)
        self.quote_frame.pack(fill="both", expand=False, padx=10, pady=5)

        self.quote_label = tk.Label(self.quote_frame, text="Нажмите 'Генерировать цитату'", wraplength=650,
                                     font=("Arial", 12), justify="left")
        self.quote_label.pack(fill="both", expand=True)

        self.author_label = tk.Label(self.quote_frame, text="", font=("Arial", 10, "italic"), fg="gray")
        self.author_label.pack()

        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="🎲 Сгенерировать цитату", command=self.generate_quote,
                                       font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.generate_btn.pack(pady=5)

        # Панель фильтрации
        self.filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        self.filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по автору
        tk.Label(self.filter_frame, text="Автор:").grid(row=0, column=0, padx=5, sticky="w")
        authors = sorted(set(q["author"] for q in self.quotes))
        self.author_combo = ttk.Combobox(self.filter_frame, textvariable=self.filter_author,
                                         values=["Все"] + authors, state="readonly")
        self.author_combo.current(0)
        self.author_combo.grid(row=0, column=1, padx=5, pady=5)

        # Фильтр по теме
        tk.Label(self.filter_frame, text="Тема:").grid(row=0, column=2, padx=5, sticky="w")
        topics = sorted(set(q["topic"] for q in self.quotes))
        self.topic_combo = ttk.Combobox(self.filter_frame, textvariable=self.filter_topic,
                                        values=["Все"] + topics, state="readonly")
        self.topic_combo.current(0)
        self.topic_combo.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка применения фильтра
        self.filter_btn = tk.Button(self.filter_frame, text="Применить фильтр", command=self.apply_filter,
                                     bg="#2196F3", fg="white")
        self.filter_btn.grid(row=0, column=4, padx=10)

        # История
        self.history_frame = tk.LabelFrame(self.root, text="История цитат", padx=10, pady=5)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Скроллбар для истории
        scrollbar = tk.Scrollbar(self.history_frame)
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(self.history_frame, yscrollcommand=scrollbar.set,
                                           height=12, font=("Arial", 10))
        self.history_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Кнопки управления историей
        self.history_buttons_frame = tk.Frame(self.root)
        self.history_buttons_frame.pack(pady=5)

        self.clear_history_btn = tk.Button(self.history_buttons_frame, text="Очистить историю",
                                            command=self.clear_history, bg="#f44336", fg="white")
        self.clear_history_btn.pack(side="left", padx=5)

        # Панель добавления новой цитаты
        self.add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=5)
        self.add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.add_frame, text="Текст цитаты:").grid(row=0, column=0, sticky="w")
        self.new_text_entry = tk.Entry(self.add_frame, width=50)
        self.new_text_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.add_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.new_author_entry = tk.Entry(self.add_frame, width=30)
        self.new_author_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        tk.Label(self.add_frame, text="Тема:").grid(row=2, column=0, sticky="w")
        self.new_topic_entry = tk.Entry(self.add_frame, width=20)
        self.new_topic_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        self.add_quote_btn = tk.Button(self.add_frame, text="➕ Добавить цитату", command=self.add_quote,
                                        bg="#FF9800", fg="white")
        self.add_quote_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def generate_quote(self):
        """Генерация случайной цитаты с учётом фильтров"""
        filtered_quotes = self.quotes

        # Применяем фильтры
        if self.filter_author.get() != "Все":
            filtered_quotes = [q for q in filtered_quotes if q["author"] == self.filter_author.get()]
        if self.filter_topic.get() != "Все":
            filtered_quotes = [q for q in filtered_quotes if q["topic"] == self.filter_topic.get()]

        if not filtered_quotes:
            messagebox.showwarning("Нет цитат", "Нет цитат, соответствующих выбранным фильтрам!")
            return

        quote = random.choice(filtered_quotes)

        # Отображение
        self.quote_label.config(text=f"«{quote['text']}»")
        self.author_label.config(text=f"— {quote['author']} (тема: {quote['topic']})")

        # Сохранение в историю
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"]
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history_list()

    def update_history_list(self):
        """Обновление списка истории"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.history):  # Показываем новые сверху
            self.history_listbox.insert(tk.END,
                f"[{entry['timestamp']}] {entry['author']}: {entry['text'][:60]}...")

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_list()
            messagebox.showinfo("История очищена", "История цитат успешно очищена!")

    def apply_filter(self):
        """Применение фильтров и генерация новой цитаты"""
        self.generate_quote()

    def add_quote(self):
        """Добавление новой цитаты"""
        text = self.new_text_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()

        # Проверка корректности ввода
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        if not topic:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return

        # Добавляем цитату
        new_quote = {"text": text, "author": author, "topic": topic}
        self.quotes.append(new_quote)
        self.save_quotes(self.quotes)

        # Обновляем фильтры
        authors = sorted(set(q["author"] for q in self.quotes))
        topics = sorted(set(q["topic"] for q in self.quotes))
        self.author_combo["values"] = ["Все"] + authors
        self.topic_combo["values"] = ["Все"] + topics

        # Очищаем поля ввода
        self.new_text_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Цитата от {author} успешно добавлена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
