"""
Multi-language support (i18n) for TweetDuel.
Supports: English (en), Turkish (tr), Spanish (es), German (de), French (fr).
"""

from typing import Dict, Optional

# Translation keys -> { lang_code -> text }
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_title": "TweetDuel",
        "app_subtitle": "The AI Debate Champion",
        "enter_tweet_url": "Enter tweet URL",
        "scraping": "Scraping tweet and replies...",
        "scraping_replies": "Scraping replies...",
        "analyzing": "Analyzing {count} replies...",
        "analyzing_reply": "Analyzing reply {current}/{total}...",
        "no_replies": "No replies found for this tweet.",
        "save_to_armory_prompt": "Save responses to armory for later deployment?",
        "duel_saved": "Duel saved to: {path}",
        "armory_saved": "Responses saved to armory: {path}",
        "original_tweet": "Original Tweet",
        "reply": "Reply",
        "counter_attack": "Counter-Attack",
        "instant_mode": "INSTANT DUEL MODE",
        "sniper_mode": "SNIPER MODE",
        "armory_mode": "ARMORY MODE",
        "sniper_watching": "Watching for new replies... (Press Ctrl+C to stop)",
        "sniper_concept": "Sniper mode would monitor for new replies and auto-generate counters.",
        "armory_generating": "Generating and saving responses for strategic deployment...",
        "armory_done": "All responses saved to armory for strategic deployment!",
        "ollama_connected": "Ollama connected. Available models: {models}",
        "ollama_not_running": "Ollama not running. Please start Ollama first:",
        "no_url": "No tweet URL provided.",
        "interrupted": "Duel interrupted by user.",
        "error_extracting_id": "Error extracting tweet ID: {e}",
        "error_scraping": "Error scraping tweet: {e}",
        "error_analyzing": "Error analyzing arguments: {e}",
        "error_generating": "Error generating response: {e}",
        "persona_socrates": "Socrates",
        "persona_machiavelli": "Machiavelli",
        "persona_chomsky": "Chomsky",
        "persona_tate": "Tate",
        "persona_neutral": "Neutral",
        "report_generated": "Report generated: {path}",
        "thread_prediction": "Thread Prediction",
        "prediction_title": "Where this thread might go",
        "post_approval": "Post this reply to Twitter?",
        "post_success": "Posted successfully.",
        "post_cancelled": "Post cancelled.",
        "batch_processing": "Batch processing {count} URLs...",
        "stats_duels": "Total duels: {count}",
        "stats_armory": "Armory items: {count}",
        "language": "Language",
    },
    "tr": {
        "app_title": "TweetDuel",
        "app_subtitle": "Yapay Zeka Tartışma Şampiyonu",
        "enter_tweet_url": "Tweet URL'sini girin",
        "scraping": "Tweet ve yanıtlar alınıyor...",
        "scraping_replies": "Yanıtlar alınıyor...",
        "analyzing": "{count} yanıt analiz ediliyor...",
        "analyzing_reply": "Yanıt {current}/{total} analiz ediliyor...",
        "no_replies": "Bu tweet için yanıt bulunamadı.",
        "save_to_armory_prompt": "Yanıtları daha sonra kullanmak için cephaneliğe kaydet?",
        "duel_saved": "Düello kaydedildi: {path}",
        "armory_saved": "Yanıtlar cephaneliğe kaydedildi: {path}",
        "original_tweet": "Orijinal Tweet",
        "reply": "Yanıt",
        "counter_attack": "Karşı Saldırı",
        "instant_mode": "ANINDA DÜELLO MODU",
        "sniper_mode": "KESKİN NİŞANCI MODU",
        "armory_mode": "CEPHANELİK MODU",
        "sniper_watching": "Yeni yanıtlar izleniyor... (Durdurmak için Ctrl+C)",
        "sniper_concept": "Keskin nişancı modu yeni yanıtları izleyip otomatik karşılık üretir.",
        "armory_generating": "Stratejik kullanım için yanıtlar üretilip kaydediliyor...",
        "armory_done": "Tüm yanıtlar stratejik kullanım için cephaneliğe kaydedildi!",
        "ollama_connected": "Ollama bağlı. Kullanılabilir modeller: {models}",
        "ollama_not_running": "Ollama çalışmıyor. Lütfen önce Ollama'yı başlatın:",
        "no_url": "Tweet URL'si verilmedi.",
        "interrupted": "Düello kullanıcı tarafından kesildi.",
        "error_extracting_id": "Tweet ID alınırken hata: {e}",
        "error_scraping": "Tweet alınırken hata: {e}",
        "error_analyzing": "Argümanlar analiz edilirken hata: {e}",
        "error_generating": "Yanıt üretilirken hata: {e}",
        "persona_socrates": "Sokrates",
        "persona_machiavelli": "Machiavelli",
        "persona_chomsky": "Chomsky",
        "persona_tate": "Tate",
        "persona_neutral": "Tarafsız",
        "report_generated": "Rapor oluşturuldu: {path}",
        "thread_prediction": "Konu Tahmini",
        "prediction_title": "Bu konuşmanın nereye gidebileceği",
        "post_approval": "Bu yanıtı Twitter'a gönder?",
        "post_success": "Başarıyla gönderildi.",
        "post_cancelled": "Gönderim iptal edildi.",
        "batch_processing": "{count} URL toplu işleniyor...",
        "stats_duels": "Toplam düello: {count}",
        "stats_armory": "Cephanelik öğesi: {count}",
        "language": "Dil",
    },
    "es": {
        "app_title": "TweetDuel",
        "app_subtitle": "El Campeón de Debate con IA",
        "enter_tweet_url": "Introduce la URL del tweet",
        "scraping": "Obteniendo tweet y respuestas...",
        "scraping_replies": "Obteniendo respuestas...",
        "analyzing": "Analizando {} respuestas...",
        "analyzing_reply": "Analizando respuesta {}/{}...",
        "no_replies": "No se encontraron respuestas para este tweet.",
        "save_to_armory_prompt": "¿Guardar respuestas en el arsenal para usar después?",
        "duel_saved": "Duelo guardado en: {}",
        "armory_saved": "Respuestas guardadas en arsenal: {}",
        "original_tweet": "Tweet Original",
        "reply": "Respuesta",
        "counter_attack": "Contraataque",
        "instant_mode": "MODO DUELO INSTANTÁNEO",
        "sniper_mode": "MODO FRANCOTIRADOR",
        "armory_mode": "MODO ARSENAL",
        "report_generated": "Informe generado: {}",
        "thread_prediction": "Predicción del hilo",
        "prediction_title": "Hacia dónde podría ir esta conversación",
        "post_approval": "¿Publicar esta respuesta en Twitter?",
        "post_success": "Publicado correctamente.",
        "post_cancelled": "Publicación cancelada.",
        "language": "Idioma",
    },
    "de": {
        "app_title": "TweetDuel",
        "app_subtitle": "Der KI-Debatten-Champion",
        "enter_tweet_url": "Tweet-URL eingeben",
        "scraping": "Tweet und Antworten werden geladen...",
        "scraping_replies": "Antworten werden geladen...",
        "analyzing": "{} Antworten werden analysiert...",
        "no_replies": "Keine Antworten zu diesem Tweet gefunden.",
        "save_to_armory_prompt": "Antworten ins Arsenal für späteren Einsatz speichern?",
        "original_tweet": "Original-Tweet",
        "reply": "Antwort",
        "counter_attack": "Gegenangriff",
        "instant_mode": "SOFORT-DUELL-MODUS",
        "report_generated": "Bericht erstellt: {}",
        "thread_prediction": "Thread-Vorhersage",
        "prediction_title": "Wohin dieser Thread gehen könnte",
        "language": "Sprache",
    },
    "fr": {
        "app_title": "TweetDuel",
        "app_subtitle": "Le Champion du Débat IA",
        "enter_tweet_url": "Entrez l'URL du tweet",
        "scraping": "Récupération du tweet et des réponses...",
        "analyzing": "Analyse de {} réponses...",
        "no_replies": "Aucune réponse trouvée pour ce tweet.",
        "save_to_armory_prompt": "Enregistrer les réponses dans l'arsenal ?",
        "original_tweet": "Tweet original",
        "reply": "Réponse",
        "counter_attack": "Contre-attaque",
        "instant_mode": "MODE DUEL INSTANTANÉ",
        "report_generated": "Rapport généré : {}",
        "thread_prediction": "Prédiction du fil",
        "prediction_title": "Où cette conversation pourrait aller",
        "language": "Langue",
    },
}

# Default fallback
DEFAULT_LANG = "en"
SUPPORTED_LANGS = list(TRANSLATIONS.keys())


def t(key: str, lang: Optional[str] = None, **format_args) -> str:
    """Get translated string for key. Use lang or default. Format with format_args."""
    locale = (lang or DEFAULT_LANG).lower()
    if locale not in TRANSLATIONS:
        locale = DEFAULT_LANG
    text = TRANSLATIONS[locale].get(key) or TRANSLATIONS[DEFAULT_LANG].get(key) or key
    if format_args:
        try:
            return text.format(**format_args)
        except (KeyError, ValueError):
            return text
    return text


def set_default_language(lang: str) -> None:
    """Set default language code (e.g. 'tr', 'en')."""
    global DEFAULT_LANG
    if lang and lang.lower() in TRANSLATIONS:
        DEFAULT_LANG = lang.lower()


def get_default_language() -> str:
    return DEFAULT_LANG


def get_supported_languages() -> list:
    return SUPPORTED_LANGS.copy()
