import json
import pickle
import csv
import xml.etree.ElementTree as ET


def get_files():
    files = input("Print file_from and file_to: ")
    if len(files.split()) < 2:
        raise Exception('Incorrect Input')
    files = files.split()
    file_from, file_to = files[0], files[1]
    return file_from, file_to


def check_and_get_ext(file_from, file_to):
    try:
        divided = file_from.split('.')[1], file_to.split('.')[1]
    except IndexError:
        print('Incorrect Input!')
    else:
        for elem in divided:
            if elem not in ['json', 'csv', 'txt', 'xml']:
                raise Exception('Incorrect Input!')
            else:
                file_from_ext, file_to_ext = divided[0], divided[1]
            return file_from_ext, file_to_ext


def json_reader(file_from):
    with open(file_from, 'r') as file_from:
        data = json.load(file_from)
    return data


def json_writer(data, file_to):
    with open(file_to, 'w') as file_to:
        json.dump(data, file_to, indent=3)


def pickle_reader(file_from):
    with open(file_from, 'rb') as file_from:
        data = pickle.load(file_from)
    return data


def pickle_writer(data, file_to):
    with open(file_to, 'wb') as file_to:
        pickle.dump(data, file_to)


def csv_reader(file_from):
    with open(file_from, 'r') as file_from:
        reader = csv.DictReader(file_from)
        data = [dct for dct in reader]
    return data


def csv_writer(data, file_to):
    with open(file_to, 'w') as file_to:
        writer = csv.DictWriter(file_to, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def xml_reader(file_from):
    with open(file_from, 'r') as file_from:
        tree = ET.parse(file_from)
        root = tree.getroot()
        data = []
        for elem in root:
            if not elem.getchildren():
                data.append({elem.tag: elem.text})
            else:
                data.append({elem.tag: {child.tag: child.text for child in elem}})
    return data


def xml_writer(data, file_to):
    with open(file_to, 'w') as file_to:
        res_str = ''
        for k, v in data.items():
            # strings with -1 children
            if type(v) is type([]) and type(v[0]) is type({}):
                m_res_str = ''
                for m_dct in v:
                    for m_key, m_val in m_dct.items():
                        m_res_str += f'<{m_key}>{m_val}</{m_key}>\n'
                res_str += f'<{k}>\n{m_res_str}</{k}>'
            # strings with no children
            else:
                string = f'<{k}>{v}</{k}>\n'
                res_str += string
        result = f'<root>\n{res_str}\n</root>'
        file_to.write(result)


def get_function(file_ext):
    functions = {
        'json': (json_reader, json_writer),
        'csv': (csv_reader, csv_writer),
        'txt': (pickle_reader, pickle_writer),
        'xml': (xml_reader, xml_writer)
    }
    return functions[file_ext]


if __name__ == "__main__":
    file_from, file_to = get_files()
    print('File From:', file_from, '||', 'File To:', file_to)
    extensions = check_and_get_ext(file_from, file_to)
    print('Extensions:', extensions)
    read_file_ext, write_file_ext = extensions[0], extensions[1]
    read_func = get_function(read_file_ext)[0]
    write_func = get_function(write_file_ext)[1]
    data = read_func(file_from)
    write_func(data, file_to)
    print('CLEAR!!!')
