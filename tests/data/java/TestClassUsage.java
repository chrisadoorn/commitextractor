import java.util.ArrayList;

public class TestClassUsage {

    //instance declaratie
    private Thread t = new Thread();

    private Thread isResultaat() {
        return t;
    }

    public void isArgument(Thread th) {
        t = th;
    }

    public void isParameter(ArrayList<Thread> list)  {
        int i = list.size();
    }

    public void lokaalGedeclareerd(){
        Thread a = new Thread();
        a.run();
    }

}
