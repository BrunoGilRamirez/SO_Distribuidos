package Mbit;

public class segmento {
    private int size;
    private int index;
    private int[] start = new int[2]; //Posicion en el mapa de bits y numero de entero en el mapa de bits
    public segmento(int size, int index) {
        this.size = size;
        this.index = index;
        
    }
    public int getSize() {
        return size;
    }
    public void setSize(int size) {
        this.size = size;
    }
    public int[] getStart() {
        return start;
    }
    public void setStart(int[] start) {
        this.start = start;
    }
    public int getIndex() {
        return index;
    }
}
