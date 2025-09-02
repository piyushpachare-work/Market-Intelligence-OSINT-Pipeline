from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Define the associated terms and their importance (simulated using frequency)
associated_terms = {
    "Snacks": 100,
    "Sweets": 90,
    "Quality": 85,
    "Taste": 80,
    "India": 75,
    "Festival": 70,
    "Tradition": 65,
    "Gift": 60,
    "Packaging": 55,
    "Hygiene": 50
}

# Step 2: Generate the word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='viridis'
).generate_from_frequencies(associated_terms)

# Step 3: Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Haldiram Brand Association Cloud", fontsize=16)
plt.show()
