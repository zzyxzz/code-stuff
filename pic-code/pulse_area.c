#include <p30fxxxx.h>
#include <p30f2011.h>
#include <spi.h>

/*Macros for Configuration Fuse Registers*/
_FOSC(CSW_FSCM_OFF & FRC);      //set up for internal Fast RC oscillator
_FWDT(WDT_OFF);                 //turn off the Watch-Dog Timer.
_FBORPOR(MCLR_EN & PBOR_OFF & PWRT_OFF);  //Disable MCLR reset pin;brown-out rest off;turn off the power-up timers.
_FGS(CODE_PROT_OFF);            //code protection off

#define THR 2.0           //threshold 2457->3V
#define RMIN 16            //resistance value 625 ohm of POT
#define RMID 128           //resistance value 5K
#define RMAX 256          //resistance value 10k of POT
#define MODE00 1          //four modes could be used: MODE00; MODE01; MODE10; MODE11

void Rtrans(unsigned int spivalue);
void SPI_init(void);
void timer(void);
void ADC_init(void);

int main(void)
{   
    unsigned int adcresult;
    float adcresultf;
    unsigned int num = 0;
    ADC_init();                  //initialise ADC
    SPI_init();                  //initialise SPI
    TRISD = 0;                   //PORTD as output
    LATD = 1;                    //set PORTD high
     
    while(1)
    {   
        Rtrans(RMID);

        ADCON1bits.SAMP = 1;                 //manual start sampling
        while(!ADCON1bits.DONE);             //conversion done?
        adcresult = ADCBUF0;                 //read ADC buffer0
        adcresultf = adcresult*0.001221;     //get real voltage value
         
        if(adcresultf > THR)
        {
           Rtrans(RMAX);
        }
        else if(adcresult> 1.0)
        {
            Rtrans(RMIN);
        }
        else
        {
            Rtrans(RMID);
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

void timer(void) 
{   
    TMR1  = 0;                      //Clear Timer1 register
    T1CON = 0x0000;                 //clear timer control register
    IFS0bits.T1IF = 0;              //clear timer interrupt flag
    IEC0bits.T1IE = 0;              //interrupt disable
    PR1=0x00FF;                     //period register
    T1CONbits.TON = 0;              //turn off timer1
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

void ADC_init(void)
{
    /*Manual sampling start and automatic converting start after 12Tad*/
    IFS0bits.ADIF = 0;        //clear AD interrupt flag
    IEC0bits.ADIE = 0;        //disable AD interrupt
    ADPCFG = 0xFFFB;          //RB2=analog
    ADCSSL = 0x0000;          //No scanning

    /********ADCON1********/
    ADCON1bits.ADSIDL = 0;    //continue module operation in idle mode
        //data output format bits
    ADCON1bits.FORM = 1;      //11--signed fraction;10--fraction;01--signed integer;00--integer
        //conversion trigger source select bits
    ADCON1bits.SSRC = 7;      //integer counter ends sampling and starts conversion(auto convert)
    ADCON1bits.ASAM = 0;      //sampling begins when SAMP bit set
        //A/D sample enable bit
    ADCON1bits.SAMP = 0;      //0--A/D sample/hold amplifers are holding;1--start sampling
    //ADCON1bits.DONE--------A/D conversion status bit; 1---conversion done

    /********ADCON2********/
        //voltage reference configuration bits
    ADCON2bits.VCFG = 0;      //;000--AVdd&AVss(internal High/Low Vref)
    ADCON2bits.CSCNA = 0;     //do not scan inputs
    //ADCON2bits.BUFS--------buffer fill status bit
    ADCON2bits.SMPI = 0;      //interrupts at the completion of conversion for each sample/convert sequence
        //buffer mode select bit
    ADCON2bits.BUFM = 0;      //0--configured as one 16-word buffer ADCBUF(15...0)
        //Alternate input sample mode select bit
    ADCON2bits.ALTS = 0;      //always use MUXA input multiplexer settings

    /********ADCON3********/
        //auto sample time bits
    ADCON3bits.SAMC = 1;      //12 Tad
        //A/D conversion clcok source bit
    ADCON3bits.ADRC = 0;      //clock derived from system clock
        //A/D conversion clock select bits
    ADCON3bits.ADCS = 2;      //Tad = 1.5*Tcy

    /*********ADCHS********/
        //MUX B multiplexer
    ADCHSbits.CH0NB = 0;
    ADCHSbits.CH0SB = 0;
        //MUX A multiplexer
    ADCHSbits.CH0NA = 0;      //channel 0 negtive input is Vref-;1--AN1
    ADCHSbits.CH0SA = 2;      //channel 0 positive input is AN2
 
    /****Turn on AD Converter****/
    ADCON1bits.ADON = 1;
}
