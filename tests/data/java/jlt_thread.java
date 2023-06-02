public class jlt_thread {

    //instance declaratie
    private Thread t = new Thread();

    private Thread isResultaat() {
        return t;
    }

    public void isArgument(Thread th) {
        t = th;
    }

    public void lokaalGedeclareerd(){
        Thread a = new Thread();
        a.run();
    }
}
