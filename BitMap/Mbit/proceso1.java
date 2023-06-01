package Mbit;

import java.util.ArrayList;
import java.util.List;

public class proceso1
{
    //Attributes
    private int size; //Tamaño del proceso en bloques
    private final String name; //Nombre del proceso
    // se agrega una lista para guardar los segmentos en los que se divide el proceso para guardarlos en memoria
    List<segmento> segmentos = new ArrayList<>();
    public int remanente;

    //Constructors
    public proceso1(String name, int size, int[] disponibilidad) //Constructor
    {
        this.name = name; //Asigna el nombre del proceso
        this.size = size; //Asigna el tamaño del proceso
        System.out.println("disponibilidad: "+disponibilidad);
        remanente = divideProceso(size, disponibilidad);
        System.out.println("remanente: "+remanente);
    }
    public  List<segmento> getSegmentos(){
        return segmentos;
    }
    public int divideProceso(int size, int[] disponibilidad) {
        // esta funcion divide al proceso si es mayor o igual a 31 bloques y lo guarda en una pila de segmentos
      
        
        int index=0, sizeaux=0;
        // pero si el tamaño es menor a 31 se crea un solo segmento
        int a = Verifica_procesoCorrido(size, disponibilidad);
        for (int i = a; i < disponibilidad.length; i++) {
            int auxdisp=disponibilidad[i], operation = size-auxdisp;
            if (disponibilidad[i]>=0){
                if (operation>0) {
                    size=operation;
                    segmento s = new segmento(auxdisp, index);
                    segmentos.add(s);
                }
                sizeaux = size;  
                int tamaño,cont= 1+ (int) Math.ceil(size/31); //cont es el numero de segmentos que se crearan 
                System.out.println("cont: "+cont);
                while (cont>0) {
                    tamaño=sizeaux;
                    System.out.println("tamaño: "+tamaño);
                    
                    if(sizeaux>31){
                        sizeaux-=31;
                        tamaño=31;
                        auxdisp=0;
                    }
                    segmento s = new segmento(tamaño, index);
                    segmentos.add(s);
                    cont--;
                    index++;
                }
                    break;
            }
            
            
        }  
        return a;
    }
    public int Verifica_procesoCorrido(int size ,int [] disponibilidad){
        int posicion=0;
        int disponibilidadAcumulada=0;
        int con= 1+ (int) Math.ceil(size/31); 
        for (int i = 0; i < disponibilidad.length; i++) {
            if (disponibilidad[i]>0) {
                disponibilidadAcumulada=disponibilidad[i];
                for (int j=1; j<=con; j++) {
                    disponibilidadAcumulada+=disponibilidad[i+j];
                    System.out.println("indice i "+i+" indicej "+j +" disponibilidadAcumulada: "+disponibilidadAcumulada);
                }
                if (disponibilidadAcumulada>=size) {
                    posicion=i;
                    break;
                }
            }
            
        }
        return posicion;
    }
    public proceso1(String name)
    {
        this.name = name;
    }

    public String getName()
    {
        return name;
    }

    public int getSize()
    {
        return size;
    }

}
