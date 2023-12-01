import re
from typing import NamedTuple, Optional


class ParsedMessage(NamedTuple):
    category_alias: Optional[str]
    amount: int
    comment: Optional[str]


    def __str__(self):
        return  f"ParsedMessage(category_alias={self.category_alias}, amount={self.amount}, comment={self.comment})"


# def determine_the_expense_on_inline(raw_message: str) -> dict:
#     regexp = re.match(r"([\d]+) (.*)", raw_message)

#     if not regexp:
#         return None

#     amount = int(regexp.group(1))
#     comment = regexp.group(2)

#     result = {
#         'amount': amount,
#         'comment': comment
#     }

#     return result


def _parse_message(raw_message: str, inline: bool=False) -> ParsedMessage:
    if inline:
        pattern = re.compile(r"([\d]+) ([^\d]+)")
    else:
        pattern = re.compile(r"([\d]+) ([^\s\d]+)( .+)?")

    regexp_result = pattern.match(raw_message)

    if not regexp_result:
        return None

    amount = int(regexp_result.group(1))

    if inline:
        category_alias = None
        comment = regexp_result.group(2)
    else:
        category_alias = regexp_result.group(2)
        comment = regexp_result.group(3).strip() if regexp_result.group(3) else None

    return ParsedMessage(category_alias, amount, comment)
