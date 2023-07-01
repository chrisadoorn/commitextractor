// import hoeft niet qua java, maar wel voor testen
import java.lang.Thread;

// extends
public class TestClassUsage extends Thread{

    //instance declaratie
    private Thread t = new Thread();

    private Thread isResultaat() {
        return t
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
        a = Thread();
    }

    public class innerClass<T extends Thread>{

    }

    public class innerClass2 extends Thread{

    }

}
