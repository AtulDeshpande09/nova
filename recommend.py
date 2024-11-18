# Simple dictionary with fertilizer recommendations
fertilizer_recommendations = {
    "wheat": "Use NPK 20:20:20 during early growth and a nitrogen boost later.",
    "corn": "Apply nitrogen-based fertilizers like urea at planting and mid-season.",
    "rice": "Use NPK 16:16:16 at the start and a top-dressing of urea at tillering."
}

# Function to provide fertilizer recommendations
def recommend_fertilizer(crop_type):
    recommendation = fertilizer_recommendations.get(crop_type.lower(), "No specific recommendation available.")
    return recommendation

# Ask the user for the crop type
crop_type = input("Enter the crop type for a fertilizer recommendation (e.g., wheat, corn, rice): ")
print(recommend_fertilizer(crop_type))
