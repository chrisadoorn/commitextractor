import unittest

from src.elixir_parsing import last_check


class Test(unittest.TestCase):
    token_list = [
        '{:identifier, {1, 1, ~c"defmodule"}, :defmodule}',
        '{:kw_identifier, {97, 53, ~c"else"}, :else}',
        '{:kw_identifier_unsafe, {44, 17, nil}, [{{44, 18, nil}, {44, 24, nil}, [{:identifier, {44, 20, ~c"type"}, :type}]}]}',
        '{:bracket_identifier, {164, 12, ~c"params"}}',
        '{:paren_identifier, {84, 9, ~c"choose"}, :choose}',
        '{:do_identifier, {66, 5, ~c"cond"}, :cond}',
        '{:block_identifier, {98, 5, nil}, :rescue}',
        '{:op_identifier, {128, 5, ~c"assert"}, :assert}',
        '{:fn, {89, 26, nil}}', '{:end, {103, 9, nil}}',
        '{:alias, {89, 10, ~c"Enum"}, :Enum}',
        '{:atom, {131, 23, ~c"done"}}',
        '{:atom_quoted, {746, 7, nil}, :"$.xgafv"}',
        '{:atom_unsafe, {18, 39, nil}, [{{18, 41, nil}, {18, 52, nil}, [{:identifier, {18, 43, ~c""func_name""}, :func_name}]}]}',
        '{:bin_string, {128, 35, nil}, [" "]}',
        '{:list_string, {16, 20, nil}, [""Web DSL""]}',
        '{:sigil, {56, 38, nil}, :sigil_N, ["2016-01-01 00:00:00"], [], nil, "["}',
        '{:bin_heredoc, {37, 8, nil}, 2, ["Same as `string/1` but it will continue to \\"prompt\\" the user in case of an empty response.\\n"]}',
        '{:list_heredoc, {158, 5, nil}, 4, ["case true do\\n  true && true -> true\\nend\\n"]}',
        '{:comp_op, {100, 44, nil}, :==}',
        '{:at_op, {120, 3, nil}, :@}',
        '{:unary_op, {167, 8, nil}, :!}',
        '{:and_op, {254, 33, nil}, :and}',
        '{:or_op, {176, 26, nil}, :||}',
        '{:arrow_op, {287, 5, 1}, :|>}',
        '{:match_op, {96, 9, nil}, :=}',
        '{:in_op, {94, 12, nil}, :in}',
        '{:in_match_op, {121, 29, nil}, :\\\\}',
        '{:type_op, {84, 33, nil}, :"::"}',
        '{:dual_op, {90, 24, nil}, :+}',
        '{:mult_op, {232, 25, nil}, :*}',
        '{:power_op, {205, 8, nil}, :**}',
        '{:concat_op, {128, 32, nil}, :<>}',
        '{:range_op, {45, 35, nil}, :..}',
        '{:xor_op, {93, 40, nil}, :""^^^""}',
        '{:pipe_op, {91, 11, nil}, :|}',
        '{:stab_op, {33, 11, nil}, :->}',
        '{:when_op, {83, 32, nil}, :when}',
        '{:capture_int, {100, 41, nil}, :&}',
        '{:capture_op, {100, 39, nil}, :&}',
        '{:assoc_op, {25, 62, nil}, :""=>""}',
        '{:rel_op, {97, 12, nil}, :>}',
        '{:ternary_op, {278, 63, nil}, :""//""}',
        '{:dot_call_op, {20, 22, nil}, :.}',
        '{true, {121, 32, nil}}',
        '{false, {134, 7, nil}}',
        '{:do, {1, 20, nil}}',
        '{:eol, {12, 6, 2}}',
        '{:";", {85, 20, 0}}',
        '{:",", {85, 20, 0}}',
        '{:., {120, 54, nil}}',
        '{:"(", {64, 20, nil}}',
        '{:")", {62, 23, nil}}',
        '{:"[", {39, 11, nil}}',
        '{:"]", {19, 5, 1}}',
        '{:"{", {89, 29, nil}}',
        '{:"}", {89, 34, nil}}',
        '{:""<<"", {14, 23, nil}}',
        '{:"">>"", {4, 36, nil}}',
        '{:%{}, {41, 5, nil}}',
        '{:%, {30, 12, nil}}',
        '{:int, {101, 19, 1}, ~c"1"}',
        '{:flt, {18, 28, 200.0}, ~c""200.0""}',
        '{:char, {282, 22, ~c""?[""}, 91}']

    def test_split_lexeme(self):
        token_string = '{:identifier, {1, 1, ~c"defmodule"}, :defmodule}'
        a, b, c = last_check.split_lexeme(token_string)
        unittest.TestCase.assertEqual(self, a, 1)
        unittest.TestCase.assertEqual(self, b, ":identifier")
        unittest.TestCase.assertEqual(self, c, ":defmodule")

        # heredoc 3 part tuple

        token_string = '{:bin_heredoc, {48, 8, nil}, 2, ["Asks for confirmation to the user.\nIt allows the user to answer or respond with the following options:\n  - Yes, yes, YES, Y, y\n  - No, no, NO, N, n\n\nIn case that the answer is none of the above, it will prompt again until we do.\n\n## Examples\n\nTo ask whether the user wants to delete a file or not:\n\n  ExPrompt.confirm(\"Are you sure you want to delete this file?\n\'")\n"]}'
        a, b, c = last_check.split_lexeme(token_string)
        unittest.TestCase.assertEqual(self, a, 48)
        unittest.TestCase.assertEqual(self, b, ":bin_heredoc")
        unittest.TestCase.assertEqual(self, c,
                                      '2, ["Asks for confirmation to the user.\nIt allows the user to answer or respond with the following options:\n  - Yes, yes, YES, Y, y\n  - No, no, NO, N, n\n\nIn case that the answer is none of the above, it will prompt again until we do.\n\n## Examples\n\nTo ask whether the user wants to delete a file or not:\n\n  ExPrompt.confirm(\"Are you sure you want to delete this file?\n\'")\n"]')
        # fn 2 part tuple
        token_string = '{:fn, {126, 26, nil}}'
        a, b, c = last_check.split_lexeme(token_string)
        unittest.TestCase.assertEqual(self, a, 126)
        unittest.TestCase.assertEqual(self, b, ":fn")

    def test_read_diff(self):
        text = self.read_file(filepath='token_array.txt')
        x = last_check.parse_to_lexeme_list(text)
        for i in range(len(x)):
            unittest.TestCase.assertEqual(self, x[i], self.token_list[i])

    def test_split_lexeme2(self):
        for i in range(len(self.token_list)):
            a, b, c = last_check.split_lexeme(self.token_list[i])


    @staticmethod
    def read_file(filepath):
        file = open(filepath, 'rt')
        chunk = file.read()
        file.close()
        return chunk
