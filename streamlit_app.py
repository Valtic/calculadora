from datetime import timedelta
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy.sql import text
from PIL import Image

icon=Image.open('favicon.ico')

st.set_page_config(
    page_title="Calc - Streamlit Web develop",
    page_icon=icon,
    layout='centered',
    initial_sidebar_state='auto',
    menu_items={
        'Get Help':'https://streamlit.io/',
        'About':'About your application: ** Hello World**'
    }
)
st.sidebar.title("Seleccion")

#mark = ' <div class="markdown-text-container stText" style="width: 698px;"> <footer><p></p></footer><div style="font-size: 12px;">  Hello world v 0.1</div> <div style="font-size: 12px;">Hello world LLC.</div> </div>' 
#st.sidebar.markdown(mark, unsafe_allow_html=True)


# Title of the app
title_template="""
    <div style="background-color:rgb(235, 238, 245);border-radius:12px; padding:8px;">
    <h1 style="color:rgb(3, 24, 66)"> Cambio de unidades volumen</h1>
    </div> """

# st.title('title_template')
st.markdown(title_template, unsafe_allow_html=True)
    
subheader_template="""
    <div style="background-color: white; padding:8px;">
    <h3 style="color:rgb(202, 240, 248)"> By Valtic</h3>
    </div> """
    
st.markdown(subheader_template, unsafe_allow_html=True)

opciones_menu=["Home", "Litros -> galones (us)",
                     "Galones -> litros",
                      "gpm (us) -> litros/hora",
                       "litros/h -> gpm(us)",
                       "Streamlit Web App Cap 2",
                        "Streamlit Web App Cap 3"]

# Sidebar menu for navigation
menu = st.sidebar.selectbox("Selecciona una opción", opciones_menu)

# Home
if menu == opciones_menu[0]: #HOME
    st.header("Conversion unidades de Volumen")
    st.write("Usa el menu lateral para seleccionar una calculadora")

    conn = st.connection('pets_db', type='sql')

    with conn.session as s:
        try:
            st.markdown(f"Note that `s` is a `{type(s)}`")
            s.execute(text('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);'))
            s.execute(text('DELETE FROM pet_owners;'))
            pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
            for k in pet_owners:
                s.execute(text(
                    'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);'),
                    params=dict(owner=k, pet=pet_owners[k])
                )
            s.commit()
        except:
            st.error("Error al incializar la base de datos")

    pet_owners = conn.query('select * from pet_owners', ttl=timedelta(minutes=10))
    st.dataframe(pet_owners)

# gal to l.
elif menu == opciones_menu[1] or menu == opciones_menu[2]: #"Galones -> litros"
    st.header("Galones (us) a Litros")
    galones = st.number_input("Escribe volumen en galones para calcular en litros",step=1.0)
    if galones:
        litros = galones * 3.785412
        st.write(f"Resultado: {galones:.2f} gal son {litros:.2f} litros.")

    # L to gal.
    st.header("Litros a Galones(us)")
    litros_2 = st.number_input("Escribe volumen en litros para calcular en galones(us)",step=1.0)
    if litros_2:
        galones_2 = litros_2 / 3.785412
        st.write(f"Resultado: {litros_2:.2f} litros son {galones_2:.2f} galones.")


# gmp to l/h.
elif menu == opciones_menu[3] or menu == opciones_menu[4]: 
    #"Galones por minuto -> litros/hora"
    st.header("Galones por minuto (us) a Litros/hora")
    gpm = st.number_input("Escribe volumen en galones para calcular en litros",step=1.0)
    if gpm:
        litros_hora = ( gpm * 3.785412 ) * 60
        st.info(f"Resultado: {gpm:.2f} gpm (us) son {litros_hora:.2f} litros/hora.")

# l/h to gpm.
#elif menu == opciones_menu[4]: #"Litros/hora -> Galones por minuto"
    st.header("Litros/hora a Galones por minuto (us)")
    litros_hora_ = st.number_input("Escribe volumen en litros para calcular en galones(us)",step=1.0)
    if litros_hora_:
        galones_pmim = ( litros_hora_ / 3.785412) / 60
        st.info(f"Resultado: {litros_hora_:.2f} litros/hora son {galones_pmim:.2f} gpm (us).")

#Web Application Development with Streamlit Develop and Deploy Secure and Scalable Web Applications 
elif menu == opciones_menu[5]: #"Streamlit Web App Cap 2"
    #Ejercicios del libro
    st.header("Web Application Development with Streamlit")

    with st.form('feedback_form'):
        st.header('Feedback form')
        # Creating columns to organize the form
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input('Please enter your name')
            rating = st.slider('Please rate this app',0,10,5)
        with col2:
            dob = st.date_input('Please enter your date of birth')
            recommend = st.radio('Would you recommend this app to others?',('Yes','No'))
        submit_button = st.form_submit_button('Submit')
        if submit_button:
            st.write('**Name:**', name, '**Date of birth:**', dob,
            '**Rating:**', rating,'**Would recommend?:**', recommend)

    st.header("Conditionals IF") 
    def display_name(name):
        st.info(f'**Name:** {name}')
    name=st.text_input('Please fill your name')
    if not name:
        st.error("No name entered")
        #st.stop()  # Ya detiene el scrip y no sigue cargando el resto de cosas-.
    if name:
        display_name(name)
    #st.header("Si haces STOP (nombre en blanco - no me ves") 

    col1, col2=st.columns(2)
    with col1:
        number_1=st.number_input('Please enter the first number',value=0,step=1)

    with col2:
        number_2=st.number_input('Please enter the second number',value=0,step=1)

    try:
        st.info(f'**{number_1}/{number_2}=** {number_1/number_2:.2f}')
    #except ZeroDivisionError:
    #   st.error("Cannot divide by Zero")
    except Exception as e:
        st.error(f'Error: {e}')

    st.header("Mutate dataframe")

    np.random.seed(0)
    df = pd.DataFrame(np.random.randn(4,3),columns=('Colum_1','Colum_2','Colum_3'))

    st.subheader('Original Dataframe')  
    st.write(df)

    df = df[['Colum_1','Colum_3']]
    df=df.sort_values(by='Colum_1',ascending=True)    
    st.subheader('Mutated dataframe')
    st.write(df)

    st.header("Group by")
    df3 = pd.DataFrame( np.random.randn(12, 3), columns=('Score 1','Score 2','Score 3'))
    df3['Name'] = pd.DataFrame(['John','Alex','Jessica','John','Alex',
    'John', 'Jessica','John','Alex','Alex','Jessica','Jessica'])
    df3['Category'] = pd.DataFrame(['B','A','D','C','C','A',
    'B','C','B','A','A','D'])
    st.subheader('Original dataframe')
    st.write(df3)
    df3 = df3.groupby(['Name','Category']).sum()  #.first()
    st.subheader('Mutated dataframe')
    st.write(df3)

    st.header("Merge")
    df1 = pd.DataFrame(data={'Name':['Jessica','John','Alex'],'Score 1':[77,56,87]})
    df2 = pd.DataFrame(data={'Name':['Jessica','John','Alex'],'Score 2':[76,97,82]}
    )
    st.subheader('Original dataframes')
    st.write(df1)
    st.write(df2)
    df1 = df1.merge(df2,how='inner',on='Name')
    st.subheader('Mutated dataframe')
    st.write(df1)


    # Plot Sine Wave
    st.header("Plot Sine Wave")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    st.pyplot(plt)

    st.header('** CHARTS **')
    df4 = pd.DataFrame(data={'Exam':['Exam 1','Exam 2','Exam 3'],'Jessica':[77,76,87],'John':[56,97,95],'Alex':[87,82,93]})
    df4.set_index('Exam').plot(kind='line',xlabel='Exam',ylabel='Score',subplots=True) 
    st.pyplot(plt)



# Plot CSV Data

    st.header("Plot CSV Data")
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        st.line_chart(data)

# Plot interactive Chart

    st.header("Plot interantive Chart")
    import plotly.graph_objects as go

    df= pd.DataFrame(data={'Exam': ['Exam 1','Exam 2','Exam 3'],'Jessica':[77,76,87],'John':[56,97,95],'Alex':[87,82,93]})

    fig= go.Figure(data=[
                   go.Line(name='Jessica',x=df['Exam'],y=df['Jessica']),
                   go.Line(name='John',x=df['Exam'],y=df['John']),  
                   go.Line(name='Alex',x=df['Exam'],y=df['Alex']) ]) 

    fig.update_layout( xaxis_title='exam',
                      yaxis_title='score',
                      legend_title='name')

    st.plotly_chart(fig)

    import plotly.express as px
    program = st.sidebar.selectbox('Select program',['Dataframe Demo','Other Demo'])
    code = st.sidebar.checkbox('Display code')
    if program == 'Dataframe Demo':
        df = px.data.stocks()
        st.title('DataFrame Demo')
        stocks = st.multiselect('Select stocks',df.columns[1:],
        [df.columns[1]])
        st.subheader('Stock value')
        # Mutating the dataframe to keep selected columns only
        st.write(df[['date'] + stocks].set_index('date'))
        # Creating a Plotly timeseriesfig line chart
        fig = px.line(df, x='date', y=stocks,hover_data={"date": "|%Y %b %d"}  )
        st.write(fig)

        if code:
            st.code(
            """
            import streamlit as st
            import pandas as pd
            import plotly.express as px
            df = px.data.stocks()
            st.title('DataFrame demo')
            program = st.sidebar.selectbox('Select
            program',['Dataframe Demo'])
            code = st.sidebar.checkbox('Display code')
            stocks = st.multiselect('Select stocks',df.columns[1:],[df.
            columns[1]])
            st.subheader('Stock value')
            st.write(df[['date'] + stocks].set_index('date'))
            fig = px.line(df, x='date', y=stocks,
            hover_data={"date": "|%Y %b %d"}
            )
            st.write(fig)
            """
            )
    elif program == 'Other Demo':
        st.title('Other Demo')
        st.write("- TODO -")

# CAP 3        
elif menu == opciones_menu[6]: #"Streamlit Web App Cap 2"
    #Ejercicios del libro
    st.header("Web Application Development with Streamlit Cap 3- User Interface")

    from datetime import datetime

    #Expander in sidebar
    st.sidebar.subheader('Expander')
    with st.sidebar.expander('Time'):
        time = datetime.now().strftime("%H:%M:%S")
        st.write('**%s**' % (time))
        #Columns in sidebar
        st.sidebar.subheader('Columns')
        col1, col2 = st.sidebar.columns(2)
        with col1:
            option_1 = st.selectbox('Please select option 1',['A','B'])
        with col2:
            option_2 = st.radio('Please select option 2',['A','B'])

    #Container in sidebar
    container = st.sidebar.container()
    container.subheader('Container')
    option_3 = container.slider('Please select option 3')
    st.sidebar.warning('Elements outside of container will be displayed externally')
    container.info('**Option 3:** %s' % (option_3))

    #Expander in main body
    st.subheader('Expander')
    with st.expander('Time'):
        time = datetime.now().strftime("%H:%M:%S")
        st.write('**%s**' % (time))
    #Columns in main body
    st.subheader('Columns')
    col1, col2 = st.columns(2)
    with col1:
        option_4 = st.selectbox('Please select option 4',['A','B'])
    with col2:
        option_5 = st.radio('Please select option 5',['A','B'])

    #Container in main body
    container = st.container()
    container.subheader('Container')
    option_6 = container.slider('Please select option 6')
    st.warning('Elements outside of container will be displayed externally')
    container.info('**Option 6:** %s' % (option_6))