import tkinter as tk
from tkinter import ttk



def create_files():
    try:
        N = int(entry.get())  # Получаем число N от пользователя

        # Проверка, что N является положительным числом
        if N <= 0:
            lab.config(text="Введите положительное число.")
            return

        for i in range(1, N + 1):
            filename = f"{i}.md"
            with open(filename, "w") as f:
                f.write(f"")
            #     f.write(f"## \n\n")  # Запись заголовка
            #     f.write(f"```python\n\n```")  # Запись блока кода

        lab.config(text=f"Создано {N} файлов.")
        success_message()  # Вызов сообщения об успешном завершении

    except ValueError:
        lab.config(text="Пожалуйста, введите целое число.")
    except Exception as e:
        lab.config(text=f"Произошла ошибка: {e}")


def success_message():
    lab.config(text="Файлы успешно созданы!")
    root.after(1000, root.destroy)  # Закрытие окна через 1 секунду


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('400x200')
    root.title('Создание Markdown файлов')

    # Метка для ввода
    lbl = ttk.Label(root, text='Введите число N:')
    lbl.pack(pady=10)

    # Поле ввода
    entry = ttk.Entry(root)
    entry.pack(pady=10)

    # Кнопка для создания файлов
    btn = ttk.Button(root, text='Создать файлы', command=create_files)
    btn.pack(pady=10)

    # Метка для отображения результата
    lab = ttk.Label(root, text='', font=5)
    lab.pack(pady=10)

    root.mainloop()
