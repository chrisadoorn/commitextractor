import unittest
from src.utils.read_diff import ReadDiff, Language


class Test(unittest.TestCase):
    # tests of de juiste combinatie van hash methode en seed gebruikt wordt
    def test_java_text_geen_keywords(self):
        diff_text = self.read_diff_file(filepath='data/read_diff_java_zonder_keywords.txt')
        read_diff = ReadDiff(language=Language.JAVA)
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
        read_diff = ReadDiff(language=Language.JAVA)
        (new_lines, old_lines) = read_diff.read_diff_text(diff_text)

        unittest.TestCase.assertEqual(self, 11, len(new_lines), 'onjuist aantal nieuwe regels gevonden')
        unittest.TestCase.assertEqual(self, 6, len(old_lines), 'onjuist aantal gewijzigde regels gevonden')
        expected = {
            "import Thread": "['Thread']",
            "/* FIXME Intentionally verbose: always log this until we've": "[]",
            "fully debugged the app failing to start up */": "[]",
            "\" now Thread\" + now);": "[]",
            "/* wake device */": "[]",
            "/* start audio/vibe */": "[]",
            "AlarmKlaxon klaxon = AlarmKlaxon.getInstance();": "[]",
            "Thread thread = new Thread();": "['Thread']",
            "/* launch Thread */": "['Thread']",
            "Intent fireAlarm = new Intent(context, AlarmAlert.class);": "[]",
            "Log.v(\"AlarmReceiver.onReceive() id \" + id + \" setFor \" + setFor +": "[]"
        }
        for (regelnr, line, keywords) in new_lines:
            #print(line)
            #print(str(keywords))
            unittest.TestCase.assertEqual(self, expected.get(line),str(keywords),
                                         'onverwacht keywords {0} gevonden in nieuwe regel {1}'.format(str(keywords),
                                                                                                       str(regelnr)))

        expected = {
            "import android.os.Handler;": "[]",
            "import android.os.PowerManager;": "[]",
            "import android.os.SystemClock;": "[]",
            "import Thread": "['Thread']",
            "Thread thread = new Thread();": "['Thread']",
            "Intent fireAlarm = new Intent(context, AlarmAlert.class);": "[]"
        }
        for (regelnr, line, keywords) in old_lines:
            #print(line)
            #print(str(keywords))
            unittest.TestCase.assertEqual(self, expected.get(line),str(keywords),
                                         'onverwacht keywords {0} gevonden in oude regel {1}'.format(str(keywords),
                                                                                                     str(regelnr)))

    @staticmethod
    def read_diff_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk
