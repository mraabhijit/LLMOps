import re
from dataclasses import dataclass, field

INGREDIENT_SET = {
    # spices "whole and ground"
    "turmeric powder",
    "haldi",
    "cumin seeds",
    "heera",
    "cumin powder",
    "jeera powder",
    "coriander powder",
    "dhaniya powder",
    "red chili powder",
    "lal mirch",
    "garam masala",
    "mustard seeds",
    "rai",
    "sarson",
    "asafoetida",
    "hing",
    "green cardamom",
    "hari elaichi",
    "black cardamom",
    "badi elaichi",
    "cinnamon stick",
    "dalchini",
    "cloves",
    "laung",
    "fenugreek seeds",
    "methi dana",
    "fennel seeds",
    "saunf",
    "star anise",
    "chakra phool",
    "mace",
    "javitri",
    "nutmeg",
    "jaiphal",
    "indian bay leaf",
    "tej patta",
    "carom seeds",
    "ajwain",
    "nigella seeds",
    "kalonji",
    "dry mango powder",
    "amchur",
    "dried red chilies",
    "black pepper",
    "kali mirch",
    "dried pomegranate seeds",
    "anardana",
    "kashmiri chili powder",
    # herbs and fresh produce
    "ginger",
    "adrak",
    "garlic",
    "lahsun",
    "green chilies",
    "fresh coriander leaves",
    "cilantro",
    "dhaniya",
    "curry leaves",
    "kadi patta",
    "fresh mint leaves",
    "pudina",
    "dried fenugreek leaves",
    "kasuri methi",
    "red onions",
    "tomatoes",
    "potatoes",
    "aloo",
    # lentils, grains, and flours
    "basmati rice",
    "wheat flour",
    "atta",
    "toor dal",
    "split pigeon peas",
    "masoor dal",
    "red lentils",
    "urad dal",
    "black gram",
    "moong dal",
    "green gram",
    "yellow gram",
    "chickpea flour",
    "besan",
    "chickpeas",
    "chole",
    "garbanzo",
    "kidney beans",
    "rajma",
    "semolina",
    "sooji",
    "rava",
    # oils, dairy, and others
    "ghee",
    "clarified butter",
    "mustard oil",
    "yogurt",
    "dahi",
    "coconut",
    "tamarind paste",
}

JAILBREAK_PATTERNS = {
    "ignore all instructions",
    "ignore previous",
    "you are now",
    "pretend to be",
    "system prompt",
    "forget everything",
    "disregard",
    "act as if",
}


ALLERGY_DECLARATION_PATTERNS = [
    r"allergic to ([\w\s]+)",
    r"(\w+) allergy",
    r"(\w+) intolerant",
    r"no ([\w\s]+)",
    r"can'?t (?:eat|have) ([\w\s]+)",
    r"avoid ([\w\s]+)",
]


NORMALIZE_MAP = {
    "chicken breasts": "chicken breast",
    "tomatoes": "tomato",
    "onions": "onion",
    "potatoes": "potato",
    "lemons": "lemon",
    "eggs": "egg",
    "mushrooms": "mushroom",
    "carrots": "carrot",
    "peppers": "pepper",
    "noodles": "noodle",
    "prawns": "prawn",
    "peanuts": "peanut",
}


class InputException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


@dataclass
class InputRailResponse:
    sanitized_input: str = ""
    is_valid: bool = False
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    detected_allergens: list[str] = field(default_factory=list)


class InputRail:
    def _check_gibberish(self, query: str) -> str | None:
        allergies = self._detect_allergies(query)
        valid_ingredients = self._get_valid_ingredients(query)
        if not valid_ingredients and not allergies:
            return "No Valid Ingredients found."
        return None

    def _detect_allergies(self, query: str) -> list[str]:
        found = []
        for pattern in ALLERGY_DECLARATION_PATTERNS:
            matches = re.findall(pattern, query, re.IGNORECASE)
            found.extend(matches)
        return list(set(found))

    def _get_valid_ingredients(self, query: str) -> bool:
        return any(ing in query.lower() for ing in INGREDIENT_SET)

    def _check_jailbreak(self, query: str) -> str | None:
        query = query.lower()
        if any(p in query for p in JAILBREAK_PATTERNS):
            return "Potential Prompt injection detected."
        return None

    def _normalize(self, query: str) -> str:
        for k, v in NORMALIZE_MAP.items():
            query = query.replace(k, v)
        return query

    def check_input(self, query: str) -> InputRailResponse:
        result = InputRailResponse()

        gibberish = self._check_gibberish(query)
        if gibberish:
            result.violations.append(gibberish)
        jailbreak_attempt = self._check_jailbreak(query)
        if jailbreak_attempt:
            result.violations.append(jailbreak_attempt)
        if gibberish or jailbreak_attempt:
            return result

        result.is_valid = True

        normalized_query = self._normalize(query)
        result.sanitized_input = normalized_query

        allergens = self._detect_allergies(query)
        result.detected_allergens.extend(allergens)

        return result
