// JAPVIC  -  Java Applet for the Visualisation of CNN Dynamics
// (c) 1997  Institute for Signal and Information Processing, ETHZ.
// written by Martin Haenggi
//
// Template defines the template objects.

import java.awt.*;
import java.util.*;
import java.lang.*;

public class Template extends Panel 
{  
    static int field_width=3;
    public double v[][]={{0,0,0},{0,0,0},{0,0,0}};
    TextField vfield[][]=new TextField[3][3];
   
    public Template()
    { 
      String initstr="0";
      this.setLayout(new GridLayout(3,3));
      int i,j;
      for(i=0;i<3;i++)
        for(j=0;j<3;j++)  // Attention: 1st index=vertical direction 
          {
           vfield[i][j]=new TextField(initstr,field_width);
           this.add(vfield[i][j]);
          }
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

    public void getValues()
    {
      int i,j;
      for(i=0;i<3;i++)
        for(j=0;j<3;j++)        
           v[i][j]=Str2double(vfield[i][j].getText());
    }     

}
