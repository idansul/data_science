from mushroom_preprocessing import preprocessing
from mushroom_models import get_model, clustering_model
import pickle


def construct_models():
    """Constructs all the models in this project and pickles the 3 interesting ones"""
    
    # Gets the original dataframe after cleaning
    df = preprocessing()
    
    # First model: all of the data; yields perfect score, so uninteresting
    model2 = get_model(df, 2)
    
    # Second model: all of the data, except for "odor"; perfect score
    df3 = df.drop("odor", axis=1)
    model3 = get_model(df3, 3)
    
    # Third model: Only the "odor" features; close to perfect score
    df4 = df[["class", "odor"]]
    model4 = get_model(df4, 4)
    
    # Fourth model: Only colors related features; not a perfect score, so interesting
    df5 = df[["class"] + [i for i in df.columns if "color" in i]]
    model5 = get_model(df5, 5)
    with open("colors_model", "wb") as p:
        pickle.dump(model5, p)
    
    # Fifth model: Based only on population and habitat; interesting one
    df6 = df[["class", "population", "habitat"]]
    model6 = get_model(df6, 6)
    with open("area_model", "wb") as p:
        pickle.dump(model6, p)
    
    # Seventh model: all of the data but the target is generated by a 2-clustering algorithm; interesting
    model7 = clustering_model(df)
    with open("clustering_model", "wb") as p:
        pickle.dump(model7, p)
    
def use_models():
    """Returns one of the models that were pickled"""
    
    print("Which model would you like to use: Colors, Area or Clustering? ", end="")
    m = input("(C - for colors; A - for area; K - for clustering): ")
    if m == "C":
        with open("colors_model", "rb") as p:
            model_prediction(pickle.load(p))
    elif m == "A":
        with open("area_model", "rb") as p:
            model_prediction(pickle.load(p))
    elif m == "K":
        with open("clustering_model", "rb") as p:
            model_prediction(pickle.load(p))
    else:
        raise ValueError("Invalid input")
        
def model_prediction(model):
    """Gets a model and returns predictions according to the user's choice"""
    
    p = 0
    while p != "E":
        print("Which kind of prediction would you like to make? ", end="")
        p = input("(M - for manual; R - for random; B - go back to model selection; E - to exit): ")
        if p == "M":
            sample = []
            print("Enter your sample:")
            for i, col in enumerate(model.df.drop("class", axis=1).columns):
                values = ", ".join(model.uniques[i])
                sample.append(input(col + " (" + values + "): "))
            print(model.predict(sample))
        elif p == "R":
            print(model.random_predict())
        elif p == "B":
            use_models()


if __name__ == "__main__":
    print("Do you want reconstruct the models or to use them as a product? ", end="")
    v = input("(R - to reconstruct; U - to use): ")
    if v == "R":
        construct_models()
    elif v == "U":
        use_models()
    else:
        raise ValueError("Invalid input")