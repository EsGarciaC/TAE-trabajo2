import matplotlib.pyplot as plt
lista_revol_util = [-4,-14,11,-3,8,11,-6,1,-1,15]
x1 = range(0, 10)
x = [i/10 for i in x1]
plt.scatter(x, lista_revol_util)
plt.xlabel(xlabel="Porcentaje utilizado")
plt.ylabel(ylabel="Puntaje")
plt.grid(visible=True)
plt.title(label="revol_util vs Score")
plt.show()

