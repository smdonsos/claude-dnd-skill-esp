"""
test_lookup_suggest.py — near-miss "did you mean?" suggestions for lookup.py.

Runs against the bundled dnd5e_srd.json (no fixtures needed): a mistyped rule,
condition, spell, or monster should surface the closest real name instead of
dead-ending.

Run from repo root:
    python3 -m unittest tests.test_lookup_suggest -v
"""
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "dnd" if (REPO / "skills" / "dnd").is_dir() else REPO
sys.path.insert(0, str(SKILL / "scripts"))

import lookup  # noqa: E402


def _names(hints):
    return [nm.lower() for nm, _cat in hints]


class SuggestTests(unittest.TestCase):

    def test_condition_typo(self):
        # "conditions" is translated (Fase 3/CLA-8) — the English typo must
        # still resolve via the untranslated `index` slug, surfaced under
        # the (Spanish) display name "envenenado".
        hints = lookup.suggest("poisonned", category="condition")
        self.assertIn("envenenado", _names(hints))

    def test_spell_typo(self):
        # "spells" is translated (Fase 3/CLA-8) — the English typo resolves
        # under the Spanish display name via the untranslated `index`.
        hints = lookup.suggest("fireballl", category="spell")
        self.assertIn("bola de fuego", _names(hints))

    def test_monster_typo(self):
        hints = lookup.suggest("gobblin", category="monster")
        self.assertIn("goblin", _names(hints))

    def test_feature_typo(self):
        # "features" is translated (Fase 3/CLA-8) — same reasoning as
        # test_spell_typo above.
        hints = lookup.suggest("cunnning action", category="feature")
        self.assertIn("acción astuta", _names(hints))

    def test_cross_category_typo(self):
        # No category given — should still find the near-miss across
        # categories. "conditions" is translated (Fase 3/CLA-8), so the
        # English typo resolves under the Spanish display name.
        hints = lookup.suggest("poisonned")
        self.assertIn("envenenado", _names(hints))

    def test_respects_result_cap(self):
        hints = lookup.suggest("fireballl", category="spell", n=2)
        self.assertLessEqual(len(hints), 2)

    def test_exact_name_still_offered_when_query_is_garbage(self):
        # A totally unrelated query returns few/no suggestions, never raises.
        hints = lookup.suggest("zzzxqqywv", category="condition")
        self.assertIsInstance(hints, list)

    def test_category_scoping(self):
        # A condition typo scoped to spells must not return the condition.
        hints = lookup.suggest("poisonned", category="spell")
        self.assertNotIn("poisoned", _names(hints))

    def test_returns_name_category_tuples(self):
        hints = lookup.suggest("fireballl", category="spell")
        self.assertTrue(hints)
        nm, cat = hints[0]
        self.assertIsInstance(nm, str)
        self.assertEqual(cat, "spells")


class NormAccentTests(unittest.TestCase):
    """_norm() must fold Spanish accents/ñ onto their unaccented form (CLA-25/CLA-8)
    instead of the old `[^a-z0-9]+` regex silently dropping the accented letter."""

    def test_accented_vowels_fold_to_unaccented(self):
        self.assertEqual(lookup._norm("salvación"), lookup._norm("salvacion"))
        self.assertEqual(lookup._norm("café"), lookup._norm("cafe"))

    def test_ene_folds_to_n(self):
        self.assertEqual(lookup._norm("ñoño"), "nono")

    def test_accented_multiword_query_matches_unaccented(self):
        self.assertEqual(
            lookup._norm("Bola de Fuégo"), lookup._norm("bola de fuego")
        )

    def test_english_names_unaffected(self):
        self.assertEqual(lookup._norm("Healing Word"), "healing-word")
        self.assertEqual(lookup._norm("Fireball"), "fireball")

    def test_wikidot_url_slug_uses_same_folding(self):
        url_accented = lookup.wikidot_url("Poción", category="equipment")
        url_plain = lookup.wikidot_url("Pocion", category="equipment")
        self.assertEqual(url_accented, url_plain)


if __name__ == "__main__":
    unittest.main()
