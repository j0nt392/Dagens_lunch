def handle_response(message) -> str:
    p_message = message.lower()

    if "dagenslunch" in p_message:
        return "lunch"

    return ""