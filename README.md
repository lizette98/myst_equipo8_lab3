#Lab3: Behavioral Finance

## Description
En este proyecto se analizan los históricos del laboratorio 2 a partir de herramientas computacionales, 
en donde se analiza el desempeño de las operaciones realizadas personalmente
a lo largo del laboratorio pasado, donde se hicieron operaciones 
a través de Oanda con CFD's, para ahora analizar operaciones ganadoras y perdedoras, introduciendo el behavioral finance.

## Install dependencies

Install all the dependencies stated in the requirements.txt file, just run the following command in terminal:

        pip install -r requirements.txt
        
Or you can manually install one by one using the name and version in the file.

## Funcionalities

Un ejemplo de las funciones usadas en functions.py :

METRICAS DE ATRIBUCION AL DESEMPEÑO

Evolucion de capital en la cuenta de trading

    def f_profit_acm_d(param_data):
        """
        Funcion para agregar columna de evolución de capital.
    
        Parameters
        ----------
        param_data: DataFrame
                DataFrame que contiene la informacion de las operaciones en oanda actualizado.
    
        Returns
        -------
        param_data: DataFrame
                Dataframe actualizado con columna de evolución de capital inicializada con $100,000 Usd
                y se suma las ganancias o perdidas de la columna 'profit_acm'.
        """
    
        # Columna inicializada en $100,000 donde se le suma/resta el profit acumulado
        param_data['profit_acm_d'] = 100000 + param_data.profit_acm
    
        return param_data.copy()

## Authors
*Andrea Lizette Contreras González*
*Isamar Garcia Gomez*
*Erendira Marin Haro*

## License
**GNU General Public License v3.0** 

*Permissions of this strong copyleft license are conditioned on making available 
complete source code of licensed works and modifications, which include larger 
works using a licensed work, under the same license. Copyright and license notices 
must be preserved. Contributors provide an express grant of patent rights.*

## Contact
*For more information in reggards of this repo, please contact: Andrea Contreras  if708857@iteso.mx*
