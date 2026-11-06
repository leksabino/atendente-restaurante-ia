from consultas import listar_pratos, buscar_prato, filtrar_por_dieta

print(buscar_prato("hamburguer"))
print(buscar_prato("HAMBÚRGUER"))
print(buscar_prato("pernil"))
print(buscar_prato("suco de laranja"))
print(filtrar_por_dieta("vegano"))
print(filtrar_por_dieta("vegetariano"))
print(filtrar_por_dieta("carnivoro"))