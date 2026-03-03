import random

# ==========================================
# SELEÇÃO DE PALAVRA POR NÍVEL E IDIOMA
# ==========================================

def select_word_by_level(words_data, level, language):
    if level == 1:
        min_len, max_len = 3, 5
    elif level == 2:
        min_len, max_len = 4, 6
    elif level == 3:
        min_len, max_len = 5, 8
    else:
        min_len, max_len = 6, 20

    filtered = []

    for word in words_data:
        length = word["len_pt"] if language == "pt" else word["len_en"]

        if min_len <= length <= max_len:
            filtered.append(word)

    if not filtered:
        return None

    chosen = random.choice(filtered)

    return chosen["pt"] if language == "pt" else chosen["en"]


# ==========================================
# SPAWN SEM SOBREPOSIÇÃO
# ==========================================

def get_spawn_x(existing_words, screen_width, min_distance=150):
    while True:
        x = random.randint(50, screen_width - 200)
        overlap = False

        for word in existing_words:
            if abs(word.x - x) < min_distance:
                overlap = True
                break

        if not overlap:
            return x


# ==========================================
# SISTEMA COMPLETO DE DIFICULDADE
# ==========================================

def calculate_difficulty(level):
    """
    Retorna:
    - velocidade base
    - max palavras simultâneas
    - spawn delay (quanto menor, mais rápido aparece)
    """

    base_speed = 1 + (level * 0.5)

    max_words = min(5, 1 + level)

    # A cada nível diminui 15 frames até mínimo 20
    spawn_delay = max(20, 120 - (level * 15))

    return base_speed, max_words, spawn_delay