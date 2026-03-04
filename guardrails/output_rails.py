import re

KNOWN_ALLERGENS = {
    "peanuts",
    "nuts",
    "dairy",
    "gluten",
    "soy",
    "egg",
    "fish",
    "shellfish",
    "crustaceans",
    "sesame",
    "mustard",
}

ALLERGEN_SYNONYMS = {
    "dairy": [
        "dairy",
        "butter",
        "cream",
        "cheese",
        "milk",
        "ghee",
        "yogurt",
        "paneer",
        "curd",
    ],
    "gluten": ["gluten", "wheat", "flour", "pasta", "noodle", "bread", "maida", "atta"],
    "nuts": ["nuts", "cashew", "almond", "walnut", "pistachio"],
    "peanuts": ["peanut", "peanuts", "groundnut"],
    "soy": ["soy", "soya", "soy sauce", "tofu"],
    "egg": ["egg", "eggs"],
    "fish": ["fish", "bhetki", "kingfish", "salmon", "tuna"],
    "shellfish": ["shellfish", "prawn", "prawns", "shrimp", "crab", "lobster"],
    "crustaceans": ["crustacean", "crustaceans"],
    "sesame": ["sesame"],
    "mustard": ["mustard"],
}
# Unsafe food patterns
UNSAFE_FOOD_PATTERNS = [
    r"raw chicken",
    r"undercooked (?:chicken|pork|poultry)",
    r"rare (?:chicken|pork)",
    r"do not cook (?:chicken|pork|meat)",
]
# Refusal phrases
REFUSAL_PHRASES = [
    "i cannot",
    "i can't",
    "i'm sorry, i can't",
    "i am not able to",
    "i'm unable to",
    "as an ai",
]


class OutputRail:
    def _check_refusal(self, response: str) -> bool:
        if not response:
            return True
        for phrase in REFUSAL_PHRASES:
            if phrase in response.lower():
                return True
        return False

    def _check_allergen_crossmatch(
        self, response: str, detected_allergens: list[str]
    ) -> list[str]:
        allergens_extended = []
        for allergen in detected_allergens:
            if allergen.lower() in ALLERGEN_SYNONYMS:
                allergens_extended.extend(ALLERGEN_SYNONYMS[allergen.lower()])

        allergens = []
        for allergen in allergens_extended:
            if re.search(
                r"\b" + re.escape(allergen) + r"\b(?!-free)", response.lower()
            ):
                allergens.append(allergen)
        return list(set(allergens))

    def _scan_known_allergens(self, response: str) -> list[str]:
        found = []
        for allergen, synonyms in ALLERGEN_SYNONYMS.items():
            if any(
                re.search(r"\b" + re.escape(syn) + r"\b(?!-free)", response.lower())
                for syn in synonyms
            ):
                found.append(allergen)
        return list(set(found))

    def _check_unsafe_food(self, response: str) -> list:
        found = []
        for pattern in UNSAFE_FOOD_PATTERNS:
            matches = re.findall(pattern, response.lower(), re.IGNORECASE)
            if matches:
                found.extend(matches)
        return found

    def check_output(self, response: str, user_defined_allergen: list[str]) -> dict:
        original_response = response
        result = {
            "response": original_response,
            "warnings": [],
            "is_safe": False,
            "blocked_reason": "",
        }
        if self._check_refusal(original_response):
            result["blocked_reason"] = "Empty Response"
            return result

        result["is_safe"] = True
        warnings = self._check_unsafe_food(original_response)
        if warnings:
            result["warnings"].extend(warnings)

        known_allergens_found = self._scan_known_allergens(original_response)
        if known_allergens_found:
            response_prepender = (
                "WARNING: This recipe contains "
                + ", ".join(known_allergens_found)
                + "\n\n"
            )
            response = response_prepender + response

        allergen_crossmatch = self._check_allergen_crossmatch(
            original_response, user_defined_allergen
        )
        if allergen_crossmatch:
            response_prepender = (
                "ALLERGEN WARNING: This recipe contains "
                + ", ".join(allergen_crossmatch)
                + "\n\n"
            )
            response = response_prepender + response

        result["response"] = response
        return result
