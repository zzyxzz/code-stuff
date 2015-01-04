#include<p30fxxxx.h>
#include<p30f2011.h>

/*Macros for Configuration Fuse Registers*/
_FOSC(CSW_FSCM_OFF & FRC);      //set up for internal Fast RC oscillator
_FWDT(WDT_OFF);                 //turn off the Watch-Dog Timer.
_FBORPOR(MCLR_DIS & PBOR_OFF & PWRT_OFF);  //Disable MCLR reset pin;brown-out rest off;turn off the power-up timers.
_FGS(CODE_PROT_OFF);            //code protection off

void timer_init(void) 
{   
    TMR1  = 0;                     //Clear Timer1 register
    T1CON = 0x0000;                //clear timer control register
    IFS0bits.T1IF = 0;             //clear timer interrupt flag
    IEC0bits.T1IE = 0;             //interrupt disable
    PR1=0x400;                    //period register
    T1CONbits.TON = 0;             //turn off timer1
}

int main(void)
{    
    TRISC = 0;                       //set portC output
    LATCbits.LATC13 = 0;             //search signal
    LATCbits.LATC14 = 0;             //data signal
    
    TRISD = 0;
    LATD = 0;                         //reset signal
    
    timer_init();
    
    while(1)
    {   
        //LATCbits.LATC14 = 0;       //set data pin 0
        
        T1CONbits.TON = 1;         //Start timer1
        while(!IFS0bits.T1IF);     //TMR equals PR1?
        IFS0bits.T1IF = 0;         //clear timer interrupt flag
        T1CONbits.TON = 0;         //turn off timer1
        
        LATCbits.LATC13 = 1;       //set search pin 1
        
        T1CONbits.TON = 1;         //Start timer1
        while(!IFS0bits.T1IF);     //TMR equals PR1?
        IFS0bits.T1IF = 0;         //clear timer interrupt flag
        T1CONbits.TON = 0;         //turn off timer1
        
        LATCbits.LATC13 =0;
        
        T1CONbits.TON = 1;         //Start timer1
        while(!IFS0bits.T1IF);     //TMR equals PR1?
        IFS0bits.T1IF = 0;         //clear timer interrupt flag
        T1CONbits.TON = 0;         //turn off timer1
        
        LATD = 1;        //reset memristor
        
        
        PR1 = 0x200;
        T1CONbits.TON = 1;         //Start timer1
        while(!IFS0bits.T1IF);     //TMR equals PR1?
        IFS0bits.T1IF = 0;         //clear timer interrupt flag
        T1CONbits.TON = 0;         //turn off timer1
        
        
        LATD = 0;
           
    }
    return(0);
    
} 