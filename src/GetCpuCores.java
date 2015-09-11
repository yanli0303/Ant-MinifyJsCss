import org.apache.tools.ant.Task;

public class GetCpuCores extends Task {
    private String outputProperty;

    public void execute() {
        int cores = Runtime.getRuntime().availableProcessors();
        getProject().setNewProperty(outputProperty, Integer.toString(cores));
    }

    public void setOutputProperty(String prop) { outputProperty = prop; }
}
