import json
from queue import PriorityQueue

words_dictionary = {}


def file_init(word_len):
    global words_dictionary
    chars = 'abcdefghijklmnopqrstuvwxyz'
    init_dict = {}
    freq = {}
    freq_p = []
    for i in range(word_len):
        freq_p.append({})
    for char in chars:
        freq.update({char : 0})
        for i in range(word_len):
            freq_p[i].update({char : 0})
    if len(words_dictionary) == 0:
        with open('words_dictionary.json', 'r') as f:
            words_dictionary = json.load(f)
    
    for word in words_dictionary:
        if len(word) == word_len:
            for i, char in enumerate(word):
                freq_p[i][char] += 1
                freq[char] += 1
            init_dict.update({word : 0})
    dict_len = len(init_dict)
    pq = PriorityQueue()
    word_list = []
    for word in init_dict:
        score = 0
        for i, char in enumerate(word):
            if char in word[:i]:
                score += dict_len * 4
            score -= freq[char]
            score -= freq_p[i][char]*word_len*2
        pq.put((score, word))
    while not pq.empty():
        word_list.append(pq.get()[1])
    
    with open('word'+str(word_len)+'.json', 'w') as f:
        f.write(json.dumps(word_list, indent=4))

    with open('len'+str(word_len)+'.json', 'w') as f:
        f.write(json.dumps(init_dict, indent=4))


def keep(word, positions, rules, guess):
    for x, r in enumerate(rules):
        if r == 'y':
            if word[x] == guess[x]:
                return False
            remove = True
            for i, c in enumerate(word):
                if not i in positions and c == guess[x]:
                    remove = False
            if remove:
                return False
        elif r == '*':
            positions.append(x)
            if not word[x] == guess[x]:
                return False
        elif guess[x] in word:
            return False
    return True


def narrow(word_list, positions, rules, guess):
    for word in word_list:
        word_list[:] = [word for word in word_list if keep(word, positions, rules, guess)]
        

def game(word_len):
    with open('word'+str(word_len)+'.json', 'r') as f:
        word_list = json.load(f)
    status = ''
    positions = []
    count = 0
    play = True
    while play:
        for i in range(min(5, len(word_list))):
            print(word_list[i], end=", ")
        word = input()
        status = input()
        play = not status == '*' * word_len
        narrow(word_list, positions, status, word)
        # print(word_list)
        # print()
        count += 1
    print(count)
        


# freq_p = []
# freq = []


# for i in range(3, 11):
#     freq.append([0] * 26)
#     freq_p.append([])
#     for j in range(i):
#         freq_p[i-3].append([0] * 26)

# for i in range(3, 11):
#     with open('len'+str(i)+'.json', 'r') as f:
#         words = json.load(f)
#     for word in words:
#         for x, char in enumerate(word):
#             freq[i-3][char-'a'] += 1
#             freq_p[i-3][x][char-'a'] += 1

# print(freq_p)

#sorel
#guest
#eight

if __name__ == "__main__":
    game(8)