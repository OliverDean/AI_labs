def read_dictionary_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

def is_one_letter_diff(word1, word2):
    return sum(a != b for a, b in zip(word1, word2)) == 1
    
def generate_neighbors(word, word_set):
    neighbors = []
    for i in range(len(word)):
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if char != word[i]:
                new_word = word[:i] + char + word[i+1:]
                if new_word in word_set:
                    neighbors.append(new_word)
    return neighbors

def bidirectional_bfs(startWord, endWord, word_set):
    if startWord == endWord:
        return [startWord]
    
    word_set = set(word_set)
    queue_start = [[startWord]]
    queue_end = [[endWord]]
    visited_start = {startWord: [startWord]}
    visited_end = {endWord: [endWord]}
    
    found_path = None

    while queue_start and queue_end:
        if found_path and (len(queue_start[0]) + len(queue_end[0]) - 1 > len(found_path)):
            return found_path

        # Expand from the start
        path_start = queue_start.pop(0)
        node_start = path_start[-1]
        for neighbor in generate_neighbors(node_start, word_set):
            if neighbor in visited_end:
                if is_one_letter_diff(node_start, neighbor):
                    current_path = path_start + visited_end[neighbor][::-1]
                    if not found_path or len(current_path) < len(found_path):
                        found_path = current_path
            if neighbor not in visited_start:
                visited_start[neighbor] = path_start + [neighbor]
                queue_start.append(visited_start[neighbor])

        # Expand from the end
        path_end = queue_end.pop(0)
        node_end = path_end[-1]
        for neighbor in generate_neighbors(node_end, word_set):
            if neighbor in visited_start:
                if is_one_letter_diff(node_end, neighbor):
                    current_path = visited_start[neighbor] + path_end[::-1]
                    if not found_path or len(current_path) < len(found_path):
                        found_path = current_path
            if neighbor not in visited_end:
                visited_end[neighbor] = path_end + [neighbor]
                queue_end.append(visited_end[neighbor])
                
    return found_path if found_path else []

def find_path(dictionary, startWord, endWord):
    return bidirectional_bfs(startWord, endWord, dictionary)


# Read the dictionary from file and call the function
dictionary = read_dictionary_from_file('dictionary.txt')
startWord = "ABY"
endWord = "WOO"

print(find_path(dictionary, startWord, endWord))

# def find_path(dictionary, start_word, end_word):
#     '''
#     returns a list of the word in the shortest path 
#     from start_word to end_word, 
#     where successive words are different in only one letter.
#     '''
    
