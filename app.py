import streamlit as st
import pickle
import numpy as np

# Load the data
popular_df = pickle.load(open('data/popular.pkl', 'rb'))
pt = pickle.load(open('data/pt.pkl', 'rb'))
with open('data/books.pkl', 'rb') as file:
    books = pickle.load(file)
with open('data/similarity_scores.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)

# Set the title, layout, and background image
st.set_page_config(page_title="Book Recommender System", layout="wide")
page_bg_img = '''
<style>
body {
    background-image: url("https://c1.wallpaperflare.com/preview/364/654/486/people-guy-reading-horizon.jpg");
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation 📚")
pages = ["Home 🏠", "Recommend 💡"]
selection = st.sidebar.radio("Go to", pages)

# Home Page
if selection == "Home 🏠":
    st.title("My Book Recommender")
    st.header("Top 20 Books 📖")

    # Grid layout with 4 books per row
    for i in range(0, 20, 4):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(popular_df['Image-URL-M'].values[i], width=150)
            st.subheader(popular_df['Book-Title'].values[i])
            st.write(f"**Author:** {popular_df['Book-Author'].values[i]}")
            st.write(f"**Votes:** {popular_df['Num_ratings'].values[i]}")
            st.write(f"**Rating:** {popular_df['avg_ratings'].values[i]}")

        with col2:
            st.image(popular_df['Image-URL-M'].values[i+1], width=150)
            st.subheader(popular_df['Book-Title'].values[i+1])
            st.write(f"**Author:** {popular_df['Book-Author'].values[i+1]}")
            st.write(f"**Votes:** {popular_df['Num_ratings'].values[i+1]}")
            st.write(f"**Rating:** {popular_df['avg_ratings'].values[i+1]}")

        with col3:
            st.image(popular_df['Image-URL-M'].values[i+2], width=150)
            st.subheader(popular_df['Book-Title'].values[i+2])
            st.write(f"**Author:** {popular_df['Book-Author'].values[i+2]}")
            st.write(f"**Votes:** {popular_df['Num_ratings'].values[i+2]}")
            st.write(f"**Rating:** {popular_df['avg_ratings'].values[i+2]}")

        with col4:
            st.image(popular_df['Image-URL-M'].values[i+3], width=150)
            st.subheader(popular_df['Book-Title'].values[i+3])
            st.write(f"**Author:** {popular_df['Book-Author'].values[i+3]}")
            st.write(f"**Votes:** {popular_df['Num_ratings'].values[i+3]}")
            st.write(f"**Rating:** {popular_df['avg_ratings'].values[i+3]}")

# Recommendation Page
elif selection == "Recommend 💡":
    st.title("Recommend Books")
    user_input = st.text_input("Enter book name...")

    if st.button("Recommend 📚"):
        try:
            index = np.where(pt.index == user_input)[0][0]  # Find the index of the book
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[
                            1:6]  # Get similar books

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]  # Find the book details
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)

            st.header("Recommended Books 📖")
            for i in data:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(i[2], width=150)
                with col2:
                    st.subheader(i[0])
                    st.write(f"**Author:** {i[1]}")
        except IndexError:
            st.error("Book not found! Please try another one.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Add loading animation (optional)
if st.button("Loading..."):
    st.write("Please wait while we fetch the recommendations...")

