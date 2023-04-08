N = int(input("Введите число N: "))  # получаем число N от пользователя

# создаем файлы step_1.md, step_2.md, и т.д., до step_N.md
for i in range(1, N+1):
    filename = f"{i}.md"
    with open(filename, "w") as f:
        f.write(f"## ")
        f.write(f"\n\n")
        f.write(f"```python\n\n```")

