from src.rust_parser.utils import transform_paths, UseStatementsOneLine, UseStatementsOneLineDiffText

file_path = "./data/read_diff_rust.txt"
output_text = UseStatementsOneLineDiffText(file_path)
#output_text2 = transform_paths(file_path)
print(output_text)

