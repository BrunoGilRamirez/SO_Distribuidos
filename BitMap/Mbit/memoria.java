package Mbit;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;


public class memoria {
    private final int[] bitMap = new int[32]; //Mapa de bits "final" para que no se pueda modificar su tamaño
    private final List<proceso1> process = new ArrayList<>();
    private int contador;
    public int[] remanentes= new int[32];
    public memoria() {
        Arrays.fill(bitMap,0); //Inicializa el mapeo de bits con 0
        contador=0;
    }
    public List<proceso1> getProcess() {
        return process;
    }

    public int[] getBitMap(){
        return bitMap;
    }
    /**
     *  Añade un nuevo proceso a la memoria
     * @param p1 Proceso a añadir a la memoria
     * @return 1 si tuvo exito ó -1 si no lo tuvo
     */
    public int addProcess(String name, int size){  //Añade un proceso a la memoria
        int[] remanente= getRemanente();
        proceso1 p1 = new proceso1(name, size, remanente);
        int numBlocks; //Numero de bloques que necesita el proceso
        int numBinary; //Numero en binario que se necesita para el proceso
        int[] result; //Arreglo que guarda la posicion inicial del proceso y en que entero del mapa de bits
        int startProcess;
        int bitAux;
        List <segmento> segmentos = p1.getSegmentos();
        int i=0;
        while(i<segmentos.size()){
            segmento segmento = segmentos.get(i);
            numBlocks = segmento.getSize(); /* Calcula el numero de bloques que necesita */
            String bin= generateNumBinary(numBlocks);
            numBinary = Integer.parseInt(bin, 2);
            result = searchPlace(p1.remanente,numBinary,numBlocks);
            p1.segmentos.get(i).setStart(result);
            if(result[0] < 0) return -1;
            startProcess = result[0];
            bitAux = result[1];
            this.bitMap[bitAux] = this.bitMap[bitAux] | (numBinary << startProcess); //Asigna los bits necesarios en el mapa de bits
            segmento.setStart(result); //Guarda en que entero se encuentra y en cual bit inicia
            i++;
        }
        this.process.add(p1);
        return 1;
    }
    /**
     * Remueve un proceso de la memoria
     * @param name Nombre del proceso que se quiere eliminar
     * @return Un entero, 1 si fue exitosa la operacion, -1 si no lo fue
     */
    public void removeProcess(String name){
        int[] result = new int[2];
        int a = process.size()-1;

        for (int i = a;i>=0;i--){
            boolean op=process.get(i).getName().compareTo(name) == 0;
            if(op && process.isEmpty()==false ){
                List <segmento> segmentos = process.get(i).getSegmentos();
                int j=segmentos.size()-1;
                while(j>=0){

                    segmento segmento = segmentos.get(j); //Obtiene el segmento
                    result = segmento.getStart(); //Obtiene la posicion inicial del segmento
                    int binary = Integer.parseInt(generateNumBinary(segmento.getSize()),2); //Obtiene el numero binario del segmento
                    
                    binary = binary << result[0];   //Corre el numero binario a la posicion inicial
                    this.bitMap[result[1]] = this.bitMap[result[1]] ^ binary; //Remueve los bits del mapa de bits
                    segmentos.remove(segmento);
                    j--;
                }
                process.remove(process.get(i));
            }
        }
    }

    /**
     * Busca si existe espacio en la memoria paa un proceso
     * @param binary Numero que representa el binario de los bloques a guardar
     * @param numBlocks Numero de bloques que se van a guardar
     * @return Un arreglo de enteros donde esta guardado la posision inicial del proceso y en que entero del mapa de bits
     */
    private int[] searchPlace(int ab,int binary, int numBlocks) {
        int j = 0,auz=0; auz+=ab;
        int binaryAux;
        int result[] = new int[3];
        int a1;
        if (numBlocks >=31) a1=Math.abs(numBlocks);
        else a1=Math.abs(32-numBlocks);

        for (int i = auz; i < this.bitMap.length; i++) {
            binaryAux = binary;
            
            //System.out.println ("bloques: "+ a1);
            while (j < a1){
                int a= this.bitMap[i], a2=(binaryAux << j);
                //System.out.println("bitmap: "+j+"corrimiento: "+ Integer.toBinaryString(a)+" a2: "+Integer.toBinaryString(a2)+" or "+a2);
                if((this.bitMap[i] & (binaryAux << j)) == 0){
                    result[0] = j; //Guarda la posision inical
                    result[1] = i; //Guarda el numero de entero
                    //if (this.bitMap[i]!=0)result[2] = numBlocks-(numBlocks-j); //Guarda el numero de bloques restantes
                    //else result[2] =0;
                     //Guarda la posision
                    //System.out.println("restante: "+ result[2]);
                    return result;
                }
                j++;

            }
            j=0;
        }
        result[0] = -1;
        return result;
    }
    //funcion que calcula la disponibilidad de la memoria, retorna un entero que es el remanente en un bloque de 32 bits
    public int[] getRemanente(){
        int remanente=0;
        Arrays.fill(remanentes,31);
        for (int i = 0; i < this.bitMap.length; i++) {
            remanentes[i]-=Integer.bitCount(this.bitMap[i]); //Guarda la posision inical
            System.out.println("contador: "+i+" remanente: "+remanentes[i]);

    }
        return remanentes;
    }
    /**
     * Genera el numero en binario que representa el numero de bloques que se va a almacenar.
     * Ejemplo: Si se necesitan 3 bloques genera un numero binario --> 111
     * numBlocks Numero de bloques que se van a guardar
     * Un entero que representa el binario generado
     */
    private String generateNumBinary(int numBlocks) //Generates the binary number of blocks needed by the process
    {
        StringBuilder binary = new StringBuilder();

        for (int i = 0; i < numBlocks; i++)
            binary.append(1);
        return binary.toString();

    }

    /**
     * Convierte el mapa de bits en una cadena
     * @return Una cadena que representa el mapa de bits
     */
    public String bitMapToString() {
        String formatString = "";
        int i = 1;
        for(int bit : bitMap)
        {
            StringBuilder sb = new StringBuilder(String.format("%31s",Integer.toBinaryString(bit)).replaceAll(" ", "0"));
            sb.reverse();
            formatString += sb.toString()  + " | ";
            if((i % 4) == 0)
            {
                formatString += "\n";
            }
            i++;
        }
        return formatString;
    }

}
