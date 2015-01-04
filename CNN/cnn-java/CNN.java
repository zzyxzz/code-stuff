// JAPVIC  -  Java Applet for the Visualisation of CNN Dynamics
// (c) 1997  Institute for Signal and Information Processing, ETHZ.
// written by Martin Haenggi
//
// Main class

import java.awt.*;
import java.util.*;
import java.applet.*;

public class CNN extends Applet implements Runnable
{  
  int max_size=50, size=16;
  double boundary=0;
  CNNimage input,output;
  Button clear_button;
  TextArea textarea;
  Button StartButton,SuspendButton,ResumeButton,StopButton;
  Template Atempl,Btempl;
  CNNMath Calc;
  TextField Ivalue;
  Choice TemplChoice,InitCond;
  public double I;
  GridBagLayout gridbag=new GridBagLayout();
  Panel panel1,panel2,panel3,Ipanel;
  private Thread CNNanimator=null;
  boolean first=true;
  Label outLabel;
  String msgStr;

  static double Atemplates[][][]=
   {{{0,0,0},{0,0,0},{0,0,0}},
    {{0,0,0},{0,1,0},{0,0,0}},
    {{0,0,0},{0,1.5,0},{0,0,0}},
    {{0,0,0},{0,2,0},{0,0,0}},
    {{0,0,0},{1,2,1},{0,0,0}},
    {{0,1,0},{1,2,1},{0,1,0}},
    {{0,0,0},{0,2,2},{0,0,0}},
    {{0,1,0},{1,2,1},{0,1,0}},
    {{0,0,0},{1,2,-1},{0,0,0}},
    {{0,2,0},{2,3,2},{0,2,0}}};
 
  static double Btemplates[][][]=
   {{{0,0,0},{0,0,0},{0,0,0}},
    {{0,0,0},{0,-2,0},{0,0,0}},
    {{0,-2,0},{-2,8,-2},{0,-2,0}},
    {{-1,-1,-1},{-1,8,-1},{-1,-1,-1}},
    {{0,0,0},{0,0,0},{0,0,0}},
    {{0,0,0},{0,0,0},{0,0,0}},
    {{0,0,0},{0,2,0},{0,0,0}},
    {{0,0,0},{0,4,0},{0,0,0}},
    {{0,0,0},{0,0,0},{0,0,0}},
    {{0,-2,0},{-2,0,-2},{0,-2,0}}};

  static double ConstI[]={0,0,-1,-8.5,-1,-1,0,-1,0,0};

  static int InitStates[]={0,0,0,3,3,3,1,1,3,3};

  public void init () 
  {
    String sizeStr=getParameter("SIZE");
    if (sizeStr!=null) {
             try {
                 size=Integer.parseInt(sizeStr);
             } catch (NumberFormatException e) {
                 // Use default size.
             }
    }
    if (size>max_size) size=max_size;
    String boundaryStr=getParameter("BOUNDARY");
    boundary=Str2double(boundaryStr);
    if (boundary>1) boundary=1; else if (boundary<-1) boundary=-1;
    msgStr=" Size: "+size+"  Boundary: "+boundary;
    showStatus(msgStr);
    msgStr=msgStr+"  -- ";
 
    this.setBackground(Color.lightGray);
    this.setLayout(gridbag);

    input=new  CNNimage(size,boundary," White "," Invert ","Black ");
    output=new CNNimage(size,boundary,"State","Output","Copy");
    TemplChoice=new Choice();
    TemplChoice.addItem("Manual Input");
    TemplChoice.addItem("Logic NOT");
    TemplChoice.addItem("Edge Extraction");
    TemplChoice.addItem("Convex Corner Extraction");
    TemplChoice.addItem("Horizontal Line Detection");
    TemplChoice.addItem("Noise Removal");
    TemplChoice.addItem("Shadowing");
    TemplChoice.addItem("Hole Filling");
    TemplChoice.addItem("Connected Component Detection");
    TemplChoice.addItem("Global Connectivity Detection");
    InitCond=new Choice();
    InitCond.addItem("X =  0"); 
    InitCond.addItem("X = +1");
    InitCond.addItem("X = -1");
    InitCond.addItem("X = Input");
    Atempl=new Template();
    Btempl=new Template();
    Ivalue=new TextField("0",4);
    StartButton=new Button("Start");
    SuspendButton=new Button(" Suspend "); SuspendButton.disable();
    ResumeButton=new Button("Resume"); ResumeButton.disable();
    StopButton=new Button("Stop"); StopButton.disable();

    panel1=new Panel();
    panel1.setLayout(gridbag);

    constrain(panel1,new Label("Input"),0,0,2,1);
    constrain(panel1,input,0,1,2,1,GridBagConstraints.BOTH,
      GridBagConstraints.CENTER,1.0,1.0,0,4,4,4);
    outLabel=new Label("CNN Output/State");
    constrain(panel1,outLabel,2,0,2,1);
    constrain(panel1,output,2,1,2,1,GridBagConstraints.BOTH,
      GridBagConstraints.CENTER,1.0,1.0,0,4,4,4);

    panel2=new Panel();
    panel2.setLayout(gridbag);

    Ipanel=new Panel();
    Ipanel.setLayout(new FlowLayout());
    Ipanel.add(new Label("I="));
    Ipanel.add(Ivalue);

    panel3=new Panel();
    panel3.setLayout(new GridLayout(4,1));
    panel3.add(StartButton);
    panel3.add(SuspendButton);
    panel3.add(ResumeButton);
    panel3.add(StopButton);

    constrain(panel2,new Label("Choose Template:"),0,0,1,1);
    constrain(panel2,TemplChoice,0,1,2,1);
    constrain(panel2,new Label("Initial Cell State: "),2,0,1,1,
      GridBagConstraints.NONE,
      GridBagConstraints.CENTER,0,0,5,15,0,0);
    constrain(panel2,InitCond,2,1,1,1,GridBagConstraints.NONE,
      GridBagConstraints.CENTER,0,0,5,6,0,0);
    constrain(panel2,new Label("A Template:"),0,2,1,1);
    constrain(panel2,Atempl,0,3,1,1,GridBagConstraints.NONE,
      GridBagConstraints.CENTER,0,0,0,0,0,8);
    constrain(panel2,new Label("  B Template:"),1,2,1,1);
    constrain(panel2,Btempl,1,3,1,1,GridBagConstraints.NONE,
      GridBagConstraints.CENTER,0,0,0,8,0,0);
    constrain(panel2,Ipanel,2,3,1,1);
    constrain(panel2,panel3,3,1,1,3,GridBagConstraints.VERTICAL,
        GridBagConstraints.EAST,0,0,0,20,0,0);

    this.setLayout(gridbag);
    constrain(this,panel1,0,0,1,1,GridBagConstraints.BOTH,
      GridBagConstraints.CENTER,1.0,1.0,8,4,4,4);
    constrain(this,panel2,0,1,1,1,GridBagConstraints.HORIZONTAL,
      GridBagConstraints.CENTER,1.0,0.0,4,4,8,4);
    output.button1.disable();
    output.button2.disable();
    output.button3.disable();
    showStatus(msgStr+" Ready.");
  }

  public void paint(Graphics g)
  {
    input.paint(input.getGraphics());
    output.paint(output.getGraphics());
  }

  public double Str2double (String s)
  {   
    Double dobj=new Double(0);
    if (s!=null) {
         try {
             dobj=(Double.valueOf(s));
         } catch (NumberFormatException e) {
             // Use 0 as default value
         }
  }
  return dobj.doubleValue();
  }

  public boolean mouseDown(Event e, int x, int y)
  {
     return false;
  }

  public boolean mouseUp(Event e, int x, int y)
  {
     return false;
  }
  
  // override reshape to avoid canvas clear:
  public synchronized void reshape(int x, int y, int width, int height)
  {
    super.reshape(x,y,width,height);
  }

  public void start()
  {
    if ((CNNanimator==null) && (!first)) 
    { 
      CNNanimator=new Thread(this);
      CNNanimator.start();
      StartButton.disable();
      SuspendButton.enable();
      StopButton.enable();
    }
  }

  public void stop()
  { 
    if (CNNanimator!=null) 
    {  
      
      Calc.CNNstop=true;
      String tS=new String(Double.toString(0.0001+Calc.t));
       showStatus(msgStr+"Integration stopped at t="+
         tS.substring(0,tS.indexOf(".")+2));
      if (ResumeButton.isEnabled()) 
      {  
        ResumeButton.disable();
        Calc.CNNsuspended=false;
      }
    }
    first=true;
    StartButton.enable();
    StopButton.disable();
    SuspendButton.disable();
  }
 
  public void suspend()
  {

    if (CNNanimator!=null)
    { 
       Calc.CNNsuspended=true;
       ResumeButton.enable();
       String tS=new String(Double.toString(0.0001+Calc.t));
       showStatus(msgStr+"Integration suspended at t="+
         tS.substring(0,tS.indexOf(".")+2));
    }
    SuspendButton.disable();

  }

  public void resume()
  {
    if (CNNanimator!=null) 
    {
      Calc.CNNsuspended=false;
      SuspendButton.enable();
    }
    showStatus(msgStr+"Integrating...");
    ResumeButton.disable();
  }

  public void setEditableTempl(boolean editable)
  {  
    int i,j;
    Ivalue.setEditable(editable);
    for(i=0;i<3;i++)
      for(j=0;j<3;j++)
      {
        Atempl.vfield[i][j].setEditable(editable);
        Btempl.vfield[i][j].setEditable(editable);
      }
  }
    
  public boolean action(Event e, Object arg)
  {
    if (e.target==StartButton)
    { 
      first=false;
      TemplChoice.disable();
      setEditableTempl(false);
      start();
      return true;  
    }
    else if (e.target==SuspendButton)
    {
      suspend();
      TemplChoice.enable();
      setEditableTempl(TemplChoice.getSelectedIndex()==0);
      return true;
    }
    else if (e.target==ResumeButton)
    {
      TemplChoice.disable();
      setEditableTempl(false);
      Atempl.getValues(); Btempl.getValues();
      I=Str2double(Ivalue.getText());
      Calc.I=I;
      resume();
      return true;
    }
    else if (e.target==StopButton)
    {
      stop();
      TemplChoice.enable();
      setEditableTempl(TemplChoice.getSelectedIndex()==0);
      return true;
    }  
    else if (e.target==input.button1)  // white
    {
      input.ClearImage();
      input.paint(input.getGraphics());
      return true;
    }
    else if (e.target==input.button2)  // invert
    {  
      int i,j;
      for(i=1;i<=size;i++)
        for(j=1;j<=size;j++)
          input.pixel[i][j]=-input.pixel[i][j];
      input.paint(input.getGraphics());
      return true;
    }
    else if (e.target==input.button3)  // black
    {
      int i,j;
      for(i=1;i<=size;i++)
        for(j=1;j<=size;j++)
          input.pixel[i][j]=1.0;
      input.paint(input.getGraphics());
      return true;
    }
    else if (e.target==output.button1)  // state
    {
      output.button1.disable();
      outLabel.setText("     CNN State");
      output.pixel=Calc.X;
      output.paint(output.getGraphics());
      output.button2.enable();
      return true;
    }
    else if (e.target==output.button2) // output
    {
      output.button2.disable();
      outLabel.setText("     CNN Output");
      output.pixel=Calc.Y;
      output.paint(output.getGraphics());
      output.button1.enable();
      return true;
    }
    else if (e.target==output.button3) // Copy
    {
      int i,j;
      for(i=1;i<=size;i++)
        for(j=1;j<=size;j++)
          input.pixel[i][j]=Calc.Y[i][j];
      input.paint(input.getGraphics());
      return true;
    }
    else if (e.target==TemplChoice)
    { 
      int i,j;   
      int sel=TemplChoice.getSelectedIndex();
      // Template fields may only be edited when in "manual" mode
      boolean editable=(sel==0);
      setEditableTempl(editable);
      if (!editable)  // read template values from const array
      {
      InitCond.select(InitCond.getItem(InitStates[sel]));
      InitCond.disable(); // no further changes allowed
      Ivalue.setText(Double.toString(ConstI[sel]));
      for(i=0;i<3;i++)
        for(j=0;j<3;j++)
        {
          Atempl.vfield[i][j].setText(Double.toString(Atemplates[sel][i][j]));
          Btempl.vfield[i][j].setText(Double.toString(Btemplates[sel][i][j]));
        }
      }
      else InitCond.enable(); // re-allow changes
      return true;
    }
    else  return false;
  }  

  public void run()
  { 
    showStatus(msgStr+"Integrating...");
    outLabel.setText("     CNN State");
    output.button1.disable();
    output.button2.enable();
    output.button3.enable();
    Btempl.getValues(); Atempl.getValues();
    I=Str2double(Ivalue.getText());
    Calc=new CNNMath(size,boundary,Atempl,Btempl,I,input,output,
       InitCond.getSelectedIndex(),CNNanimator);
    Calc.CNNstop=false; Calc.CNNsuspended=false;
    Calc.integrate();
    stop();
    CNNanimator=null;
    outLabel.setText("     CNN Output");
    output.button2.disable();
    output.button1.enable();
  }

  public void constrain(Container container, Component component,
    int grid_x, int grid_y, int grid_width, int grid_height,
    int fill, int anchor, double weight_x, double weight_y,
    int top, int left, int bottom, int right)
  {
    GridBagConstraints c=new GridBagConstraints();
    c.gridx=grid_x; c.gridy=grid_y;
    c.gridwidth=grid_width; c.gridheight=grid_height;
    c.fill=fill; c.anchor=anchor;
    c.weightx=weight_x; c.weighty=weight_y;
    if (bottom+top+right+left>0)
      c.insets=new Insets(top,left,bottom,right);
    ((GridBagLayout)container.getLayout()).setConstraints(component,c);
    container.add(component);
  }

  public void constrain(Container container, Component component,
    int grid_x, int grid_y, int grid_width, int grid_height)
  {
    constrain(container, component, grid_x, grid_y, grid_width,
       grid_height, GridBagConstraints.NONE,GridBagConstraints.CENTER,
       0.0,0.0,5,0,0,0);
  }  
}
