#PROYECTO DE APLICACIÓN PROFESIONAL (PAP)

### 4J05 - OPTIMIZACIÓN DE PROGRAMAS DE INVERSIÓN EN INTERMEDIARIOS FINANCIEROS

## Description

El impacto de esta investigación va dirigida a contribuir e innovar el proceso de estrategias de inversión que realizan 
actualmente los fondos de pensión (AFORES) en México. Siendo el rendimiento un factor determinante para el retiro de 
futuras generaciones. 

Tomando en cuenta el contexto actual y recientes reformas en la materia, se ha convertido 
en una problemática de suma importancia hoy en día para nuestra sociedad.

## Install dependencies

Install all the dependencies stated in the requirements.txt file, just run the following command in terminal:

        pip install -r requirements.txt
        
Or you can manually install one by one using the name and version in the file.

## Funcionalities

Un ejemplo de las funciones usadas en functions.py :

Función para leer bases de datos

    def f_leer_archivo(param_archivo):
    """
    Funcion para leer el archivo de nuestras bases de datos

    Parameters
    ----------
    param_archivo: DataFrame
            Dataframe de un csv de los datos

    Returns
    -------
    param_archivo: DataFrame
            Dataframe de la base de datos que solicitemos
    """
    abspath = path.abspath(param_archivo)
    param_archivo = pd.read_csv(abspath)

    return param_archivo
## Author
*Erendira Marin Haro*

## License
**GNU General Public License v3.0** 

*Permissions of this strong copyleft license are conditioned on making available 
complete source code of licensed works and modifications, which include larger 
works using a licensed work, under the same license. Copyright and license notices 
must be preserved. Contributors provide an express grant of patent rights.*

## Contact
*For more information in reggards of this repo, please contact: Erendira Marin Haro  if705604@iteso.mx*
