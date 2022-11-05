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
3. Se utiliza la matriz de correlación para visualizar qué variables son similares entre ellas y eliminar las redundantes. El número de columnas resultante fue 36. La matriz se puede observar en la Figura 1. Al eliminar las correspondientes columnas, se obtiene la Figura 2 que representa la matriz de correlación depurada. 

<img src="/DataFramesYutiles/matriz_corr_tot_variables.png" alt="matriz_corr_tot_variables" title="matriz_corr_tot_variables">

**Figura 1:** *Matriz de correlación sin depurar*

<img src="/DataFramesYutiles/matriz_corr_depurada.png" alt="matriz_corr_depurada" title="matriz_corr_depurada">

**Figura 2:** *Matriz de correlación depurada*


4. A continuación se crea una nueva columna 'good_bad' que mantiene los datos "negativos", es decir, los que representan que se ha incumplido con las obligaciones financieras (moroso, cancelación, 'default', o no cumple las políticas de crédito). Se divide esta información que resta en dos: 80% para entrenamiento del modelo y 20% para su validación
5. Después, se empezó con la conversión de variables. Para las fechas, se utilizó métodos de expresiones regulares para cambiar formatos tales como '< 1 year' y convertirlo a valores que el módulo datetime de python pueda comprender. Se debe tener en cuenta que la "fecha de hoy" para el trabajo en cuestión. Es decir, se utiliza la fecha de '2020-08-01'.
6. Extraemos información importante para más adelante, la media de las variables "mths_since_issue_d", "mths_since_last_credit_pull_d".
7. Continuamos con el preprocesamiento, ahora eliminando valores utilizando el estadístico de chi cuadrado. Se calculó sobre cada columna el estadístico. Se calculó el estadístico F para hallar los p values correspondientes. Para evitar los problemas con los valores nulos, se reemplazaron temporalmente por la media de la columna. Al final, con la tabla obtenida, se eliminaron las variables recomendadas por el estadístico de F (es decir, con los menores puntajes) de nuestros datos de entrenamiento. Terminamos con 24 variables (columnas).
- En este punto, para poder desarrollar nuestro WoE (Weight of Evidence) y IV(Information Value) debemos crear variables "dummy" (variable imitación o maniquí) para cada una de las variables categóricas. Antes de continuar, veamos qué es cada una de estas.
  - Dummy: es una variable que se agrega para trabajar con variables categóricas. Lo que se hace, es que para cada posible "valor" que tenga la variable, creamos una nueva variable binaria. Por dar un ejemplo, si tenemos una columna de la forma de la tabla 1, que se puede ver a continuación:

  |Índice| Humedad |
  | --- | --- |
  |1| alta |
  |2| media |
  |3| baja |

  **Tabla 1**: *Tabla inicial*

  Se reemplaza por otra, tal que, cada posible valor para la variable en cuestión se convierta en una nueva columna binaria, como se observa en la tabla 2:

  |Índice| alta | media | baja| 
  | ---- | ---- | ---- | ---- |
  | 1 | 1    |   0  | 0  |
  | 2 | 0    |   1  | 0  |
  | 3 | 0   |   0  | 1  |

**Tabla 2**: *Tabla con dummies*

  - WoE (Weight of Evidence): El _peso de la evidencia_ es una medida de qué tanto apoya la evidencia (o no) una hipótesis. Con este, se mide el riesgo relativo de un atributo de nivel de _binning_.
  $WoE = ln$((\%of good customers)/(\%of bad customers))


  - Binning: Es una técnica de preprocesamiento de data que se usa para reducir los efectos menores de observación. El binning estadístico (Statistical data binning) es una manera de agrupar números continuos o semi-continuos en pequeños números que consideraremos _bins_[2]. Podríamos tomar una variable que vaya desde 1 a 100 y dividirla en grupos de 20, entonces la primera variable tendría valores de 1-20, la segunda de 21-40 y así.

   - IV (Information Value)[3]: Es un método que ayuda a clasificar variables por su orden de importancia en un modelo predictivo. Se calcula con la siguiente fórmula:
  $IV = ∑ $(\% of non-events - \% of events)$ * WOE$

8. One-hot encoding: Se crean las variables dummy para las 4 variables categóricas ('grade', 'home_ownership', 'verification_status', 'purpose'). Se utiliza la siguiente convención de nombres 'variable':'valor'. Por ejemplo, un posible dummy de 'grade' es 'grade:A'. 

9. Nos aseguramos de que nuestro dataset de prueba tenga todas las columnas que el principal. Por lo tanto, agregamos estas nuevas variables dummy.

10. se hace el WoE y se organiza tal que los datos puedan ser categóricos. Esto se hace delimitando los valores continuos usando binning. Esto, si bien afecta la precisión del modelo, vuelve el resultado más fácilmente interpretable.
11. Luego de analizar los puntajes IV de los datos, se observa que algunos tienen, según la interpretación del IV score, fuerte poder de predicción, bajo, sospechoso, o medio. A algunas de las categorías de las variables que tengan muy bajo poder predictivo, y sean parecidas, se juntan con otras a la hora de hacer el binning. El binning en este caso se hace a mano para garantizar un mayor control sobre cómo se crean los grupos de binning y juntar las características deseadas en una sola. Esto también se hace dentro de una clase que permite utilizar el método fit_transform de otros módulos y sea más sencillo de hacer.
12. Se entrena el modelo. Se calculan los puntajes AUC de la RO_Curve y Gini. El puntaje AUC es el área bajo la curva de la curva calculada de sensibilidad contra la especificidad, siendo respectivamente la tasa de verdaderos positivos y la tasa de falsos positivos. Un puntaje de 0.5 es el peor de los casos, indicando que el modelo no puede diferenciar entre los casos verdaderos positivos y los falsos positivos. En este caso, nuestro puntaje es de 0.8658, haciendolo un muy buen puntaje, teniendo en cuenta que el mejor es 1.0.
13. Con el modelo se obtienen los coeficientes de peso analizados por el modelo para poder crear el valor que añadirán o restarán las respectivas categorías de las características elegidas. utilizando fórmulas algebráicas para traer estos coeficientes al rango de valores necesarios, podemos obtener los valores necesarios para poder calcular más adelante el score crediticio de una persona por medio de una multiplicación matricial, gracias a la conversión del dataframe con valores dummies.
14. Los valores calculados con los coeficientes de peso son transformados de manera que al sumarlos, sus resultados sigan el rango de valores del score crediticio de  FICO, esto es, de 300 puntos a 850 puntos.
15. Se obtienen las probabilidades en un nuevo dataframe. 
16. Se hace una curva ROC, para representar gráficamente un análisis de sensibilidad del modelo. Se puede ver a continuación en la Figura 2 y la FIgura 3, que se da una mayor insidencia de falsos positivos que de falsos negativos. 
###### ROC CURVE

<img src="/DataFramesYutiles/ROC curve.png" alt="ROC" title="ROC Curve">

**FIgura 3:** *Curva ROC* 

<img src="/DataFramesYutiles/PR curve.png" alt="PR" title="PR Curve">

**Figura 4:** *Curva PR* 

16. Se hace una scoreboard que ayude a medir qué tanto vale el hecho de quedar en cualquiera de las variables bins, para, con esto, poder calcular los scores de cada individuo. Se desarrolla de tal manera que el mínimo y máximo para cada persona en su score sea 300 y 850, respectivamente. 
# Variables

  | Variable | Significado | 
  | ---- | ---- | 
  | grade |Nota asignada por el Letter of Credit (LC) |  
  | home_ownership | Sobre su vivienda, si tiene casa propia, hipoteca u otro|
  | verification_status | Estado de verificación   |
  | purpose | Razón para hacer el préstamo |
  | term | 36 o 60 cuotas mesuales|
  | int_rate | Tasa de interés de su préstamo (%) |
  | annual_inc |Ingreso anual en dólares |
  | dti | Número de consultas por parte de prestamistas a tu historial |
  | inq_last_6mths |Total en dólares abonado a sus deudas activas |
  | revol_util | Revolving utilization rate ó porcentaje de uso de cupo |
  | out_prncp | Capital pendiente de pago |
  | total_pymnt | Pago total hasta el momento |
  | total_rec_int | Intereses pagados hasta el momento |
  | total_rev_hi_lim | Límite de crédito |
  | mths_since_earliest_cr_line | Primera fecha reportada en la línea de crédito |
  | mths_since_issue_d| Meses desde que se financió el préstamo |
  | mths_since_last_credit_pull_d | Months since LC pulled credit for this loan |


# Análisis de las variables seleccionadas
* Algunas de los puntajes obtenidos para los bins de las variables resultaron ser un poco diferentes a lo esperado. Un ejemplo podría ser la variable "verification status". En esta, los bins tienen puntajes negativos. O sea, se podría tomar como que estar verificado de alguna de las formas posibles en los datos es algo negativo, lo cuál es contradictorio a lo que uno pueda esperar al estar verificado.

Adicionalmente, el bin "Verified", tiene un mejor puntaje (mayor) a "Source Verified". La diferencia entre las dos es que Verified es estar verificado, pero no se sabe por cuál entidad, mientras que en "Source Verified" se sabe la entidad que verifica el estado de crediticio de la persona, haciendolo una certificación más "confiable".

Otro ejemplo se puede encontrar en la primera de las conclusiones del blog, donde se habla de un poco de una variable en las que los puntajes de los bins estuvieron dispersas.


# Conclusiones
* A pesar de que expertos recomiendan mantener una tasa de utilización de crédito (revolving utilization rate) baja, cercana a un 30% [4], podemos observar según la scorecard que el score esperado varía impredeciblemente entre los diferentes bins de la variable revol_util. Se puede ver a continuación en la Figura 5:
<img src="/DataFramesYutiles/Figure_1.png" alt="revolving utilization rate" title="Tasa de utilización">

**Figura 5:** *Tasa de utilización de crédito vs score*

* La variable con mayor peso a la hora de evaluar el puntaje crediticio es el de 'total_pymnt', es decir, el del pago que se ha efectuado hasta el momento de acuerdo a un préstamo ya en efecto. Por lo tanto, se recomienda poner mucho cuidado al hacer un préstamo, especialmente si es uno grande, dado que, este bloqueará estos medios de obtención de capital hasta que no se haya pagado toda o gran parte de la deuda inicial. 
* En el scoreboard, hay algunos bins cuyos coeficientes y scores se encuentran en 0. Esto se debe a que es posible que no hubo ningún dato de este tipo a la hora de entrenar el modelo. Puede ser que sea muy raro el caso, por ejemplo, que alguien tenga una calificación o 'grade' tipo G, o que, a la hora de hacer la división de los datos para crear el set de test haya ocurrido que alguno de los datos terminara exclusivamente en este set. 


# Bibliografía
Código basado en [1]

[1] A. Mumtaz (2020, Agosto 13). How to Develop a Credit Risk Model and Scorecard [Online]. Available: https://towardsdatascience.com/how-to-develop-a-credit-risk-model-and-scorecard-91335fc01f03

[2] SAS® Help Center (2020, Agosto 13). The BINNING Procedure[Online]. Available: https://documentation.sas.com/doc/en/vdmmlcdc/8.1/casstat/viyastat_binning_details02.htm

[3] T. J. Fellers, K. M. Vogt, and M. W. Davidson (2020).  CCD Signal-To-Noise Ratio [Online]. Available: https://www.microscopyu.com/tutorials/ccd-signal-to-noise-ratio

[4] D. Rodeck (2021, Junio 15). What Is Revolving Utilization? [Online]. Available: https://www.nationalfunding.com/blog/what-is-revolving-utilization-how-to-improve-it/ 

## Lecturas recomendadas

J. Chen (2019, Agosto 19). Forward Looking [Online]. Available: https://www.investopedia.com/terms/f/forward-looking.asp
D. Bhalla (2019, Septiembre 5). A Complete Guide to Credit Risk Modelling [Online]. Available: https://www.listendata.com/2019/08/credit-risk-modelling.html
https://media.geeksforgeeks.org/auth/avatar.png
ag01harshit (2020, Diciembre 11). Convert a categorical variable into dummy variables [Online]. Available: https://www.geeksforgeeks.org/convert-a-categorical-variable-into-dummy-variables/
