import streamlit as st
from preprocesamiento import input_toCreditScore
from preprocesamiento import create_score_pie_chart
from preprocesamiento import calcular_percentil

st.set_page_config(page_title="miDataCreditoGratis.com", page_icon="./DataFramesYutiles/stockfish.png", layout="centered", initial_sidebar_state="auto")




st.title("miDataCreditoGratis.com")

st.markdown("¡Infórmate sobre la página! https://www.youtube.com/watch?v=0QM6W8hIw54&t=11s")

st.markdown("""¡Bienvenido! Esta aplicación le ayudará a averiguar su puntaje 
            crediticio de manera totalmenta gratuita. Conocer su puntaje crediticio es útil para
            aquellos que estén pensando en adquirir un préstamo, 
            una tarjeta de crédito o simplemente estén interesados en la confianza que generan
            en las entidades financieras. Para comenzar, simplemente 
            rellene el cuestionario de la izquierda con su información financiera básica. En la parte de abajo podrá visualizar su puntaje crediticio, lo que implica y 
            cómo éste se compara con el de la persona promedio.""")


########### SIDEBAR ##########
with st.sidebar:

    ################# ENTRADAS DATOS A PRECEDIR ##############################
    st.markdown("# Datos de nueva entrada para predecir")
    st.write("Por favor rellene el siguiente cuestionario: ")
    #grade
    grade = st.selectbox(label="Nota asignada por el Letter of Credit (LC): ",
             options=("A","B","C","D","E","F","G", "No lo sé"))
    if grade == "No lo sé":
        grade = "B"

    #home_ownership
    home_ownership = st.selectbox(label="Sobre su vivienda, usted tiene: ",
            options=("Casa propia","Hipoteca","Alquiler/Ninguna/Otra"))
    if home_ownership == "Casa propia":
        home_ownership = "OWN"
    elif home_ownership == "Hipoteca":
        home_ownership = "MORTGAGE"
    else:
        home_ownership = "OTHER_NONE_RENT"
        
    #verification_status
    verification_status = st.selectbox(label="Su estado de verificacion es: ",
            options=("Verificado en la fuente","Verificado","No Verificado", "No lo sé"))
    if verification_status == "Verificado en la fuente":
        verification_status = "Source Verified"
    elif verification_status == "Verificado":
        verification_status = "Verified"
    elif verification_status == "No Verificado":
        verification_status = "Not Verified"
    else:
        verification_status = "Verified"  

    #purpose
    purpose = st.selectbox(label="¿Con qué propósito pediría un préstamo?: ",
            options=("Tarjeta de crédito", "Consolidación de déudas","Médicos","Mejora de hogar" ,"Energía renovable","Negocio pequeño","Boda","Vacaciones","Mudanza","Casa","Automóvil","Compra importante/grande", "Otra/Ninguno"))
    if purpose == "Consolidación de déudas":
        purpose = "debt_consolidation"
    elif purpose == "Médicos":
        purpose = "vacation__house__wedding__med__oth"
    elif purpose == "Mejora de hogar":
        purpose = "major_purch__car__home_impr"
    elif purpose == "Energía renovable":
        purpose = "educ__ren_en__sm_b__mov"
    elif purpose == "Negocio pequeño":
        purpose = "educ__ren_en__sm_b__mov"
    elif purpose == "Boda":
        purpose = "vacation__house__wedding__med__oth"
    elif purpose == "Vacaciones":
        purpose = "vacation__house__wedding__med__oth"
    elif purpose == "Mudanza":
        purpose = "vacation__house__wedding__med__oth"
    elif purpose == "Casa":
        purpose = "vacation__house__wedding__med__oth"
    elif purpose == "Automóvil":
        purpose = "major_purch__car__home_impr"
    elif purpose == "Compra importante/grande":
        purpose = "major_purch__car__home_impr"
    elif purpose == "Tarjeta de crédito":
        purpose = "credit_card"
    else:
        purpose = "debt_consolidation"

    #term
    term = st.selectbox(label="Número de pagos mensuales a la deuda: ", 
                        options=("36","60", "No lo sé"))
    if term == "No lo sé":
        term = "36"
        
    
    #int_rate
    int_rate = st.number_input(label="Tasa de interés de su préstamo (%), si no sabe dejar -1: ", value = -1)
    if int_rate == -1:
        int_rate = "13.676-15.74"
    elif int_rate < 7.071:
        int_rate = "<7.071"
    elif int_rate < 10.374:
        int_rate = "7.071-10.374"
    elif int_rate < 13.676:
        int_rate = "10.374-13.676"
    elif int_rate < 15.74:
        int_rate = "13.676-15.74"
    elif int_rate < 20.281:
        int_rate = "15.74-20.281"
    else:
        int_rate = ">20.281"
    
    #annual_inc
    annual_inc = st.number_input(label="Ingreso anual en dólares, si no sabe dejar 0: ", value = 0)
    if annual_inc == 0:
        annual_inc = "missing"
    elif annual_inc <28555:
        annual_inc = "<28,555"
    elif annual_inc < 37440:
        annual_inc = "28,555-37,440"
    elif annual_inc < 61137:
        annual_inc = "37,440-61,137"
    elif annual_inc < 81872:
        annual_inc = "61,137-81,872"
    elif annual_inc < 102606:
        annual_inc = "81,872-102,606"
    elif annual_inc < 120379:
        annual_inc = "102,606-120,379"
    elif annual_inc <= 150000:
        annual_inc = "120,379-150,000"
    else:
        annual_inc = ">150K"

    dti = "10.397-15.196"

    inq_last_6mths = st.number_input(label="Número de consultas por parte de prestamistas a tu historial (lo puedes consultar en https://www.midatacredito.com o dejar el campo en -1 si no es posible): ", value = -1)
    if inq_last_6mths == -1:
        inq_last_6mths = "missing"
    elif inq_last_6mths == 0:
        inq_last_6mths = "0"
    elif inq_last_6mths < 3:
        inq_last_6mths = "1-2"
    elif inq_last_6mths < 5:
        inq_last_6mths = "3-4"
    else:
        inq_last_6mths = ">4"
    
    #revol_util
    revol_util = "0.5-0.6"

    #out_prncp
    out_prncp = "1,286-6,432"

    #total_pymnt
    total_pymnt = st.number_input(label="Total en dólares abonado a sus deudas activas, si no sabe dejar -1: ", value = -1)
    if total_pymnt == -1:
        total_pymnt = "10,000-15,000"
    elif total_pymnt <10000:
        total_pymnt = "<10,000"
    elif total_pymnt < 15000:
        total_pymnt = "10,000-15,000"
    elif total_pymnt < 20000:
        total_pymnt = "15,000-20,000"
    elif total_pymnt < 25000:
        total_pymnt = "20,000-25,000"
    else:
        total_pymnt = ">25,000"

    #total_rec_int
    total_rec_int = "2,541-4,719"

    #total_rev_hi_lim
    total_rev_hi_lim = "25,525-35,097"

    #mths_since_earliest_cr_line
    mths_since_earliest_cr_line = st.number_input(label="Meses desde que abrió su primera línea de crédito, si no sabe dejar -1: ", value = -1)
    if mths_since_earliest_cr_line == -1:
        mths_since_earliest_cr_line = "missing"
    elif mths_since_earliest_cr_line <125:
        mths_since_earliest_cr_line = "<125"
    elif mths_since_earliest_cr_line < 167:
        mths_since_earliest_cr_line = "125-167"
    elif mths_since_earliest_cr_line < 249:
        mths_since_earliest_cr_line = "167-249"
    elif mths_since_earliest_cr_line < 331:
        mths_since_earliest_cr_line = "249-331"
    elif mths_since_earliest_cr_line < 434:
        mths_since_earliest_cr_line = "331-434"
    else:
        mths_since_earliest_cr_line = ">434"

    #mths_since_issue_d
    mths_since_issue_d = st.number_input(label="Meses desde que abrió su préstamo actual, si no sabe dejar -1: ", value = -1)
    if mths_since_issue_d == -1:
        mths_since_issue_d = "89-100"
    elif mths_since_issue_d <79:
        mths_since_issue_d = "<79"
    elif mths_since_issue_d < 89:
        mths_since_issue_d = "79-89"
    elif mths_since_issue_d < 100:
        mths_since_issue_d = "89-100"
    elif mths_since_issue_d < 122:
        mths_since_issue_d = "100-122"
    else:
        mths_since_issue_d = ">122"

    #mths_since_last_credit_pull_d
    mths_since_last_credit_pull_d = "56-61"

#############################

score = input_toCreditScore(grade, home_ownership, verification_status, purpose, term, int_rate,
                            annual_inc, dti, inq_last_6mths, revol_util, out_prncp, total_pymnt, 
                            total_rec_int, total_rev_hi_lim, mths_since_earliest_cr_line, mths_since_issue_d,
                            mths_since_last_credit_pull_d)


st.subheader("Oráculo de puntaje crediticio")

if score >= 630:
    st.markdown(f"""¡Felicitaciones! Su puntaje es de **{score}**, que está muy por encima del puntaje 
            promedio de los consumidores y demuestra claramente a los prestamistas que es un
            prestatario excepcional.""")
elif score >= 584:
    st.markdown(f"""¡Bien! Su puntaje es de **{score}**, que está por encima del puntaje 
            promedio de los consumidores y demuestra a los prestamistas que es un
            prestatario muy confiable.""")
elif score >= 517:
    st.markdown(f"""Su puntaje es de **{score}**, que está cerca o ligeramente por encima del puntaje 
            promedio de los consumidores y la mayoría de los prestamistas lo consideran como un 
            buen puntaje.""")
elif score >= 460:
    st.markdown(f"""Su puntaje es de **{score}**, que está por debajo del puntaje 
            promedio de los consumidores. Aún así, existen prestamistas que aprobarán
            prestamos con este puntaje.""")
else:
    st.markdown(f"""Su puntaje es de **{score}**, que está muy por debajo del puntaje 
            promedio de los consumidores y demuestra a los prestamistas que es un
            prestatario riesgoso.""")

percentil = calcular_percentil(score)

st.markdown(f"""Su percentil es de **{percentil}**,  lo que significa que su score crediticio 
            está por encima del de **{percentil}%** de las personas.""")
if score >= 630:
    st.pyplot(create_score_pie_chart(explode = (0,0,0,0,0.4)))  
elif score >= 584:
    st.pyplot(create_score_pie_chart(explode = (0,0,0,0.1,0)))   
elif score >= 517:
    st.pyplot(create_score_pie_chart(explode = (0,0,0.1,0,0))) 
elif score >= 460:
    st.pyplot(create_score_pie_chart(explode = (0,0.1,0,0,0)))   
else:
    st.pyplot(create_score_pie_chart(explode = (0.4,0,0,0,0)))

st.markdown("Rangos adaptados de: *experian.com*")

st.markdown("Para detalles técnicos sobre el desarrollo de la aplicación, dirigirse a: https://github.com/EsGarciaC/TAE-trabajo2")

        