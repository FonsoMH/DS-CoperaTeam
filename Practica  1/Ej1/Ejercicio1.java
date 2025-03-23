//seguir añadiendo clases y to eso
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

// Interfaz de la Factoría Abstracta
interface FactoriaCarreraYBicicleta {
    Carrera crearCarrera(int numBicicletas);
    Bicicleta crearBicicleta(int id);
}

// Clase abstracta Bicicleta
abstract class Bicicleta {
    protected int id;
    
    public Bicicleta(int id) {
        this.id = id;
    }
    
    public int getId() {
        return id;
    }
}

// Clase abstracta Carrera
abstract class Carrera implements Runnable {
    protected List<Bicicleta> bicicletas;
    protected int duracion = 60; // Duración en segundos
    protected double porcentajeRetiro;
    
    public Carrera(int numBicicletas, double porcentajeRetiro) {
        this.bicicletas = new ArrayList<>();
        this.porcentajeRetiro = porcentajeRetiro;
    }
    
    public void iniciarCarrera() {
        System.out.println(getClass().getSimpleName() + " iniciando con " + bicicletas.size() + " bicicletas...");
        try {
            Thread.sleep(duracion * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        retirarBicicletas();
        System.out.println(getClass().getSimpleName() + " finalizada con " + bicicletas.size() + " bicicletas.");
    }
    
    private void retirarBicicletas() {
        int aRetirar = (int) (bicicletas.size() * porcentajeRetiro);
        for (int i = 0; i < aRetirar; i++) {
            bicicletas.remove(0);
        }
        System.out.println(aRetirar + " bicicletas retiradas de " + getClass().getSimpleName());
    }
    
    public void agregarBicicleta(Bicicleta bicicleta) {
        bicicletas.add(bicicleta);
    }
    
    @Override
    public void run() {
        iniciarCarrera();
    }
}

// Implementaciones concretas de Bicicleta
class BicicletaMontana extends Bicicleta {
    public BicicletaMontana(int id) { super(id); }
}

class BicicletaCarretera extends Bicicleta {
    public BicicletaCarretera(int id) { super(id); }
}

// Implementaciones concretas de Carrera
class CarreraMontana extends Carrera {
    public CarreraMontana(int numBicicletas) {
        super(numBicicletas, 0.2);
    }
}

class CarreraCarretera extends Carrera {
    public CarreraCarretera(int numBicicletas) {
        super(numBicicletas, 0.1);
    }
}

// Implementaciones concretas de las Factorías
class FactoriaMontana implements FactoriaCarreraYBicicleta {
    public Carrera crearCarrera(int numBicicletas) {
        CarreraMontana carrera = new CarreraMontana(numBicicletas);
        for (int i = 0; i < numBicicletas; i++) {
            carrera.agregarBicicleta(new BicicletaMontana(i + 1));
        }
        return carrera;
    }
    
    public Bicicleta crearBicicleta(int id) {
        return new BicicletaMontana(id);
    }
}

class FactoriaCarretera implements FactoriaCarreraYBicicleta {
    public Carrera crearCarrera(int numBicicletas) {
        CarreraCarretera carrera = new CarreraCarretera(numBicicletas);
        for (int i = 0; i < numBicicletas; i++) {
            carrera.agregarBicicleta(new BicicletaCarretera(i + 1));
        }
        return carrera;
    }
    
    public Bicicleta crearBicicleta(int id) {
        return new BicicletaCarretera(id);
    }
}

// Clase principal para ejecutar la simulación
public class Ejercicio1 {
    
    public static void main(String[] args) {
        int numBicicletas = new Random().nextInt(10) + 5; // Generamos entre 5 y 15 bicicletas
        System.out.println("Número inicial de bicicletas: " + numBicicletas);

        FactoriaCarreraYBicicleta factoriaMontana = new FactoriaMontana();
        FactoriaCarreraYBicicleta factoriaCarretera = new FactoriaCarretera();

        Carrera carreraMontana = factoriaMontana.crearCarrera(numBicicletas);
        Carrera carreraCarretera = factoriaCarretera.crearCarrera(numBicicletas);

        Thread threadMontana = new Thread(carreraMontana);
        Thread threadCarretera = new Thread(carreraCarretera);
        
        threadMontana.start();
        threadCarretera.start();
    }
    
}
