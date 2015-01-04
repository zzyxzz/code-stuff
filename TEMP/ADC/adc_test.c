/************************************************************
*                ADC Demo Code using MPLAB C30              *
*************************************************************
*Author: X.Yang                                             *
*Date: 15/09/2011                                           *
*Intro: This file is used to test the ADC module of         *
*dsPIC30f2011 and demo or practise how to use ADC module.   *
*************************************************************/

#include <p30f2011.h>
#include <p30fxxxx.h>
#include <adc12.h>

/*Macros for Configuration Fuse Registers*/
_FOSC(CSW_FSCM_OFF & FRC);      //set up for internal Fast RC oscillator
_FWDT(WDT_OFF);                 //turn off the Watch-Dog Timer.
_FBORPOR(MCLR_DIS & PBOR_OFF & PWRT_OFF);  //Disable MCLR reset pin;brown-out rest off;turn off the power-up timers.
_FGS(CODE_PROT_OFF);            //code protection off

/************************************************************
*                 ADC Module Initialisation                 *
*************************************************************
* signed integer. Manual start saompling auto conversion.   *
* sampling time 1 Tad. Tad=1.5Tcy. system clock.                        *
*                                                           *
*************************************************************/ 

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
    ADCON3bits.SAMC = 1;     //12 Tad
        //A/D conversion clcok source bit
    ADCON3bits.ADRC = 0;      //clock derived from system clock
        //A/D conversion clock select bits
    ADCON3bits.ADCS = 2;      //Tad = 1.5*Tcy

    /*********ADCHS********/
        //MUX B multiplexer
    ADCHSbits.CH0NB = 0;
    ADCHSbits.CH0SB = 0;
        //MUX A multiplexer
    ADCHSbits.CH0NA = 0;     //channel 0 negtive input is Vref-;1--An1
    ADCHSbits.CH0SA = 2;     //channel 0 positive input is AN2
 
    /****Turn on AD Converter****/
    ADCON1bits.ADON = 1;
}

int main(void)
{       
    float adcresult = 0;
    float adcresultf = 0;
    TRISD = 0;                //PORTD setted as output
    ADC_init();
    //while(1)
    //{
        ADCON1bits.SAMP = 1;                 //manual start sampling
        while(!ADCON1bits.DONE);             //conversion done?
        adcresult  = ADCBUF0;                //read ADC buffer0
        adcresultf = adcresult*0.001221;     //get real voltage value
        if(adcresultf > 3.0)                 //give a high to PORTD when sampled voltage is above 3.0v 
            LATD = 1;
    //}  
    return(0);
}      
