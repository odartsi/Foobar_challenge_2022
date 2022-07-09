def solution(data, n): 
    from collections import Counter
    counting_set= Counter(data)
    x=[key for key,value in counting_set.items() if value>n]
    data=list(filter(lambda i : i not in x, data)) 
    return data
