
key = '63a3cf94e0042b9c67abf0892fc1d223'

import requests
import pandas as pd
import json
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events

# Function to fetch data from the API
def fetch_data(api_key, search_query, hits_per_page):
    url = 'https://9ioacg5nhe-dsn.algolia.net/1/indexes/alltrails_primary_en-US/query'
    headers = {
        'Content-Type': 'application/json',
        'X-Algolia-API-Key': api_key,
        'X-Algolia-Application-Id': '9IOACG5NHE'
    }
    payload = {
        "params": f"query={search_query}&hitsPerPage={hits_per_page}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data['hits'])

# Function to fetch detailed hike information
def fetch_hike_details(hike_id):
    url = f'https://www.alltrails.com/api/alltrails/trails/{hike_id}/props?explore=true'
    headers = {
        'X-At-Key': '3p0t5s6b5g4g0e8k3c1j3w7y5c3m4t8i',
        'X-Csrf-Token': 'lNDgw5dw5_PVi5qXuGOOFtGifT_uObF9j0Kl6UiiOLex_z9IvpPPB50-R9Yfej5HJzk8xpexYVt2xOp9OjaHig',
        'X-Language-Locale': 'en-US',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,am;q=0.8',
        'Referer': 'https://www.alltrails.com/explore/trail/us/washington/duwamish-trail--2',
        'Sec-CH-UA': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'Sec-CH-UA-Arch': 'x86',
        'Sec-CH-UA-Full-Version-List': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Microsoft Edge";v="126.0.2592.81"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Model': '',
        'Sec-CH-UA-Platform': 'Windows',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cookie': 'trail_count=0; at_osano={%22consent%22:{%22ESSENTIAL%22:%22ACCEPT%22%2C%22STORAGE%22:%22ACCEPT%22%2C%22MARKETING%22:%22ACCEPT%22%2C%22PERSONALIZATION%22:%22ACCEPT%22%2C%22ANALYTICS%22:%22ACCEPT%22%2C%22OPT_OUT%22:%22DENY%22}}; osano_consentmanager_uuid=c8ee19ba-451f-4505-9ff0-ed31a0dc4d28; osano_consentmanager=kpR4TjDdcQVYG891mG-V6jzswUc_70K3Ry9qXwBpktS0cK13FX4zur3iPVvDbQjYkZY1S4zyaFjjsw7QHat71OhjNd1dD7lCJ9BQ3pBN_zncmVhd3xRHM2NlRNa80aVlu_TbqrAoKImvAbV_Hh9yVKmApO_ZCN4eKgzQ4P8WYm6DG_5rtBZy0CHmypqVgse7cgljU8Qbw-rhoX2E2RHq7dk842UXr5KxwaZ7U7TTE1VP_n4oFXcwhQv5EwP3AYa48qPmeV2Nq8IAPmRzxtPV8_tOxZn4iGRecTCVjg==; _ga=GA1.1.2023577491.1720036521; _fbp=fb.1.1720036520793.529386507798065949; _tt_enable_cookie=1; _ttp=hf-lPa9KWVbUQhK3RQWz9-UV2bZ; __gads=ID=1dfd5d7b9f83e1a5:T=1720036521:RT=1720036521:S=ALNI_MZJygtQmLocoqbkxPNAtHSSBa8FCw; at_redirected_lang_amt=1; at_former_lang_code_pre_redirect=en; G_ENABLED_IDPS=google; _pin_unauth=dWlkPVpUQmxZalF4T0dVdFpqVmtNaTAwTW1ZM0xUZ3hPREl0T0RVelpUbGlPR0UxT0dJNA; access_token=OXA4H0El_fc_yVJYJSZ_RGiHGp4caCK1MwJRihMucGU; refresh_token=tDpgd1_G5yEZ1YbjZlUdmwif9dCmLhpiqUndkO9gDJc; auth_client_id=pR23h1Okw-8bPWpue8UBtR8XvebH2oijOU6ebx8QGAQ; at_tinuitifpc=8c25d815-b999-424b-9c53-0dbdc41541d6; at_redirected_lang_msg_shown=true; AF_DEFAULT_MEASUREMENT_STATUS=false; ab._gd=ab._gd; IR_22353=1720036767030%7C0%7C1720036767030%7C%7C; _derived_epik=dj0yJnU9dV90dlFtdHB5RlBDOUtKVnprNzNWTWRBU1d4WFQwVUEmbj1WbnplUkFaUUh2TUpaaV9seEN1Qlh3Jm09NCZ0PUFBQUFBR2FGclo4JnJtPTQmcnQ9QUFBQUFHYUZyWjgmc3A9Mg; _ga_V6WJN779TY=GS1.1.1720036520.1.1.1720036790.0.0.0; datadome=MAEeBQmysrOyL2TJa5zwbS24_Mgo~WUzRMKTjYudNBxSTWR9YCgBmzjNBVtZZAsd~ZtHn6OlkNkxCCzg5KgKNEhCSUU5waq0xSQbhftuYMW9drb9BKeQoAGmq5dqxaMl; _alltrails_session=DLntQPcNWOanIWE8dsSCPQKDEjLexX4i%2BDI46F3BPMa7%2BtWUvRiedp1UsYKVCR3kCpx%2FGWEE%2F5%2FHhuW0SZZmRQlsFab%2BqlKhPemCBUg24wpRNDTa0LLrYzIg33piWuGS1h4lA%2B0lOAdjEfycaUylahZPdmaXgLgWp4GP6v7esapfr74EAgyJg8IzlfMNkU4mNRZpHgw57nnW%2F5OLZbURyCQEuEbpAGsFXVIEg2fns9IcH3kwR0MZ%2BIMJFs7WAYWo32X7iBJ81K3I5AW96llU5%2BHExoGr%2FrR0FZjG7OU9h%2BrxqH2b97Cx7%2FETJHNdxdKMPxgwo18I2isqksOIgVHDKi4W7%2Fs%3D--hZ6cOCto%2BNXyIU4N--mjjINcWXfw2WuMgdhIINIg%3D%3D; amp_6ad463=c5731cfb-2eb1-476a-84ea-8f6325be1527.MjAxODQxNTM=..1i1t2s70n.1i1'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Streamlit app
st.title("Trail Data Viewer")

# Input for API key
api_key = key

# Input for search query
search_query = st.text_input("Enter search query:", value="")

# Input for hits per page
hits_per_page = st.number_input("Enter number of hits per page:", min_value=1, value=10)

# Checkbox for excluding NaN/0 values
exclude_nan_zero = st.checkbox("Exclude NaN/0 values", value=True)

if api_key:
    df = fetch_data(api_key, search_query, hits_per_page)

    if not df.empty:
        # Check for necessary columns and fill NaN values if they exist
        necessary_columns = ['length', 'elevation_gain', 'popularity', 'num_reviews', 'avg_rating', '_cluster_geoloc']
        for column in necessary_columns:
            if column in df.columns:
                df[column] = df[column].fillna(0)
            else:
                df[column] = 0

        # Sort the DataFrame by the 'popularity' column
        if 'popularity' in df.columns:
            df = df.sort_values(by='popularity', ascending=False)

        # Reorder the columns to show specified columns first
        columns_order = ['ID', 'length', 'popularity', 'elevation_gain', 'name', '_cluster_geoloc']
        df = df.reindex(columns=columns_order + [col for col in df.columns if col not in columns_order])

        # Display the sorted and reordered DataFrame interactively
        st.write("### Sorted Trail Data")
        st.dataframe(df)

        # Filters for the DataFrame
        length_filter = st.slider("Filter trails longer than (meters):", min_value=0, max_value=int(df['length'].max()), value=12000)
        elevation_filter = st.slider("Filter trails with elevation gain greater than (meters):", min_value=0, max_value=int(df['elevation_gain'].max()), value=500)
        popularity_filter = st.slider("Filter trails with popularity greater than:", min_value=0.0, max_value=float(df['popularity'].max()), value=50.0)
        reviews_filter = st.slider("Filter trails with number of reviews greater than:", min_value=0, max_value=int(df['num_reviews'].max()), value=100)

        # Apply filters
        filtered_df = df[(df['length'] > length_filter) &
                         (df['elevation_gain'] > elevation_filter) &
                         (df['popularity'] > popularity_filter) &
                         (df['num_reviews'] > reviews_filter)]

        if exclude_nan_zero:
            filtered_df = filtered_df[(filtered_df['length'] > 0) &
                                      (filtered_df['elevation_gain'] > 0) &
                                      (filtered_df['popularity'] > 0) &
                                      (filtered_df['num_reviews'] > 0)]

        st.write(f"### Filtered Trails (Length > {length_filter} meters, Elevation Gain > {elevation_filter} meters, Popularity > {popularity_filter}, Reviews > {reviews_filter})")
        st.dataframe(filtered_df)

        # Plot interactive data: trail length vs elevation gain
        if 'length' in filtered_df.columns and 'elevation_gain' in filtered_df.columns:
            st.write("### Trail Length vs. Elevation Gain")
            fig = px.scatter(filtered_df, x='length', y='elevation_gain', hover_data=['name', 'popularity'])
            selected_points = plotly_events(fig)
            st.plotly_chart(fig)

            # Display details of selected points
            if selected_points:
                selected_df = filtered_df.iloc[[p['pointIndex'] for p in selected_points]]
                st.write("### Details of Selected Trails")
                st.dataframe(selected_df)
                # Fetch and display detailed hike information
                hike_id = selected_df.iloc[0]['ID']
                hike_details = fetch_hike_details(hike_id)
                st.write("### Detailed Hike Information")
                st.json(hike_details)

        # Additional interactive chart: Length vs. Popularity
        if 'length' in filtered_df.columns and 'popularity' in filtered_df.columns:
            st.write("### Trail Length vs. Popularity")
            fig = px.scatter(filtered_df, x='length', y='popularity', hover_data=['name', 'elevation_gain'])
            selected_points = plotly_events(fig)
            st.plotly_chart(fig)

            # Display details of selected points
            if selected_points:
                selected_df = filtered_df.iloc[[p['pointIndex'] for p in selected_points]]
                st.write("### Details of Selected Trails")
                st.dataframe(selected_df)
                # Fetch and display detailed hike information
                hike_id = selected_df.iloc[0]['ID']
                hike_details = fetch_hike_details(hike_id)
                st.write("### Detailed Hike Information")
                st.json(hike_details)

        # Additional interactive chart: Elevation Gain vs. Popularity
        if 'elevation_gain' in filtered_df.columns and 'popularity' in filtered_df.columns:
            st.write("### Elevation Gain vs. Popularity")
            fig = px.scatter(filtered_df, x='elevation_gain', y='popularity', hover_data=['name', 'length'])
            selected_points = plotly_events(fig)
            st.plotly_chart(fig)

            # Display details of selected points
            if selected_points:
                selected_df = filtered_df.iloc[[p['pointIndex'] for p in selected_points]]
                st.write("### Details of Selected Trails")
                st.dataframe(selected_df)
                # Fetch and display detailed hike information
                hike_id = selected_df.iloc[0]['ID']
                hike_details = fetch_hike_details(hike_id)
                st.write("### Detailed Hike Information")
                st.json(hike_details)

        # Additional interactive chart: Average Rating vs. Number of Reviews
        if 'avg_rating' in filtered_df.columns and 'num_reviews' in filtered_df.columns:
            st.write("### Average Rating vs. Number of Reviews")
            fig = px.scatter(filtered_df, x='avg_rating', y='num_reviews', hover_data=['name', 'popularity'])
            selected_points = plotly_events(fig)
            st.plotly_chart(fig)

            # Display details of selected points
            if selected_points:
                selected_df = filtered_df.iloc[[p['pointIndex'] for p in selected_points]]
                st.write("### Details of Selected Trails")
                st.dataframe(selected_df)
                # Fetch and display detailed hike information
                hike_id = selected_df.iloc[0]['ID']
                hike_details = fetch_hike_details(hike_id)
                st.write("### Detailed Hike Information")
                st.json(hike_details)

        # Additional interactive chart: Average Rating vs. Popularity
        if 'avg_rating' in filtered_df.columns and 'popularity' in filtered_df.columns:
            st.write("### Average Rating vs. Popularity")
            fig = px.scatter(filtered_df, x='avg_rating', y='popularity', hover_data=['name', 'num_reviews'])
            selected_points = plotly_events(fig)
            st.plotly_chart(fig)

            # Display details of selected points
            if selected_points:
                selected_df = filtered_df.iloc[[p['pointIndex'] for p in selected_points]]
                st.write("### Details of Selected Trails")
                st.dataframe(selected_df)
                # Fetch and display detailed hike information
                hike_id = selected_df.iloc[0]['ID']
                hike_details = fetch_hike_details(hike_id)
                st.write("### Detailed Hike Information")
                st.json(hike_details)
