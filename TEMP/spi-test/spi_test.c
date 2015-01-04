/***************************************************************
*                 SPI Demo Code Using C30                      *
****************************************************************
* Author: X. Yang                                              *
* Date: 13/09/2011                                             *
* Intro: This code is used to test C codes of SPI communiction *
*        and as a practice or demo of dsPIC30f2011.            *
***************************************************************/

#include <p30f2011.h>
#include <p30fxxxx.h>
#include <spi.h>
#define MODE00   //four modes could be used: MODE00; MODE01; MODE10; MODE11

/*Macros for Configuration Fuse Registers*/
_FOSC(CSW_FSCM_OFF & FRC);      //set up for internal Fast RC oscillator
_FWDT(WDT_OFF);                 //turn off the Watch-Dog Timer.
_FBORPOR(MCLR_DIS & PBOR_OFF & PWRT_OFF);  //Disable MCLR reset pin;brown-out rest off;turn off the power-up timers.
_FGS(CODE_PROT_OFF);            //code protection off


/**************************************************************
*                      SPI initialisation                     *
***************************************************************
*  |SPI Mode:   CKP:    CKE:|   In this demo we use mode(0,0) *
*  | (0,0)       0       1  |   which means CKP=0; CKE=1      *
*  | (0,1)       0       0  |   No interrupt                  *
*  | (1,0)       1       1  |   16-bit mode communication     *
*  | (1,1)       1       0  |   Mater mode                    *
*  |________________________|                                 *
**************************************************************/

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

//void SpiWrite(unsigned int Data)
//{  
//   unsigned int dump;
    // send the data byte
//   SPI1BUF = Data;
//   while(SPI1STATbits.SPITBF);
    // wait for a data byte reception
//   SPI1STATbits.SPIROV = 0;
//   while(!SPI1STATbits.SPIRBF);
//   dump = SPI1BUF;
//   Nop();
//   Nop();
//} 

int main(void)
{
    int spivalue;
    SPI_init();
//    while(1)
//        {
            WriteSPI1(0x11);               //write data to SPI bus
            while(SPI1STATbits.SPITBF);    //transmit done?
            while(!SPI1STATbits.SPIRBF);   //receive complete,ready for reading?
            spivalue = ReadSPI1();         //read
            Nop();
            Nop();
//        }
    return(0);
}
