from logger_config import setup_logger
from triangle import process_triangle


def main():
    logger = setup_logger()
    logger.info("Приложение запущено")


    test_cases = [
        ("0.3", "0.4", "0.7"),
        ("авыаы", "авыаы", "авыавы"),
        ("3", "4", "5"),        # разносторонний
        ("7", "7", "7"),        # равносторонний
        ("5", "5", "8"),        # равнобедренный
        ("1", "2", "10"),       # не треугольник
        ("-3", "4", "5"),       # ошибочные числовые (отрицательное)
        ("abc", "4", "5"),      # нечисловые
        ("0", "4", "5"),        # ошибочные числовые (ноль)
    ]

    for a, b, c in test_cases:
        logger.info("=" * 60)
        triangle_type, coords = process_triangle(a, b, c)
        print(f"Вход: ({a}, {b}, {c})")
        print(f"  Тип: {triangle_type!r}")
        print(f"  Координаты: {coords}")
        print()

    logger.info("Приложение завершено")


if __name__ == "__main__":
    main()
    main()