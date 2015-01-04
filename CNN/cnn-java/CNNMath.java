// JAPVIC  -  Java Applet for the Visualisation of CNN Dynamics
// (c) 1997  Institute for Signal and Information Processing, ETHZ.
// written by Martin Haenggi
//
// CNNMath does the CNN integration.

import java.util.*;
import java.lang.*;

public class CNNMath extends Object
{
    public double step=0.1;
    public int max_size=50;
    public int size;
    public double t;
    public double U[][]=new double[max_size+2][max_size+2];
    public double X[][]=new double[max_size+2][max_size+2];
    public double Y[][]=new double[max_size+2][max_size+2];
    private static int xoffs[]={-1,0,1,-1,0,1,-1,0,1};
    private static int yoffs[]={-1,-1,-1,0,0,0,1,1,1};
    Template Atempl,Btempl;
    CNNimage input,output;
    double I,boundary;
    int Xinit;
    boolean CNNstop=false,CNNsuspended=false;
    Thread CNNthread;

  public CNNMath(int sz, double b,Template A, Template B, double z, 
      CNNimage ipic, CNNimage opic, int Initx, Thread T)
    {
      size=sz; boundary=b;
      Atempl=A; Btempl=B;
      input=ipic; output=opic;
      I=z;
      Xinit=Initx;
      CNNthread=T;
    }

    public static double PWL(double q)
    {
     return (q<-1.0)?-1.0:((q>1)?1.0:q);
    }

    public double foldA(int xp, int yp)  // fold using A template
    {
      double s=0.0;
      for(int i=0;i<9;i++) 
         s+=Y[xp+xoffs[i]][yp+yoffs[i]]*Atempl.v[yoffs[i]+1][xoffs[i]+1];
      return s;
    }

    public double foldB(int xp, int yp)  // fold using B template
    {
      double s=0.0;
      for(int i=0;i<9;i++) 
         s+=U[xp+xoffs[i]][yp+yoffs[i]]*Btempl.v[yoffs[i]+1][xoffs[i]+1];
      return s;
    }

  public void integrate()  // Euler
  {
    X=output.pixel; U=input.pixel;
    double b,d=0;
   
    b=(Xinit==2)?-1.0:((double)Xinit); // Initial Condition for X
    int i,j;
    for(i=0;i<=size+1;i++)
      for(j=0;j<=size+1;j++)
	if (((i>0) && (j>0)) && ((i<=size) && (j<=size)))
        {
          X[i][j]=((Xinit==3)?U[i][j]:b);
          Y[i][j]=PWL(X[i][j]);
        }
       else Y[i][j]=X[i][j];  // x boundary is already set
       
    t=0;
    while (!CNNstop)
    {
      for(i=1;i<=size;i++)  // Calculate new x values
        for(j=1;j<=size;j++)
        {
          d=-X[i][j]+foldA(i,j)+foldB(i,j)+I;  // CNN Equation
          X[i][j]+=step*d; // Euler 1st
        }
      t+=step;
      output.paint(output.canvas.getGraphics());
      for(i=1;i<=size;i++)  //  calculate new y
        for(j=1;j<=size;j++)     
          Y[i][j]=PWL(X[i][j]);
      while (CNNsuspended) 
      { try { CNNthread.sleep(100); }
        catch (InterruptedException e) {}
      }
    }
    output.pixel=Y;
    output.paint(output.canvas.getGraphics());
  }  

}
