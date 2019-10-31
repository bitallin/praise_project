import re
from string import digits


def main(path):
    data_list = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            remove_digits = str.maketrans('', '', digits)
            res = line.translate(remove_digits)
            remove_dot = res.replace('.', '')
            res = remove_dot.strip()
            if len(res) > 2:
                data_list.append(res)
        f.close()

    return data_list


if __name__ == '__main__':
    path = 'data/praise_sentences.txt'
    data_list = main(path)
    des_path = 'data/praise_dataset.txt'
    with open(des_path, 'w', encoding='utf-8') as f:
        for i in data_list:
            f.write(i+'\n')
        f.close()