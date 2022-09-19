from enum import Enum
from typing import Tuple

WHITESPACES = b'\r\n'
DELIMITERS = [b'---']


class ExtractorStates(Enum):
    READY = 0
    SAVED = 1


def text_blocks_extractor(receipt) -> Tuple[list, list]:
    """
    Extracts relevant information from receipt file
    :param receipt: Uploaded receipt file
    :return: tuple containing lists of text_extracts (receipt content) and
    blocks containing row and column information
    """

    begin_row = begin_column = False
    end_column = 0
    counter = 0
    blocks = []
    current_state = ExtractorStates.READY

    text_extract = []
    block_info = ''

    for line in receipt:
        counter += 1
        is_delimiter: bool = not line.rstrip(WHITESPACES) or any(substring in line for substring in DELIMITERS)

        if not is_delimiter:
            begin_row = counter if begin_row is False else begin_row
            begin_column = len(line) - len(line.lstrip()) if begin_column is False else begin_column
            end_column = len(line)
            current_state = ExtractorStates.READY

            block_info += line.decode('utf-8')

        if is_delimiter and current_state == ExtractorStates.READY:
            blocks.append({
                'begin_row': begin_row,
                'begin_col': begin_column,
                "end_row": counter - 1,
                'end_column': end_column,
            })

            text_extract.append(block_info)
            block_info = ''

            begin_row = False
            begin_column = False
            current_state = ExtractorStates.SAVED

    else:
        # capture last rows if it's a block
        if begin_row:
            blocks.append({
                'begin_row': begin_row,
                'begin_col': begin_column,
                "end_row": counter,
                'end_column': end_column,
            })

            text_extract.append(block_info)

    return text_extract, blocks
