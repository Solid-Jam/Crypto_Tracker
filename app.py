import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
# Define the base URL of the FastAPI application
BASE_URL = os.getenv('BASE_URL')

api_key_input = st.text_input("Enter API Key", type="password")


def validate_api_key(api_key):
    headers = {"api-key": api_key}
    response = requests.get(f"{BASE_URL}/validate_key/", headers=headers)
    return response.status_code == 200


# Helper functions for API communication
def get_users():
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch users.")
        return []


def add_user(api_key, name):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/users/", json={"name": name}, headers=headers)
    if response.status_code == 200:
        st.success(f"user '{name}' added successfully!")
    else:
        st.error(f"Failed to add user: {response.json().get('detail', 'Unknown error')}")


def update_user(api_key, user_id, name):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json={"name": name}, headers=headers)
    if response.status_code == 200:
        st.success(f"user '{name}' updated successfully!")
    else:
        st.error(f"Failed to update user: {response.json().get('detail', 'Unknown error')}")


def delete_user(api_key, user_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    if response.status_code == 200:
        st.success("user deleted successfully!")
    else:
        st.error(f"Failed to delete user: {response.json().get('detail', 'Unknown error')}")


def get_assets():
    response = requests.get(f"{BASE_URL}/assets/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch assets.")
        return []


def add_asset(api_key, asset_data):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/assets/", json=asset_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Asset '{asset_data['title']}' added successfully!")
    else:
        st.error(f"Failed to add asset: {response.json().get('detail', 'Unknown error')}")


def update_asset(api_key, asset_id, asset_data):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/assets/{asset_id}", json=asset_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Asset '{asset_data['title']}' updated successfully!")
    else:
        st.error(f"Failed to update asset: {response.json().get('detail', 'Unknown error')}")


def delete_asset(api_key, asset_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/assets/{asset_id}", headers=headers)
    if response.status_code == 200:
        st.success("Asset deleted successfully!")
    else:
        st.error(f"Failed to delete asset: {response.json().get('detail', 'Unknown error')}")


# Dashboard for managing Users
def users_dashboard(api_key):
    st.title("Users Management")

    # Display existing users
    st.subheader("Existing Users")
    users = get_users()
    df_users = pd.DataFrame(users)
    st.dataframe(df_users, use_container_width=True)

    # Form to add a new user
    st.subheader("Add New user")
    new_user_name = st.text_input("user Name")

    if st.button("Add user"):
        if new_user_name.strip():
            add_user(api_key, new_user_name)
        else:
            st.error("user name cannot be empty.")

    # Choose an action to perform
    action = st.radio("What would you like to do?", options=["Update user", "Delete user"])

    if action == "Update user":
        selected_user = st.selectbox("Select user to Update", options=[user['name'] for user in users])
        new_name = st.text_input("New user Name", value=selected_user)

        if st.button("Update user"):
            user_id = next((user['id'] for user in users if user['name'] == selected_user), None)
            update_user(api_key, user_id, new_name)

    elif action == "Delete user":
        user_to_delete = st.selectbox("Select user to Delete", options=[user['name'] for user in users])
        if st.button("Delete user"):
            user_id = next((user['id'] for user in users if user['name'] == user_to_delete), None)
            delete_user(api_key, user_id)


# Dashboard for managing Assets
def assets_dashboard(api_key):
    st.title("Assets Management")

    # Display existing assets
    st.subheader("Existing Assets")
    assets = get_assets()
    users = get_users()

    user_id_to_name = {user['id']: user['name'] for user in users}
    for asset in assets:
        asset['user'] = user_id_to_name.get(asset['user_id'], 'Unknown')
        asset['genres'] = ', '.join(asset['genres'])  # Display genres as a comma-separated list of names
        del asset['user_id']

    df_assets = pd.DataFrame(assets)
    st.dataframe(df_assets, use_container_width=True)

    # Form to add a new asset
    st.subheader("Add New Asset")
    new_asset_name = st.text_input("Name")
    selected_user_name = st.selectbox("Select user", options=[user['name'] for user in users],
                                        key="select_user_add")
    new_asset_symbol = st.number_input("Average Rating", min_value=0.0, max_value=5.0, step=0.01)
    new_asset_genres = st.text_input("Genres (comma-separated names)")
    new_asset_year = st.number_input("Year", min_value=1440, max_value=datetime.now().year, step=1)

    if st.button("Add Asset"):
        if new_asset_name.strip() and new_asset_genres.strip():
            genres_list = [g.strip() for g in new_asset_genres.split(',') if g.strip()]
            selected_user_id = next((user['id'] for user in users if user['name'] == selected_user_name),
                                      None)
            asset_data = {
                "name": new_asset_name,
                "user_id": selected_user_id,
                "symbol":
                "type":
                "price":
            }
            add_asset(api_key, asset_data)
        else:
            st.error("error.")

    # Choose an action to perform
    action = st.radio("What would you like to do?", options=["Update Asset", "Delete Asset"], key="radio_action")

    if action == "Update Asset":
        selected_asset = st.selectbox("Select Asset to Update", options=[asset['title'] for asset in assets],
                                     key="select_asset_update")

        if selected_asset:
            asset = next((asset for asset in assets if asset['title'] == selected_asset), None)
            new_asset_title = st.text_input("Title", value=asset['title'])
            selected_user_name = st.selectbox("Select user", options=[user['name'] for user in users],
                                                index=[user['name'] for user in users].index(asset['user']),
                                                key="select_user_update")
            new_asset_average_rating = st.number_input("Average Rating", min_value=0.0, max_value=5.0, step=0.01,
                                                      value=asset['average_rating'])
            new_asset_genres = st.text_input("Genres (comma-separated names)",
                                            value=asset['genres'])  # Show existing genres as a comma-separated string
            new_asset_year = st.number_input("Year", min_value=1440, max_value=datetime.now().year, step=1,
                                            value=asset['published_year'])
            asset_id = asset['id']

            if st.button("Update Asset"):
                genres_list = [g.strip() for g in new_asset_genres.split(',') if g.strip()]
                asset_data = {
                    "title": new_asset_title,
                    "user_id": next((user['id'] for user in users if user['name'] == selected_user_name),
                                      None),
                    "asset_link": asset.get('asset_link', ""),
                    "genres": genres_list,  # Update with the list of genre names
                    "average_rating": new_asset_average_rating,
                    "published_year": new_asset_year
                }
                update_asset(api_key, asset_id, asset_data)

    elif action == "Delete Asset":
        asset_to_delete = st.selectbox("Select Asset to Delete", options=[asset['title'] for asset in assets],
                                      key="select_asset_delete")
        if st.button("Delete Asset"):
            asset_id = next((asset['id'] for asset in assets if asset['title'] == asset_to_delete), None)
            delete_asset(api_key, asset_id)


# Visualizations Dashboard

def visualizations_dashboard():
    st.title("Visualizations Dashboard")

    # Fetch the assets and users data
    assets = get_assets()
    users = get_users()

    if assets:
        # Convert assets to a DataFrame
        df_assets = pd.DataFrame(assets)

        if 'user_id' in df_assets.columns:
            # Map user_id to user names
            user_id_to_name = {user['id']: user['name'] for user in users}
            df_assets['user'] = df_assets['user_id'].map(user_id_to_name)
            df_assets.drop('user_id', axis=1, inplace=True)

        # Sidebar filters
        st.sidebar.title("Filters")

        # Filter by user
        selected_user = st.sidebar.selectbox("Select user", options=["All"] + list(user_id_to_name.values()))

        # Filter by Published Year
        min_year = int(df_assets['published_year'].min())
        max_year = int(df_assets['published_year'].max())
        selected_year = st.sidebar.slider("Select Published Year", min_value=min_year, max_value=max_year,
                                          value=(min_year, max_year))

        # Filter by Average Rating (fixed range from 0.0 to 5)
        selected_rating = st.sidebar.slider("Select Average Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0),
                                            step=0.1)

        # Check if any filters are applied
        filters_applied = selected_user != "All" or selected_year != (min_year, max_year) or selected_rating != (
            0.0, 5.0)

        # Apply Filters Button
        if st.sidebar.button("Apply Filters") or not filters_applied:
            # Apply filters if any are set
            filtered_assets = df_assets.copy()  # Default to showing all data if no filters applied

            if filters_applied:
                if selected_user != "All":
                    filtered_assets = filtered_assets[filtered_assets['user'] == selected_user]

                filtered_assets = filtered_assets[(filtered_assets['published_year'] >= selected_year[0]) & (
                        filtered_assets['published_year'] <= selected_year[1])]
                filtered_assets = filtered_assets[(filtered_assets['average_rating'] >= selected_rating[0]) & (
                        filtered_assets['average_rating'] <= selected_rating[1])]

            # Visualization 1: Assets by Year
            if not filtered_assets.empty:
                st.subheader(f"Assets by Year")
                assets_by_year = filtered_assets.groupby('published_year').size().reset_index(name='Count')
                fig_years = px.bar(
                    assets_by_year,
                    x='published_year',
                    y='Count',
                    title=f'Number of Assets by Year',
                    labels={"published_year": "Published Year", "Count": "Number of Assets"},
                    text='Count'
                )
                fig_years.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig_years.update_layout(
                    uniformtext_minsize=8,
                    uniformtext_mode='hide',
                    xaxis=dict(
                        tickmode='linear',
                        tick0=min_year,
                        dtick=5,  # Show a label every 5 years (adjust as needed)
                        tickangle=-45,
                        tickfont=dict(size=10)
                    ),
                    yaxis=dict(title='Number of Assets', range=[0, assets_by_year['Count'].max() + 1]),
                    title_x=0.5
                )
                st.plotly_chart(fig_years, use_container_width=True)

                # Visualization 2: Assets by Average Rating
                st.subheader(f"Assets by Average Rating")
                assets_by_rating = filtered_assets.groupby('average_rating').size().reset_index(name='Count')
                fig_ratings = px.bar(
                    assets_by_rating,
                    x='average_rating',
                    y='Count',
                    title='Number of Assets by Average Rating',
                    labels={"average_rating": "Average Rating", "Count": "Number of Assets"},
                    text='Count'
                )
                fig_ratings.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig_ratings.update_layout(
                    uniformtext_minsize=8,
                    uniformtext_mode='hide',
                    yaxis=dict(title='Number of Assets', range=[0, assets_by_rating['Count'].max() + 1]),
                    title_x=0.5
                )
                st.plotly_chart(fig_ratings, use_container_width=True)
            else:
                st.warning("No asset data available for the selected filters.")
    else:
        st.warning("No asset data available for visualizations.")


# Main app logic
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a dashboard", ["Users Dashboard", "Assets Dashboard", "Visualizations"])
if option == "Visualizations":
    visualizations_dashboard()
if api_key_input and validate_api_key(api_key_input):
    if option == "Users Dashboard":
        users_dashboard(api_key_input)
    elif option == "Assets Dashboard":
        assets_dashboard(api_key_input)
else:
    st.error("Invalid API Key or API Key is missing.")