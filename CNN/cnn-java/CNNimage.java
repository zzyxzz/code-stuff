// JAPVIC  -  Java Applet for the Visualisation of CNN Dynamics
// (c) 1997  Institute for Signal and Information Processing, ETHZ.
// written by Martin Haenggi
//
// CNNimage defines the input and output grids.

import java.awt.*;
import java.util.*;

public class CNNimage extends Panel 
{  
    static int max_size=50;
    int size;
    double boundary;
    public double pixel[][]=new double[max_size+2][max_size+2]; // grey-scale
    CNNcanvas canvas;

    int last_x=10000;
    int last_y=10000;
    int paintcntr;
    Button button1,button2,button3;
    Panel buttonpanel;

    public int sizex()
    { 
       return canvas.size().width;
    }

    public int sizey()
    {
      return canvas.size().height;
    }

    public int pixsizex()
    {
      return (sizex()-2)/size;
    }

    public int pixsizey()
    {
      return (sizey()-2)/size;
    }

    public void ClearImage()
    {
      int i,j; 
      for(i=0;i<=size+1;i++)
        for(j=0;j<=size+1;j++)
        if (((i>0) && (j>0)) && ((i<=size) && (j<=size)))
          pixel[i][j]=-1;
        else
          pixel[i][j]=boundary;
    }
  
    public CNNimage(int sz, double b, String s1, String s2, String s3)
    { 
      size=sz; boundary=b;
      this.setLayout(new BorderLayout(0,0));
      ClearImage();
      buttonpanel=new Panel();
      buttonpanel.setLayout(new GridLayout(1,3));
      button1=new Button(s1);
      button2=new Button(s2);
      button3=new Button(s3);
      buttonpanel.add(button1);
      buttonpanel.add(button2);
      buttonpanel.add(button3);
      this.add("North",buttonpanel);
      canvas=new CNNcanvas();
      this.add("Center",canvas);
    }

    public void paint(Graphics g)
    {
 
     int psizex=pixsizex();
     int psizey=pixsizey();
     button3.resize(1+size*psizex-button3.location().x,button3.size().height);
     Graphics canvas_g=canvas.getGraphics(); 

     float a,b,c; // colors
      int j;
      for (int i=0;i<size;i++)
       for (j=0;j<size;j++)
       {
         c=(float)((-pixel[i+1][j+1]+1)*0.5);
         a=c; b=c;
         if (c<0) { a=1; b=0; c=0; }
         if (c>1) { a=0; b=1; c=0; }
  
         canvas_g.setColor(new Color(a,b,c));

         canvas_g.fillRect(1+i*psizex,1+j*psizey,psizex-1,psizey-1);
       } 
      canvas_g.setColor(Color.blue);
      // Draw blue rectangle around the canvas's display area.
      canvas_g.drawRect(0,0,size*psizex,size*psizey);
    }

    public void update(Graphics g) {paint(g);}

    private void changepix(int x, int y, boolean drag)
    {
      int ix=(x-canvas.location().x-1)/pixsizex();
          ix=(ix<0)?0:((ix>size-1)?size-1:ix);
      int iy=(y-canvas.location().y-1)/pixsizey();
          iy=(iy<0)?0:((iy>size-1)?size-1:iy);
      if ((last_x!=ix) || (last_y!=iy) || !drag)
      {
        Graphics canvas_g=canvas.getGraphics();
        if (pixel[ix+1][iy+1]<0) 
           pixel[ix+1][iy+1]=1;
        else
        {
          canvas_g.setColor(Color.white);
          pixel[ix+1][iy+1]=-1;
        }
        last_x=ix; last_y=iy;
        canvas_g.fillRect(1+ix*pixsizex(),1+iy*pixsizey(),
           pixsizex()-1,pixsizey()-1);
        canvas_g.setColor(Color.black);
      }
 
    }

    public boolean mouseDown(Event e, int x, int y)
    {
      changepix(x,y,false);    
      return true;
    }

    public boolean mouseDrag(Event e, int x, int y)
    {
      changepix(x,y,true);
      return true;
    }
}




