from nim import Nim

n = Nim()

print(n.available_actions([1, 3, 5, 7]))

print(n.player)
n.switch_player
print(n.player)

