import unittest
from Assignments.A2.scrabble_score import ScrabbleScore

class ScrabbleScoreTestCase(unittest.TestCase):
    program = ScrabbleScore()

    def test_initialisation(self):
        self.assertEqual(
            [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10],
            self.program.score_table
        )

    def test_add_up(self):
        self.assertEqual(
            14, self.program.add_up("cabbage")
        )

    def test_letter_values(self):
        self.assertEqual(
            self.program.get_value("A"),
            self.program.get_value("a")
        )
        self.assertEqual(
            self.program.get_value("D"),
            self.program.get_value("d")
        )
        self.assertEqual(
            self.program.get_value("H"),
            self.program.get_value("h")
        )
        self.assertEqual(
            self.program.get_value("K"),
            self.program.get_value("k")
        )
        self.assertEqual(
            self.program.get_value("Q"),
            self.program.get_value("q")
        )

    def test_input_validation(self):
        with self.assertRaises(RuntimeError):
            self.program.validate_input("")

        self.assertEqual(
            3,
            self.program.validate_input("abc")
        )
    def test_word_validation(self):
        self.assertTrue(True, self.program.validate_word("apple"))
        self.assertFalse(False, self.program.validate_word("boook"))


if __name__ == "__main__":
    unittest.main()
