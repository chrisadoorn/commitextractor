import unittest

from src.utils.read_diff import InvalidDiffText, ReadDiffJava, ReadDiffElixir


class Test(unittest.TestCase):

    def test_java_text_geen_keywords(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_java_zonder_keywords.txt')
        read_diff = ReadDiffJava()
        (new_lines, old_lines) = read_diff.check_diff_text(diff_text, ['Thread'])

        unittest.TestCase.assertEqual(self, 10, len(new_lines), 'onjuist aantal nieuwe regels gevonden')
        unittest.TestCase.assertEqual(self, 5, len(old_lines), 'onjuist aantal gewijzigde regels gevonden')

        for (regelnr, line, keywords) in new_lines:
            unittest.TestCase.assertTrue(keywords,
                                         'onverwacht keywords {0} gevonden in nieuwe regel {1}'.format(str(keywords),
                                                                                                       str(regelnr)))

        for (regelnr, line, keywords) in old_lines:
            unittest.TestCase.assertTrue(keywords,
                                         'onverwacht keywords {0} gevonden in oude regel {1}'.format(str(keywords),
                                                                                                     str(regelnr)))

    def test_java_text_met_keywords(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_java_met_keywords.txt')
        keywords = ["Thread"]
        read_diff = ReadDiffJava()
        (new_lines, old_lines) = read_diff.check_diff_text(diff_text, keywords)
        unittest.TestCase.assertEqual(self, 11, len(new_lines), 'onjuist aantal nieuwe regels gevonden')
        unittest.TestCase.assertEqual(self, 6, len(old_lines), 'onjuist aantal gewijzigde regels gevonden')
        expected = [(23, "import Thread", ['Thread']),
                    (40, "/* FIXME Intentionally verbose: always log this until we've", []),
                    (41, "fully debugged the app failing to start up */", []),
                    (42, "Log.v(\"AlarmReceiver.onReceive() id \" + id + \" setFor \" + setFor +", []),
                    (43, "\" now Thread\" + now);", []), (51, "/* wake device */", []),
                    (54, "/* start audio/vibe */", []), (55, "AlarmKlaxon klaxon = AlarmKlaxon.getInstance();", []),
                    (56, "Thread thread = new Thread();", ['Thread', 'Thread']), (58, "/* launch Thread */", []),
                    (59, "Intent fireAlarm = new Intent(context, AlarmAlert.class);", [])]

        for (regelnr, line, keywords) in new_lines:
            unittest.TestCase.assertEqual(self, expected.pop(0), (regelnr, line, keywords),
                                          'onjuiste regel {0} gevonden'.format(str(regelnr)))

        expected2 = [(23, "import android.os.Handler;", []), (24, "import android.os.PowerManager;", []),
                     (25, "import android.os.SystemClock;", []), (26, "import Thread", ['Thread']),
                     (49, "Thread thread = new Thread();", ['Thread', 'Thread']),
                     (52, "Intent fireAlarm = new Intent(context, AlarmAlert.class);", [])]

        for (regelnr, line, keywords) in old_lines:
            unittest.TestCase.assertEqual(self, expected2.pop(0), (regelnr, line, keywords),
                                          'onjuiste regel {0} gevonden'.format(str(regelnr)))

    def test_text_starts_with_not_an_expected_chunk_header(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiffJava()
        text = "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@aa@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@1,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@1,1 2,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@ 1,1 2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@ -1,1 2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@ 1,1 -2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@ +1,1 -2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)
        text = "@@+1,1-2,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.check_diff_text, text, keywords)

    def test_text_starts_with_an_expected_chunk_header(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiffJava()
        try:
            text = "@@ -1,1 +2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
            x = read_diff.check_diff_text(text, keywords)
            print(x)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_starts_with_an_expected_chunk_header_netto_added_keyword(self):
        read_diff = ReadDiffJava()
        textheader = "@@ -1,1 +1,1 @@" + "\n"
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi #Hallo\"Hoi" + "\n"
            text = text + "-Hoi #Hallo\"Hoi" + "\n"
            nl, ol = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(2, "Hoi #Hallo\"Hoi", ['Hoi'])], nl)
            unittest.TestCase.assertEqual(self, [(2, "Hoi #Hallo\"Hoi", ['Hoi'])], ol)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hoi #Hallo\"Hoi Hoi Hoi" + "\n"
            text = text + "-Hoi #Hallo\"Hoi" + "\n"
            nl, ol = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(2, "Hoi Hoi #Hallo\"Hoi Hoi Hoi", ["Hoi", "Hoi"])], nl)
            unittest.TestCase.assertEqual(self, [(2, "Hoi #Hallo\"Hoi", ["Hoi"])], ol)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hoi #Hallo\"Hoi Hoi Hoi" + "\n"
            text = text + "-Test 123" + "\n"
            text = text + "-Hoi #Hallo\"Hoi" + "\n"
            nl, ol = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(2, "Hoi Hoi #Hallo\"Hoi Hoi Hoi", ["Hoi", "Hoi"])], nl)
            unittest.TestCase.assertEqual(self, [(2, "Test 123", []), (3, "Hoi #Hallo\"Hoi", ["Hoi"])], ol)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_starts_with_an_expected_chunk_header_and_has_keywords(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi", "Hoi.dag_Hoi"]
        read_diff = ReadDiffJava()
        textheader = "@@ -1,1 +2,1 @@" + "\n"

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ HoiHoi \"//\" Hallo Hoi"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hallo', 'Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+   Hoi Hallo Hoi" + "\n"
            text = text + "- Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, 2, len(x))
            unittest.TestCase.assertEqual(self, [(3, ['Hoi', 'Hallo', 'Hoi'])], [(x[0][0][0], x[0][0][2])])
            unittest.TestCase.assertEqual(self, [(2, ["Hoi.dag_Hoi"])], [(x[1][0][0], x[1][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ //Hoi Hallo Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, [])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi //Hallo Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")
        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi /* Hallo Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi \"/* Hallo Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ hoi \"/* Hallo Hoi" + "\n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, [])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Anders bla = 12, c=2; string=\"Hallo Hoi\",  Hallo \"Hallo Doeidag\"_Hoi Hoi.dag_Hoi \n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hallo', 'Hoi.dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Anders bla = 12, c=2; string=\"Hallo Hoi\",  Hallo \"Hallo Doeidag\"_Hoi*/ Hoi.dag_Hoi \n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi.dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Anders bla = 12, c=2; string=\"Hallo Hoi\",  " \
                          "Hallo(\"Hallo Doeidag\"_Hoi\"*/\" Hoi.dag_Hoi \n"
            x = read_diff.check_diff_text(text, keywords)
            unittest.TestCase.assertEqual(self, [(3, ['Hallo', 'Hoi.dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_text_has_escaped_quotes(self):
        read_diff = ReadDiffJava()
        textheader = "@@ -1,1 +2,1 @@" + "\n"
        text = textheader + "Same line that was not changed\n"
        text = text + "+Hoi \"Hallo \\\" Hoi\""
        (x, y) = read_diff.check_diff_text(text, ["Hoi"])
        unittest.TestCase.assertEqual(self, (x[0][0], x[0][2]), (3, ["Hoi"]))

    def test_text_starts_with_an_expected_chunk_header_and_has_keywords_single_word_java(self):
        read_diff = ReadDiffJava()
        textheader = "@@ -1,1 +2,1 @@" + "\n"

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hallo Hoi*/"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi Hallo Hoi*/HoiHoi Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+HoiHalloHoi HoiHoiHoiHoiHoiHoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi \"//\" HalloHoi Hallo Hoi "
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi", "Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hallo"])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi Hallo Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi", "Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hallo"])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi \"Hallo Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi\"Hallo\"Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi", "Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+ Hoi//Hallo\"Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+// Hoi//Hallo\"Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Same line that was not changed\n"
            text = text + "+Hoi/*Hallo\"Hoi"
            x = read_diff.check_diff_text(text, ["Hoi"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, ["Hoi"])])
            x = read_diff.check_diff_text(text, ["Hallo"])
            unittest.TestCase.assertEqual(self, [(x[0][0][0], x[0][0][2])], [(3, [])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")
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
        diff_text = self.read_diff_file(filepath='data/read_diff_elixir.txt')
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
