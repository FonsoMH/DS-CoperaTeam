from abc import ABC, abstractmethod

# Interfaz Filtro
class Filter(ABC):
    @abstractmethod
    def execute(self, cadena):
        pass

# Filtro que comprueba que haya texto antes del caracter @
class FilterMail(Filter):
    def execute(self, cadena):
        if "@" not in cadena:
            print("Error: No es un correo.")
            return False
        
        parte_antes, parte_despues = cadena.split("@", 1)
        if not parte_antes:
            print("Error: El correo electrónico debe contener texto antes del carácter '@'.")
            return False
        
        if parte_despues not in ["gmail.com", "hotmail.com"]:
            print("Error: El dominio del correo electrónico debe ser gmail.com o hotmail.com.")
            return False
        
        print("Correo electrónico válido.")
        return True


# Filtro que comprueba la longitud de la contraseña
class PasswordSizeFilter(Filter):
    def execute(self, cadena):
        if len(cadena) < 8:
            print("Error: La contraseña debe tener al menos 8 caracteres.")
            return False
        
        return True

# Filtro que comprueba que contenga al menos un número
class PasswordNumberFilter(Filter):
    def execute(self, cadena):
        if not any(char.isdigit() for char in cadena):
            print("Error: La contraseña debe contener al menos un número.")
            return False
        
        return True

# Filtro que comprueba que contenga al menos una letra mayúscula
class PasswordUpperFilter(Filter):
    def execute(self, cadena):
        if not any(char.isupper() for char in cadena):
            print("Error: La contraseña debe contener al menos una letra mayúscula.")
            return False
        
        return True
    
# Clase de Cadena de Filtros
class FilterChain:
    def __init__(self):
        self.filters = []
        self.target = None

    def add_filter(self, filter):
        self.filters.append(filter)

    def set_target(self, target):
        self.target = target

    def execute(self, cadena):
        valido = True
        for filter in self.filters:
            if not filter.execute(cadena):
                valido = False  # Si un filtro falla debja de ser valida la psswd
        if valido:  
            self.target.execute()
        return valido

# Clase Target
class Objetivo:
    def execute(self):
        print("Autenticación exitosa para 1 de los filtros")


# Clase FilterManager
class FilterManager:
    def __init__(self, target):
        self.cadena_correo = FilterChain()
        self.cadena_psswd = FilterChain()
        self.cadena_psswd.target = target
        self.cadena_correo.target = target

    def add_correo_filter(self, filter):
        self.cadena_correo.add_filter(filter)

    def add_contrasena_filter(self, filter):
        self.cadena_psswd.add_filter(filter)

    def postCadena(self, email, password):
        if not self.cadena_correo.execute(email):
            print("Correo electrónico no válido.")
            return False
        
        if not self.cadena_psswd.execute(password):
            print("Contraseña no válida.")
            return False
        
        return True
    


# Cliente
def main():

    servicio_autenticacion = Objetivo()

    # Crear el gestor de filtros y pasarle el Target
    gestor = FilterManager(servicio_autenticacion)

    # Agregar filtros para el correo
    gestor.add_correo_filter(FilterMail())

    # Agregar filtros para la contraseña
    gestor.add_contrasena_filter(PasswordSizeFilter())
    gestor.add_contrasena_filter(PasswordNumberFilter())
    gestor.add_contrasena_filter(PasswordUpperFilter())

    correo = input("Introduce tu correo: ")
    contrasena = input("Introduce tu contraseña: ")


    # Procesar las credenciales
    if gestor.postCadena(correo, contrasena):
        print("Bienvenido.")
    else:
        print("Error en las credenciales. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()