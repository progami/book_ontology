import pandas as pd

def create_object_properties_template():
    # Create a template with the correct CHARACTERISTIC column
    props = [
        ["ID", "Label", "Type", "Domain", "Range", "Definition", "Characteristic"],
        ["ID", "LABEL", "TYPE", "DOMAIN", "RANGE", "A IAO:0000115", "CHARACTERISTIC"],
        ["BOOK:1000001", "has descriptor", "owl:ObjectProperty", "BOOK:0000001", "", "Property linking a book to its descriptors", ""],
        ["BOOK:1000002", "has genre", "owl:ObjectProperty", "BOOK:0000001", "BOOK:0000013", "Property linking a book to its genre", ""],
        ["BOOK:1000003", "has topic", "owl:ObjectProperty", "BOOK:0000004", "BOOK:0000014", "Property linking general descriptors to topics", ""],
        ["BOOK:1000004", "is part of", "owl:ObjectProperty", "", "", "Property indicating part-whole relationship", "transitive"],
        ["BOOK:1000005", "needs to satisfy", "owl:ObjectProperty", "BOOK:0000018", "BOOK:0000019", "Property indicating that a standard needs to satisfy state requirements", ""]
    ]
    
    df = pd.DataFrame(props)
    df.to_csv('../robot_object_properties.csv', index=False, header=False)
    print("Created ../robot_object_properties.csv with correct CHARACTERISTIC format")

create_object_properties_template()
