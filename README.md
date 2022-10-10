# Trabajo 2 de Técnicas en Aprendizaje Estadístico de la UNAL-med 

## A cargo de:

- Esteban García Carmona
- Emilio Porras Mejía
- Felipe Miranda Arboleda
- José Luis Suárez Ledesma

## Introducción 
En el siguiente reporte técnico se busca crear un producto de trabajo que pueda predecir la probabilidad de que un individuo incumpla sus obligaciones financieras en los siguientes 12 meses a la fecha de originación de su crédito. La información se extrae de la base de datos del "Lending Club" estadounidense que contiene información financiera que data desde el 2007 hasta el 2014. Entre la información que trae, incluye el "default" que representa si la persona ha incumplido con sus obligaciones financieras. En EEUU esto sucede cuando se tiene un atraso de más de 30 días en su pago. 
Cuando en Datacrédito o instituciones similares analizan su credit score, lo hacen con los datos de su historial crediticio: préstamos, pagos, fechas, ingresos, entre otros. Por lo general, tan sólo le piden su número telefónico o cédula de ciudadanía, y ya con esto ingresan a la gran base de datos que comprende a todos los ciudadanos naturales que tienen historial crediticio. En cambio, nosotros utilizaremos los datos de la ya nombrada base de datos para crear un modelo de aprendizaje supervisado que según las 466284 columnas disponibles, busque acoplarlo a usted según los datos que ingrese en nuestra página web y decirle de acuerdo con sus características cuál es su scorecard y cómo se ve contra la población. 

# Problema
Para vivir sabroso en una sociedad contemporánea, se necesita capacidad de endeudamiento y obtención de préstamos. Inicialmente, las entidades bancarias podrían temer prestarle dinero a la mayoría de la población dada la posiblidad de que esta no pueda pagarle o no cumpla con los plazos establecidos entre sus obligaciones financieras. Tener una manera de predecir la probabilidad de que un individuo sea un buen prestador es indispensable, y abre los horizontes a poder ofrecerle a una mayor cantidad de personas el dinero que necesitan.
## Procedimiento
Inicialmente, el dataset de datos tiene 466283 filas y 74 columnas. Se empieza con el preprocesamiento:
1. Retiramos todas las columnas cuyos valores sean todos nulos. Con esto, terminamos con 57 columnas. 
2. Se eliminaron las columnas que no brindan información cuantitativa o analizable de cómo formular el scorecard. Así, se eliminaron variables de identificación al igual que las que representan fechas o cobros a futuro. Por ejempló, se elimino el zip code y la fecha del próximo pago del deudor.
3. Se utiliza la matriz de correlación para visualizar qué variables son similares entre ellas y eliminar las redundantes. El número de columnas resultante fue 36. La matriz se puede observar en la figura 1. 
#### FIGURA 1
4. A continuación se crea una nueva columna 'good_bad' que mantiene los datos "negativos", es decir, los que representan que se ha incumplido con las obligaciones financieras (moroso, cancelación, 'default', o no cumple las políticas de crédito). Se divide esta información que resta en dos: 80% para entrenamiento del modelo y 20% para su validación
5. Después, se empezó con la conversión de variables. Para las fechas, se utilizó métodos de expresiones regulares para cambiar formatos tales como '< 1 year' y convertirlo a valores que el módulo datetime de python pueda comprender. Se debe tener en cuenta que la "fecha de hoy" para el trabajo en cuestión. Es decir, se utiliza la fecha de '2020-08-01'.
6. Extraemos información importante para más adelante, la media de las variables "mths_since_issue_d", "mths_since_last_credit_pull_d".
7. Continuamos con el preprocesamiento, ahora eliminando valores utilizando el estadístico de chi cuadrado. Se calculó sobre cada columna el estadístico. Se calculó el estadístico F para hallar los p values correspondientes. Para evitar los problemas con los valores nulos, se reemplazaron temporalmente por la media de la columna. Al final, con la tabla obtenida, se eliminaron las variables recomendadas por el estadístico de F (es decir, con los menores puntajes) de nuestros datos de entrenamiento. Terminamos con 24 variables (columnas).
- En este punto, para poder desarrollar nuestro WoE (Weight of Evidence) y IV(Information Value) debemos crear variables "dummy" (variable imitación o maniquí) para cada una de las variables categóricas. Antes de continuar, veamos qué es cada una de estas.
  - Dummy: es una variable que se agrega para trabajar con variables categóricas. Lo que se hace, es que para cada posible "valor" que tenga la variable, creamos una nueva variable binaria. Por dar un ejemplo, si tenemos una columna de la forma



  |Índice| Humedad |
  | --- | --- |
  |1| alta |
  |2| media |
  |3| baja |
  se reemplaza por otra, tal que:

  |Índice| alta | media | baja| 
  | ---- | ---- | ---- | ---- |
  | 1 | 1    |   0  | 0  |
  | 2 | 0    |   1  | 0  |
  | 3 | 0   |   0  | 1  |

  - WoE (Weight of Evidence): El _peso de la evidencia_ es una medida de qué tanto la evidencia apoya (o no) una hipótesis. Con este, se mide el riesgo relativo de un atributo de nivel de _binning_.
  - Binning: Es una técnica de preprocesamiento de data que se usa para reducir los efectos menores de observación. El binning estadístico (Statistical data binning) es una manera de agrupar números continuos o semi-continuos en pequeños números que consideraremos _bins_. Podríamos tomar una variable que vaya desde 1 a 100 y dividirla en grupos de 20, entonces la primera variable tendría valores de 1-20, la segunda de 21-40 y así.
   - IV (Information Value): Es un método que ayuda a clasificar variables por su orden de importancia en un modelo predictivo. Se calcula con la siguiente fórmula:
  $IV = ∑ (\% of non-events - \% of events) * WOE$

8. One-hot encoding

# Conclusiones
no sé bro...


https://www.geeksforgeeks.org/convert-a-categorical-variable-into-dummy-variables/
https://towardsdatascience.com/how-to-develop-a-credit-risk-model-and-scorecard-91335fc01f03
https://www.investopedia.com/terms/f/forward-looking.asp
https://www.listendata.com/2019/08/credit-risk-modelling.html
https://documentation.sas.com/doc/en/vdmmlcdc/8.1/casstat/viyastat_binning_details02.htm
https://www.microscopyu.com/tutorials/ccd-signal-to-noise-ratio