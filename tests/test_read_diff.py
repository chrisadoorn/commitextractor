import unittest
from src.utils.read_diff import ReadDiff, InvalidDiffText


class Test(unittest.TestCase):
    # tests of de juiste combinatie van hash methode en seed gebruikt wordt
    def test_java_text_geen_keywords(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_java_zonder_keywords.txt')
        read_diff = ReadDiff(language="JAVA")
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)

        unittest.TestCase.assertEqual(self, 10, len(new_lines), 'onjuist aantal nieuwe regels gevonden')
        unittest.TestCase.assertEqual(self, 5, len(old_lines), 'onjuist aantal gewijzigde regels gevonden')

        for (regelnr, line, keywords) in new_lines:
            unittest.TestCase.assertTrue(len(keywords) == 0,
                                         'onverwacht keywords {0} gevonden in nieuwe regel {1}'.format(str(keywords),
                                                                                                       str(regelnr)))

        for (regelnr, line, keywords) in old_lines:
            unittest.TestCase.assertTrue(len(keywords) == 0,
                                         'onverwacht keywords {0} gevonden in oude regel {1}'.format(str(keywords),
                                                                                                     str(regelnr)))

    def test_java_text_met_keywords(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_java_met_keywords.txt')
        keywords = ["Thread"]
        read_diff = ReadDiff("JAVA", keywords)
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)
        unittest.TestCase.assertEqual(self, 11, len(new_lines), 'onjuist aantal nieuwe regels gevonden')
        unittest.TestCase.assertEqual(self, 6, len(old_lines), 'onjuist aantal gewijzigde regels gevonden')
        expected = [(23, "import Thread", ['Thread']),
                    (40, "/* FIXME Intentionally verbose: always log this until we've", []),
                    (41, "fully debugged the app failing to start up */", []),
                    (42, "Log.v(\"AlarmReceiver.onReceive() id \" + id + \" setFor \" + setFor +", []),
                    (43, "\" now Thread\" + now);", []), (51, "/* wake device */", []),
                    (54, "/* start audio/vibe */", []), (55, "AlarmKlaxon klaxon = AlarmKlaxon.getInstance();", []),
                    (56, "Thread thread = new Thread();", ['Thread']), (58, "/* launch Thread */", []),
                    (59, "Intent fireAlarm = new Intent(context, AlarmAlert.class);", [])]

        for (regelnr, line, keywords) in new_lines:
            unittest.TestCase.assertEqual(self, expected.pop(0), (regelnr, line, keywords),
                                          'onjuiste regel {0} gevonden'.format(str(regelnr)))

        expected2 = [(23, "import android.os.Handler;", []), (24, "import android.os.PowerManager;", []),
                     (25, "import android.os.SystemClock;", []), (26, "import Thread", ['Thread']),
                     (49, "Thread thread = new Thread();", ['Thread']),
                     (52, "Intent fireAlarm = new Intent(context, AlarmAlert.class);", [])]

        for (regelnr, line, keywords) in old_lines:
            unittest.TestCase.assertEqual(self, expected2.pop(0), (regelnr, line, keywords),
                                          'onjuiste regel {0} gevonden'.format(str(regelnr)))

    def test_text_starts_with_not_an_expected_chunk_header(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiff("JAVA", keywords)
        text = "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@aa@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@1,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@1,1 2,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@ 1,1 2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@ -1,1 2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@ 1,1 -2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@ +1,1 -2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)
        text = "@@+1,1-2,1@@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
        self.assertRaises(InvalidDiffText, read_diff.read_diff_text, text)

    def test_text_starts_with_an_expected_chunk_header(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiff("JAVA", keywords)
        try:
            text = "@@ -1,1 +2,1 @@Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi"
            x = read_diff.read_diff_text(text)
            print(x)
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    def test_elixir(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_elixir.txt')
        keywords = ["use", "Mix.Project", "def", "project", "do", "app", "plug_server", "server", "elixir",
                    "build_embedded", "application", "applications", "cowboy", "plug", "mod", "App", "env",
                    "cowboy_port", "end"]
        read_diff = ReadDiff("ELIXIR", keywords)
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)
        x = new_lines
        y = old_lines
        expected_nl = [(5, '[app: :server,', ['server']),
                       (17, '[applications: [:cowboy, :plug],', []),
                       (18, 'mod: {App, []},', ['mod', 'App']),
                       (19, 'env: [cowboy_port: 9292]]', ['env', 'cowboy_port'])]
        expected_ol = [(5, '[app: :plug_server,', ['app', 'plug_server']),
                       (17, '[applications: [:cowboy, :plug]]', ['applications', 'cowboy', 'plug'])]
        self.assertEqual(x, expected_nl)
        self.assertEqual(y, expected_ol)

    def test_text_starts_with_an_expected_chunk_header_and_has_keywords(self):
        keywords = ["Hoi", "Hallo", "Doei", "Dag_Hoi", "dag_Hoi"]
        read_diff = ReadDiff("JAVA", keywords)
        textheader = "@@ -1,1 +2,1 @@" + "\n"

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ Hoi \"//\" Hallo Hoi"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi', 'Hallo'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+   Hoi Hallo Hoi" + "\n"
            text = text + "- Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, 2, len(x))
            unittest.TestCase.assertEqual(self, [(3, ['Hoi', 'Hallo'])], [(x[0][0][0], x[0][0][2])])
            unittest.TestCase.assertEqual(self, [(2, ['Hoi', 'dag_Hoi'])], [(x[1][0][0], x[1][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ //Hoi Hallo Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, [])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ Hoi //Hallo Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")
        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ Hoi /* Hallo Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+Hoi \"/* Hallo Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ hoi \"/* Hallo Hoi" + "\n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, [])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ Anders bla = 12, c=2; string=\"Hallo Hoi\",  Hallo \"Hallo Doeidag\"_Hoi Hoi.dag_Hoi \n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hallo', 'Hoi', 'dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+ Anders bla = 12, c=2; string=\"Hallo Hoi\",  Hallo \"Hallo Doeidag\"_Hoi*/ Hoi.dag_Hoi \n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hoi', 'dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

        try:
            text = textheader + "Hoi Hallo Doeidag_Hoi Hoi.dag_Hoi" + "\n"
            text = text + "+Anders bla = 12, c=2; string=\"Hallo Hoi\",  " \
                          "Hallo(\"Hallo Doeidag\"_Hoi\"*/\" Hoi.dag_Hoi \n"
            x = read_diff.read_diff_text(text)
            unittest.TestCase.assertEqual(self, [(3, ['Hallo', 'Hoi', 'dag_Hoi'])], [(x[0][0][0], x[0][0][2])])
        except InvalidDiffText:
            self.fail("Unexpected InvalidDiffText exception")

    @staticmethod
    def read_diff_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk
