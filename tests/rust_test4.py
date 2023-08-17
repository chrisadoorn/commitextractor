
script = """@@ -0,0 +1,456 @@
+// Copyright (c) 2020 E.S.R.Labs. All rights reserved.
+//
+// NOTICE:  All information contained herein is, and remains
+// the property of E.S.R.Labs and its suppliers, if any.
"""

def splits(script: str) -> str:
    if '//' in script:
        return script.split('//')[0]
    else:
        return script

lines = script.split('\n')
for line in lines:
    print(splits(line))