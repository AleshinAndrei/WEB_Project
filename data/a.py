a = {1: 2, 4: 5}
print(list(map(lambda pair: f"{str(pair[0])}:{str(pair[1])}", a.items())))