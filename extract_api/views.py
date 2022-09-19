from enum import Enum

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from extract_api.serializers import FileSerializer


class ExtractorStates(Enum):
    READY = 0
    SAVED = 1
    STANDBY = 2


def get_next_state(state: ExtractorStates):
    value = state.value
    value += 1

    if value == len(ExtractorStates):
        value = 0

    return ExtractorStates(value)

    # state.value += 1
    #
    # if state.value == len(ExtractorStates):
    #     state.value = 0
    #
    # return state.value


def extractor(receipt):
    begin_row = False
    begin_col = False
    counter = 0
    blocks = []
    end_column = 0
    current_state = ExtractorStates.READY

    # add extra line at the end of the file
    # file_object = open('receipt', 'a')
    # receipt.seek(0)
    # receipt.write(b'\n')
    # receipt.write(b'\n')
    print('receipt: ', receipt)

    whitespaces = b'\r\n'
    delimiters = [b'---']

    for line in receipt:
        print(line)
        counter += 1
        print('counter: ', counter)

        # delimiter: bool = not line.rstrip(b'\r\n') or b'---' in line
        # is_delimiter: bool = not line.rstrip(whitespaces) or any(delimiters) in line
        is_delimiter: bool = not line.rstrip(whitespaces) or any(substring in line for substring in delimiters)
        print('delimiter: ', is_delimiter)
        print('current state: ', current_state)

        if not is_delimiter:
            print('in not delimiter')
            begin_row = counter if begin_row is False else begin_row
            begin_col = len(line) - len(line.lstrip()) if begin_col is False else begin_col
            end_column = len(line)
            current_state = ExtractorStates.READY
            print('current state is ready... in not delimiter')

        if is_delimiter and current_state == ExtractorStates.READY:
            print('current state is ready')
            blocks.append({
                'begin_row': begin_row,
                'begin_col': begin_col,
                "end_row": counter - 1,
                'end_column': end_column,
            })

            begin_row = False
            begin_col = False
            current_state = ExtractorStates.SAVED

            print(blocks)

            # continue

        # if not delimiter:
        #     print('in not delimiter')
        #     begin_row = counter if begin_row is False else begin_row
        #     end_column = len(line)
        #     current_state = ExtractorStates.READY
    else:
        # capture last rows if it's a block
        if begin_row:
            blocks.append({
                'begin_row': begin_row,
                'begin_col': begin_col,
                "end_row": counter,
                'end_column': end_column,
            })

    # if current_state
    print('outside... blocks', blocks)
    print('last state: ', current_state)
    return blocks


def extractor2(receipt):
    # with open(receipt, 'r') as file:
    chunk = ''
    delimiter = ''
    begin_row = False
    to_commit = False
    begin_column = 0
    counter = 0
    blocks = []
    end_column = None
    for line in receipt:
        print(line)

        counter += 1
        to_commit = not line.rstrip(b'\r\n')
        if to_commit and (line == b'\r\n' or b'---' in line):
            print('ignoring line and commiting chunk')
            blocks.append({
                'begin_row': begin_row,
                'begin_col': 0,
                "end_row": counter - 1,
                'end_column': end_column,
            })
            begin_row = False
            print(blocks)
            continue

        begin_row = counter if begin_row is False else begin_row
        end_column = len(line)


class ReceiptAPI(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        print('in post')
        file_serializer = FileSerializer(data=request.data)
        print(file_serializer)
        if file_serializer.is_valid():
            print('file is valid')
            receipt_file = request.FILES.get('receipt')
            print(receipt_file)
            blocks = extractor(receipt_file)
            return Response({'blocks': blocks}, status=status.HTTP_200_OK)
        print('something went wrong')
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
