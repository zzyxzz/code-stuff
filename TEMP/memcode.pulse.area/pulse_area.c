#include <p30fxxxx.h>
#include <p30f2011.h>
#include <spi.h>

/*Macros for Configuration Fuse Registers*/
_FOSC(CSW_FSCM_OFF & FRC);      //set up for internal Fast RC oscillator
_FWDT(WDT_OFF);                 //turn off the Watch-Dog Timer.
_FBORPOR(MCLR_EN & PBOR_OFF & PWRT_OFF);  //enable MCLR reset pin;brown-out rest off;turn off the power-up timers.
_FGS(CODE_PROT_OFF);            //code protection off

//#define THR 3.0            //threshold 2457->3V
//#define ADELAY 0.01      //area delay 2v*0.001s*5
#define RMIN 16            //resistance value 625 ohm of POT
#define RMAX 256           //resistance value 10k of POT
#define MODE00 1           //four modes could be used: MODE00; MODE01; MODE10; MODE11

void Rtrans(unsigned int spivalue);
void SPI_init(void);
void timer(void);

int main(void)
{   
    //initialisation
    SPI_init();                  //initialise SPI
    timer();                     //initialise TIMER
    //set PORT
    TRISD = 0;                   //PORTD as output
    LATD = 1;                    //set PORTD 1
    unsigned int Rm = 192;
    Rtrans(RMAX);//---------------

     
    while(1)
    {   
        T1CONbits.TON = 1;                   //Timer1 on
        while(IFS0bits.T1IF)                 //if flag == 1
        {
            if(TMR1==PR1&&Rm>=64)
               {
	               Rtrans(Rm);
                   Rm-=64;
			   }
            IFS0bits.T1IF = 0;              //clear timer interrupt flag
        } 
    }
    return(0);
}

void Rtrans(unsigned int spivalue)
{ 
    LATD = 0;                        //CS,POT enable
    //WriteSPI1(0x2);                //memory address of POT
    //WriteSPI1(0x0);                //command bits as write mode
    WriteSPI1(spivalue);             //write resistance value of POT
    while(SPI1STATbits.SPITBF);      //transmit done?
    while(!SPI1STATbits.SPIRBF);     //receive complete,ready for reading?
    spivalue = ReadSPI1();           //read
    Nop();
    Nop();
    LATD = 1;                       //CS,POT disable
}

void timer(void)              //16 bit timer TGATE enable
{   
    TMR1  = 0;                      //Clear Timer1 register
    T1CONbits.TON = 0;              //Timer1 off
    T1CONbits.TSIDL = 0;            //Stop in idle mode; 0--no
    T1CONbits.TGATE = 1;            //Timer Gated Time Accumulation Enable
    T1CONbits.TCKPS = 0;            //Timer Input Clock Prescale; 00--1:1; 01--1:8; 10--1:64; 11--1:256
    T1CONbits.TSYNC = 0;            //Timer External Clock Input Synchronization; no
    T1CONbits.TCS = 0;              //Timer Clock Source; internal(Fosc/4); 0--internal
    
    IFS0bits.T1IF = 0;              //clear timer interrupt flag
    IEC0bits.T1IE = 0;              //interrupt disable
    PR1=5;                     //period register
}


void SPI_init(void)
{
    /* following code snippet shows SPI register configuration for MASTER mode*/
    IFS0bits.SPI1IF = 0;             //clear the Interrupt Flag
    IEC0bits.SPI1IE = 0;             //disable the Interrupt
    /* SPI1STAT Register Settings*/
    SPI1STATbits.SPISIDL = 0;        //continue in idle mode
    SPI1STATbits.SPIROV  = 0;        //clear receive overflow flag
    /* SPI1CON register setings*/
    SPI1CONbits.FRMEN  = 0;          //framed SPI support disable
    SPI1CONbits.SPIFSD = 0;          //frame sync pulse output(master)
    SPI1CONbits.DISSDO = 0;          //SDOx pin is controlled by the module.
    SPI1CONbits.MODE16 = 1;          //communication is word-wide (16 bits).
    SPI1CONbits.SMP = 0;             //input Data is sampled at the middle of data output time.
    #if defined MODE00
        /*active state for clock is high, idle state for clock is low*/
        SPI1CONbits.CKP = 0;
        /*output data changes on transition from active to idle clock state*/
        SPI1CONbits.CKE = 1;        
    #elif defined MODE01
        /*active state is high, idle state is low*/
        SPI1CONbits.CKP = 0;
        /*output data changes on trasition from idle to active clock state*/
        SPI1CONbits.CKE = 0;
    #elif defined MODE10
        /*active state is low, idle state is high*/
        SPI1CONbits.CKP = 1;
        /*output data changes on transition from active to idle clock state*/
        SPI1CONbits.CKE = 1;
    #elif defined MODE11
        /*active state is low, idle state is high*/
        SPI1CONbits.CKP = 1;
        /*output data changes on transition from idle to active clock state*/
        SPI1CONbits.CKE = 0;
    #endif
    SPI1CONbits.SSEN   = 0;          //slave select disable
    SPI1CONbits.MSTEN  = 1;          //master mode enabled
    SPI1CONbits.SPRE   = 0;          //secondary prescale 8:1
    SPI1CONbits.PPRE   = 0;          //primary prescale 64:1
    SPI1STATbits.SPIEN = 1;          //enable SPI module
}
