import logging
import math
from typing import List, Tuple

logger = logging.getLogger("TriangleApp")

Point = Tuple[int, int]
Coords = List[Point]

INVALID_NUMERIC_POINT: Point = (-1, -1)   # ошибочные числовые
INVALID_STRING_POINT: Point = (-2, -2)    # нечисловые

CANVAS_SIZE = 100
MARGIN = 10


def _parse_side(raw: str, name: str) -> float:
    value = float(raw.strip())
    logger.debug(f"Сторона {name}: успешно распознана как число {value}")
    return value


def _classify_triangle(a: float, b: float, c: float) -> str:
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"
    if a == b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def _compute_vertices(a: float, b: float, c: float) -> Coords:
    ax, ay = 0.0, 0.0
    bx, by = c, 0.0

    cos_a = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
    cos_a = max(-1.0, min(1.0, cos_a))
    sin_a = math.sqrt(max(0.0, 1.0 - cos_a ** 2))

    cx = b * cos_a
    cy = b * sin_a

    points = [(ax, ay), (bx, by), (cx, cy)]

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    width = max_x - min_x
    height = max_y - min_y

    usable = CANVAS_SIZE - 2 * MARGIN
    scale_x = usable / width if width > 0 else 1.0
    scale_y = usable / height if height > 0 else 1.0
    scale = min(scale_x, scale_y)

    result: Coords = []
    for (x, y) in points:
        sx = int(round((x - min_x) * scale)) + MARGIN
        sy = int(round((y - min_y) * scale)) + MARGIN
        sy = CANVAS_SIZE - sy
        sx = max(0, min(CANVAS_SIZE, sx))
        sy = max(0, min(CANVAS_SIZE, sy))
        result.append((sx, sy))

    return result


def process_triangle(raw_a: str, raw_b: str, raw_c: str) -> Tuple[str, Coords]:
    logger.info(
        f"Запрос на обработку треугольника: A='{raw_a}', B='{raw_b}', C='{raw_c}'"
    )

    try:
        a = _parse_side(raw_a, "A")
        b = _parse_side(raw_b, "B")
        c = _parse_side(raw_c, "C")
    except (ValueError, TypeError):
        logger.error("Невалидные (нечисловые) входные данные")
        logger.exception("Трассировка ошибки парсинга:")
        coords = [INVALID_STRING_POINT] * 3
        logger.info(f"Результат: тип='', координаты={coords}")
        return "", coords

    if a <= 0 or b <= 0 or c <= 0:
        logger.warning(
            f"Ошибочные числовые данные (не положительные): A={a}, B={b}, C={c}"
        )
        coords = [INVALID_NUMERIC_POINT] * 3
        logger.info(f"Результат: тип='не треугольник', координаты={coords}")
        return "не треугольник", coords

    try:
        triangle_type = _classify_triangle(a, b, c)
        logger.debug(f"Вид треугольника определён: {triangle_type}")

        if triangle_type == "не треугольник":
            coords = [INVALID_NUMERIC_POINT] * 3
            logger.info(f"Результат: тип='{triangle_type}', координаты={coords}")
            return triangle_type, coords

        coords = _compute_vertices(a, b, c)
        logger.info(f"Результат: тип='{triangle_type}', координаты={coords}")
        return triangle_type, coords

    except Exception:
        logger.error("Непредвиденная ошибка при обработке треугольника")
        logger.exception("Трассировка:")
        coords = [INVALID_NUMERIC_POINT] * 3
        return "не треугольник", coords