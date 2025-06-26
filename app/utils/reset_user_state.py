from app.db.db import get_db_connection

def reset_user_state(user_number: str):
    """
    Setzt den Status eines Nutzers vollständig zurück:
    - Verlauf löschen (whatsapp_messages)
    - Session löschen (whatsapp_sessions)
    - Sync-Status zurücksetzen (falls vorhanden)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verlauf löschen
    cursor.execute("DELETE FROM whatsapp_messages WHERE user_number = ?", (user_number,))

    # Session löschen
    cursor.execute("DELETE FROM whatsapp_sessions WHERE user_number = ?", (user_number,))

    conn.commit()
    conn.close()

    # Optional: In-Memory-Cache (z. B. synced_numbers) resetten
    try:
        from app.webhook.twilio_webhook import synced_numbers
        if user_number in synced_numbers:
            synced_numbers.remove(user_number)
    except ImportError:
        pass  # Wenn kein Zugriff auf Blueprint oder `synced_numbers`, ignoriere

    print(f"🔄 Reset für {user_number} durchgeführt.")