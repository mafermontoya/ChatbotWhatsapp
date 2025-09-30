# message_splitter.py

def split_message(text, max_chars=1500, max_lines=3):
    """
    Divide un mensaje largo en partes más pequeñas.
    - max_chars: máximo de caracteres por chunk
    - max_lines: máximo de líneas por chunk
    """
    parts = []
    current = []
    current_len = 0

    for line in text.splitlines():
        # Si la línea sola es demasiado larga, la partimos
        while len(line) > max_chars:
            parts.append(line[:max_chars])
            line = line[max_chars:]

        if (current_len + len(line) > max_chars) or (len(current) >= max_lines):
            # Guardar chunk actual
            parts.append("\n".join(current))
            current = []
            current_len = 0

        current.append(line)
        current_len += len(line)

    if current:
        parts.append("\n".join(current))

    # Limpiar vacíos
    return [p.strip() for p in parts if p.strip()]
