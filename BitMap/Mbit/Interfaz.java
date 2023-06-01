package Mbit;

import java.util.List;
import java.util.Scanner;

public class Interfaz {
    public static void main (String[] args) {

        try (Scanner entry = new Scanner(System.in)) {
            int option,sizeProcedure;
            String nameProcedure;
            memoria manager = new memoria();
            do {
                System.out.println("1Estado de la Memoria:\n"+manager.bitMapToString());
                System.out.println("1.Introducir procedimiento");
                System.out.println("2.Eliminar Procedimiento");
                System.out.println("3.salir");
                System.out.print("Elige una opción: ");
                option = entry.nextInt();
                print_ActiveProcess(manager);
                switch (option)
                {
                    case 1:
                        try
                        {
                            System.out.println("1.Introducir procedimiento");
                            System.out.print("Ingrese el nombre del procedimiento: ");
                            nameProcedure = entry.next();

                            System.out.print("Ingrese el tamaño del procedimiento (bloques): ");
                            sizeProcedure = entry.nextInt();
                            manager.addProcess(nameProcedure, sizeProcedure);
                        }
                        catch (Exception e)
                        {
                            System.out.println(e);
                            option = 3;
                        }
                        break;
                    case 2:
                        System.out.println("2.Eliminar Procedimiento");
                        System.out.print("Ingrese el nombre para eliminar: ");
                        String name = entry.next();
                        manager.removeProcess(name);
                        print_ActiveProcess(manager);
                        break;
                    case 3:
                        System.out.println("Gracias por usar");
                        break;
                    default:
                        System.out.println("Elija una opcion valida");
                }
                print_ActiveProcess(manager);
            }while(option != 3);
        }
    }
    private static void print_ActiveProcess(memoria manager){
        List<proceso1> lista = manager.getProcess();
        System.out.println("\nNombres de procesos en memoria");
        for(int j = 0;j < lista.size() ;j++){
            System.out.println(String.format("%x. Nombre: %s",j+1,lista.get(j).getName()+" tamaño: "+lista.get(j).getSize()));
            List <segmento> lista2 = lista.get(j).getSegmentos();
            for(int i = 0;i < lista2.size() ;i++){
                System.out.println(String.format("   Segmento: %s",lista2.get(i).getIndex()+" tamaño: "+lista2.get(i).getSize()+" Inicio: "+lista2.get(i).getStart()[0]+" Sector:"+lista2.get(i).getStart()[1]));
            }
        }

    }
}
