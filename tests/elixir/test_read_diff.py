import unittest

from src.utils.read_diff import InvalidDiffText, ReadDiffElixir


class Test(unittest.TestCase):
    """
    cases it should only detect, on 1 line:
    text after #
    #  text
    text between double quotes = string
    " text "
    text between single quotes = charlist
    ' text '
    text part of another text
    texttext

    Other possible cases:
    Text between double quotes (multiline)
    Text between single quotes (multiline)
    Text between triple double quotes (multiline)
    Text between triple single quotes (multiline)

    text as sigils
    starts with ~ and a letter is between any of the following delimiters
    //, ||, "", '', (), [], {}, <>

    sigils can be used as multiline

    These are too numerous and are complex to find.
    Therefor detection will be done using the tokenizer output.

    """

    def test_text_starts_with_an_expected_chunk_header_java_no_exception_expected(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiffElixir()
        try:
            text = "@@ -1,1 +2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
            read_diff.check_diff_text(text, keywords)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_ends_with_triple_quotes_keyword_should_not_be_excluded(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+Hoi Hallo\"\"\""
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_begins_with_triple_quotes_keyword_should_not_be_excluded(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+\"\"\" Hoi"
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_ends_with_triple_single_quotes_keyword_should_not_be_excluded(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+Hoi = '''"
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_begins_with_triple_single_quotes_keyword_should_not_be_excluded(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+''' |> Hoi"
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_has_no_ending_double_quote_should_not_exclude_keyword(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+\" Hoi"
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_has_no_ending_single_quote_should_not_exclude_keyword(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "+'Hoi"
        (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (newlines[0][0], newlines[0][2]), (2, ["Hoi"]))

    def test_text_has_multiple_keywords_all_should_be_returned(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi/*Hallo\"Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, newlines[0][0], 3)
            unittest.TestCase.assertListEqual(self, newlines[0][2], ["Hoi", "Hallo", "Hoi"])

        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_has_multiple_keywords_before_and_after_a_string_both_should_be_found(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi \"Hallo\"Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, newlines[0][0], 3),
            unittest.TestCase.assertListEqual(self, newlines[0][2], ["Hoi", "Hoi"])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_has_one_valid_keyword_rest_should_not_be_found(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi #Hallo\"Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, newlines[0][0], 3)
            unittest.TestCase.assertListEqual(self, newlines[0][2], ["Hoi"])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_has_no_valid_keyword_non_should_be_found(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+#Hoi #Hallo\"Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, [(newlines[0][0], newlines[0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_contains_part_of_a_multiline_string_all_keywords_should_be_found(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hallo\"Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, newlines[0][0], 3)
            unittest.TestCase.assertListEqual(self, newlines[0][2], ["Hoi", "Hallo", "Hoi"])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_contains_part_of_a_multiline_charlist_all_keywords_should_be_found(self):
        read_diff = ReadDiffElixir()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hallo'Hoi"
            (newlines, old_lines) = read_diff.check_diff_text(text, ["Hoi", "Hallo"])
            unittest.TestCase.assertEqual(self, newlines[0][0], 3)
            unittest.TestCase.assertListEqual(self, newlines[0][2], ["Hoi", "Hallo", "Hoi"])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_elixir(self):
        diff_text = self.read_diff_file(filepath='../data/read_diff_elixir.txt')
        keywords = ["use",  "def", "project", "do", "app", "plug_server", "server", "elixir",
                    "build_embedded", "application", "applications", "cowboy", "plug", "mod", "App", "env",
                    "cowboy_port", "end"]
        read_diff = ReadDiffElixir()
        (new_lines, old_lines) = read_diff.check_diff_text(diff_text, keywords)

        expected_nl = [(5, '[app: :server,', ['app', 'server']),
                       (17, '[applications: [:cowboy, :plug],', ['applications', 'cowboy', 'plug']),
                       (18, 'mod: {App, []},', ['mod', 'App']),
                       (19, 'env: [cowboy_port: 9292]]', ['env', 'cowboy_port'])]
        expected_ol = [(5, '[app: :plug_server,', ['app', 'plug_server']),
                       (17, '[applications: [:cowboy, :plug]]', ['applications', 'cowboy', 'plug'])]
        self.assertEqual(new_lines, expected_nl)
        self.assertEqual(old_lines, expected_ol)

    @staticmethod
    def read_diff_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk
