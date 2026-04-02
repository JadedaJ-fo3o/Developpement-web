import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

from services.tvmaze import search_shows

#limitation du nombre de recommandations proposées
MAX_RECOMMENDATIONS = 5


def build_user_preferences(records):
    records = records or []
    lines = []

    for r in records:
        if not isinstance(r, dict):
            continue
        name = r.get("name_serie")
        if not name:
            continue
        score = r.get("rating_value")
        try:
            score = int(score)
        except (TypeError, ValueError):
            continue

        if score < 1 or score > 5: #les notes bizzares
            continue

        lines.append(f"- {name}: {score}/5")

    return "\n".join(lines)

##cette partie doit être corrigée pour mieux refléter
def detect_intent(question):
    #如果用户问电影，返回movie并引出警告
    # Si l'utilisateur demande un film, on arrete ici (TVMaze = series TV uniquement).
    text = (question or "").lower()
    movie_words = ["电影", "電影", "movie", "film", "films", "cinema", "cinéma"]
    for word in movie_words:
        if word in text:
            return "movie"
    return "series"


def build_prompt(pref_text, question):
    if not pref_text:
        pref_text = "Aucune préférence enregistrée."
    question = (question or "").strip() or "Propose-moi des séries populaires."

    return (
        "Donne au maximum 5 recommendations de series TV.\n"
        "Format obligatoire: une ligne par recommandation, comme ceci:\n"
        "Nom de la serie - raison courte\n"
        "Les notes utilisateur sont sur 5: 1 = n'aime pas, 5 = aime beaucoup.\n\n"
        f"Historique et notes utilisateur:\n{pref_text}\n"
        f"Question: {question}\n"
    )

#résultats
def parse_lines(raw_text):
    candidates = []
    if not raw_text:
        return candidates

    lines = raw_text.splitlines()
    for line in lines:
        text = line.strip().lstrip("-•0123456789. ").strip() #clean 
        if not text:
            continue
        if " - " in text:
            left, right = text.split(" - ", 1)
            title = left.strip()
            reason = right.strip()
        else:
            title = text.strip()
            reason = "Recommandé selon votre demande."
        if title:
            candidates.append({"title": title, "reason": reason})
        if len(candidates) >= MAX_RECOMMENDATIONS:
            break

    return candidates

#definir les outputs
def build_items(candidates):
    items = []
    for c in candidates:
        title = c.get("title", "").strip()
        reason = c.get("reason", "").strip() or "Recommandé selon votre demande."
        if not title:
            continue
        
        #chercher et sélectionner
        found = search_shows(title)
        show = pick_show(title, found)
        if not show:
            continue

        items.append(
            {
                "id": show.get("id"), #pour le lien vers la page de détail
                "name": show.get("name") or title,
                "image": show.get("image"),
                "rating": show.get("rating"),
                "url": show.get("url"),
                "genres": show.get("genres", []),
                "reason": reason,
            }
        )

        if len(items) >= MAX_RECOMMENDATIONS:
            break

    return items


def pick_show(query, found):
    if not found:
        return None
    query_lower = query.lower().strip()
    for show in found:
        if (show.get("name") or "").lower().strip() == query_lower:
            return show
    return found[0]


def error_message(raw_text):
    if raw_text.startswith("Erreur Gemini"):
        return raw_text
    if raw_text.startswith("Clé API"):
        return raw_text
    if "manquante" in raw_text:
        return raw_text
    return ""


class GeminiSDK:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY") #.env
        model_name = os.getenv("GEMINI_MODEL")

        if not model_name:
            model_name = "gemini-flash-latest"

        if not api_key:
            self.enabled = False
            self.model = None
            return

        #si'il y a une clé, on active le service et on crée le modèle
        self.enabled = True
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)#création du modèle

    def generate(self, prompt):
        if not self.enabled or self.model is None:
            return "Le service IA n'est pas configuré ou GEMINI_API_KEY manquante."

        for attempt in range(3): #essaie 3 fois en cas d'erreur(timeout...
            try:
                t0 = time.time()
                response = self.model.generate_content(prompt)
                t1 = time.time()
                print(f"[TIME] Gemini generate_content: {t1 - t0:.3f}s")
                return response.text
            except Exception as exc:
                print(f"[WARN] appel Gemini échoué ({attempt + 1}/3) : {exc}")
                if attempt < 2:
                    # Attend un peu puis reessaie.
                    time.sleep(2)
                    continue
                return f"Erreur Gemini: {exc}"

        return "Service temporairement indisponible, veuillez réessayer plus tard."


sdk = GeminiSDK()


def recommend_from_records(records, user_question):
    intent = detect_intent(user_question)
    if intent == "movie":
        return {
            "items": [],
            "message": "Actuellement, la recommandation est basée sur TVMaze (séries TV uniquement).",
        }

    pref_text = build_user_preferences(records)
    prompt = build_prompt(pref_text, user_question)
    raw_text = sdk.generate(prompt)

    error_message_text = error_message(raw_text)
    if error_message_text:
        return {"items": [], "message": error_message_text}

    candidates = parse_lines(raw_text)
    items = build_items(candidates)

    if not items:
        return {
            "items": [],
            "message": "Aucune série TV trouvée dans TVMaze pour cette demande.",
        }

    message = ""
    if len(items) < 3:
        message = "Peu de résultats trouvés dans TVMaze. Essayez un style ou un genre plus précis."

    return {"items": items, "message": message}
