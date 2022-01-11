import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='BWS', layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #F5F5F5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

background_color = '#F5F5F5'

st.title('Risk Management')


@st.cache
def get_data(filename):
    getData = pd.read_csv(filename)

    return getData


rad = st.sidebar.radio("Navigation", ["MD6400", "MJ1500 Deposit"])

if rad == "MD6400":
    st.header('MD6400 (29-12-2021)')

    excel_file = 'data/MD6400 211229.csv'

    df = get_data(excel_file)

    branch = df['Branch Name'].unique().tolist()
    product = df['Product Name'].unique().tolist()
    corp = df['Corperation Size'].unique().tolist()
    kualitas = df['Kualitas'].unique().tolist()

    branch_selection = st.multiselect('Cabang:',
                                              branch,
                                              default=branch)

    product_selection = st.sidebar.multiselect('Produk:',
                                               product,
                                               default=product)

    corp_selection = st.sidebar.multiselect(
        "Corperation Size:", corp, default=corp)

    kualitas_selection = st.sidebar.slider(
        "Kualitas:", min_value=1, max_value=5, value=(1, 5))

    mask = (df['Branch Name'].isin(branch_selection)
            ) & (df['Product Name'].isin(product_selection)
                 ) & (df['Corperation Size'].isin(corp_selection)
                      ) & (df['Kualitas'].between(*kualitas_selection))
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Result: **{number_of_result}** *')

    st.dataframe(df[mask])

    branch_container = st.container()
    product_container = st.container()
    corp_container = st.container()
    kualitas_container = st.container()

    with branch_container:
        st.header('Grafik Outstanding Terhadap Cabang')

        if st.checkbox('Tampilkan Grafik Outstanding per Cabang', True):
            df_grouped_branch = df[mask].groupby(
                by=['Branch Name']).sum()[['Loan Amount']]
            df_grouped_branch = df_grouped_branch.reset_index()

            bar_chart_branch = px.bar(df_grouped_branch,
                                      x='Branch Name',
                                      y='Loan Amount',
                                      text='Loan Amount',
                                      color_discrete_sequence=[
                                        '#F63366']*len(df_grouped_branch),
                                      template='plotly_white')
            bar_chart_branch.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            bar_chart_branch.update_layout(
                width=900,
                height=600,
                font=dict(color="#383635"))
            st.plotly_chart(bar_chart_branch, width=200, height=60)

    with product_container:
        st.header('Grafik Outstanding Terhadap Produk')

        if st.checkbox('Tampilkan Grafik Outstanding per Produk'):
            df_grouped_product = df[mask].groupby(
                by=['Product Name']).sum()[['Loan Amount']]
            df_grouped_product = df_grouped_product.reset_index()

            bar_chart_product = px.bar(df_grouped_product,
                                       x='Product Name',
                                       y='Loan Amount',
                                       text='Loan Amount',
                                       color_discrete_sequence=[
                                           '#F63366']*len(df_grouped_product),
                                       template='plotly_white')
            bar_chart_product.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            bar_chart_product.update_layout(
                margin_autoexpand=True,
                width=900,
                height=600,
                font=dict(color="#383635"))
            st.plotly_chart(bar_chart_product)

    with corp_container:
        st.header('Grafik Outstanding Terhadap Corperation Size')

        if st.checkbox('Tampilkan Grafik Outstanding per Corperation Size'):
            df_grouped_corp = df[mask].groupby(by=['Corperation Size']).sum()[
                ['Loan Amount']]
            df_grouped_corp = df_grouped_corp.reset_index()

            bar_chart_corp = px.bar(df_grouped_corp,
                                    x='Corperation Size',
                                    y='Loan Amount',
                                    text='Loan Amount',
                                    color_discrete_sequence=[
                                        '#F63366']*len(df_grouped_corp),
                                    template='plotly_white')
            bar_chart_corp.update_layout(margin=dict(l=5, r=5, b=10, t=10))
            st.plotly_chart(bar_chart_corp)

    with kualitas_container:
        st.header('Grafik Outstanding Terhadap Kualitas')

        if st.checkbox('Tampilkan Grafik Outstanding per Kualitas'):
            df_grouped_kualitas = df[mask].groupby(
                by=['Kualitas']).sum()[['Loan Amount']]
            df_grouped_kualitas = df_grouped_kualitas.reset_index()

            df_grouped_kualitas.dropna(inplace=True)

            pie_chart = px.pie(df_grouped_kualitas,
                               title='Outstanding per Kualitas',
                               values='Loan Amount',
                               names='Kualitas')

            pie_chart.update_layout(
                showlegend=False,
                paper_bgcolor=background_color,
                font=dict(color="#383635"))
            st.plotly_chart(pie_chart)

if rad == "MJ1500 Deposit":
    st.header('MJ1500 Deposan (29-12-2021)')

    excel_file = 'data/Mj1500 Deposit.csv'

    df = get_data(excel_file)

    branch = df['Branch'].unique().tolist()
    coa = df['COA Name'].unique().tolist()

    branch_selection = st.multiselect('Cabang:',
                                              branch,
                                              default=branch)

    coa_selection = st.sidebar.multiselect('COA Name:',
                                              coa,
                                              default=coa)

    mask = (df['Branch'].isin(branch_selection)
            ) & (df['COA Name'].isin(coa_selection))

    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Result: **{number_of_result}** *')

    st.dataframe(df[mask])

    branch2_container = st.container()
    coa_container = st.container()

    with branch2_container:
        st.header('Grafik Base Currency Amount Terhadap Cabang')

        if st.checkbox('Tampilkan Grafik Base Currency Amount per Cabang', True):
            df_grouped_branch = df[mask].groupby(by=['Branch']).sum()[
                ['Base Currency Amount']]
            df_grouped_branch = df_grouped_branch.reset_index()

            bar_chart_branch = px.bar(df_grouped_branch,
                                    x='Branch',
                                    y='Base Currency Amount',
                                    text='Base Currency Amount',
                                    color_discrete_sequence=[
                                        '#F63366']*len(df_grouped_branch),
                                    template='plotly_white')
            bar_chart_branch.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            bar_chart_branch.update_layout(
                width=900,
                height=600,
                font=dict(color="#383635"))
            st.plotly_chart(bar_chart_branch)

    with coa_container:
        st.header('Grafik Base Currency Amount Terhadap COA Name')

        if st.checkbox('Tampilkan Grafik Base Currency Amount per COA Name'):
            df_grouped_coa = df[mask].groupby(
                by=['COA Name']).sum()[['Base Currency Amount']]
            df_grouped_coa = df_grouped_coa.reset_index()

            bar_chart_coa = px.bar(df_grouped_coa,
                                    x='COA Name',
                                    y='Base Currency Amount',
                                    text='Base Currency Amount',
                                    color_discrete_sequence=[
                                        '#F63366']*len(df_grouped_coa),
                                    template='plotly_white')
            bar_chart_coa.update_layout(margin=dict(l=5, r=5, b=10, t=10))

            bar_chart_coa.update_layout(
                font=dict(color="#383635"))
            st.plotly_chart(bar_chart_coa)