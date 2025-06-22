from app.services.openai_service import generate_help_post

if __name__ == "__main__":
    example_input = "Brauche Hilfe beim Tragen eines Sofas am Samstag."
    post_text, token_count = generate_help_post(example_input, mode="suchen")

    print("\n📣 Generierter Post:\n")
    print(post_text)

    print("\n📊 Tokenverbrauch:")
    print(f"Verwendete Tokens: {token_count}")