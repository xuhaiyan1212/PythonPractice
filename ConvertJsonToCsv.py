import json
import csv


def csv_writer(data, path):
    with open(path, 'w', encoding='utf-8') as fh:
        writer = csv.writer(fh, delimiter='\t')
        for line in data:
            writer.writerow(line)


if __name__ == "__main__":
    ParseData = []
    path = r'./files/JsonToCsvOutput.csv'

    with open(r'./files/data.json', 'r+', encoding='utf-8') as fio:
        FileData = fio.read()

    json_string = '{"Object":[' + FileData+']}'

    data = json.loads(json_string)

    try:
        for element in data['Object']:
            ElementData = [element['created'],
                           element['status'],
                           element['tasks'][0]['input_values']['coordinates'],
                           element['tasks'][0]['id'],
                           element['user_id']]
            ParseData.append(ElementData)

    except (ValueError, KeyError, TypeError):

        print("Error JSON")

    csv_writer(ParseData, path)