import json
import re
suggestion = {}
file = open("hsk_dic.json", "r")
new_dict = json.load(file)
wrong_words=['判刑','唱歌']
for wrong_word in wrong_words:
    modified_list = []
    if not new_dict.get(wrong_word):
        continue
    for sen in new_dict[wrong_word]:
        modified_sen = []
        modified_sen.append(sen[0])
        modified_sen.append(sen[1].replace(wrong_word, '<span class="example_key">' + wrong_word + '<span>'))
        modified_sen.append(sen[2])
        modified_sen.append(sen[3])
    modified_list.append(modified_sen)

    suggestion[wrong_word] = modified_list
# suggestion = json.dumps(suggestion)

print(suggestion)