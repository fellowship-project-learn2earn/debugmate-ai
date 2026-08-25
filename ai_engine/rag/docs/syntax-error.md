# SyntaxError
tags: syntaxerror, invalid syntax

SyntaxError means Python couldn't even parse the code -- a missing colon, unmatched parenthesis/bracket/quote, or a misplaced keyword. The line number Python reports is often the line AFTER the actual mistake, since Python doesn't realize something's wrong until it reads further. Fix by checking the reported line and the one immediately before it for the true source of the issue.
