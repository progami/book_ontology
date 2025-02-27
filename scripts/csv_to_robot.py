#!/usr/bin/env python3
"""
csv_to_robot.py
Converts book_criteria.csv to ROBOT template files for ontology creation.

This script generates:
- robot_classes.csv
- robot_object_properties.csv
- robot_data_properties.csv
- robot_individuals.csv
"""

import pandas as pd
import os

def generate_id(prefix, index):
    """Generate a properly formatted ID with prefix and zero-padded index"""
    return f"{prefix}:{str(index).zfill(7)}"

def safe_str(value, default=""):
    """Convert value to string, handling NaN values"""
    if pd.isna(value):
        return default
    return str(value)

def create_class_template():
    """Create a classes template file"""
    classes = [
        ["ID", "Label", "Type", "Subclass Of", "Definition", "Comment"],
        ["ID", "LABEL", "TYPE", "SC %", "A IAO:0000115", "A rdfs:comment"],
        ["BOOK:0000001", "book", "owl:Class", "", "A published work consisting of pages", "The root class for all books"],
        ["BOOK:0000002", "quantitative measures", "owl:Class", "BOOK:0000001", "Measures that provide numerical assessment of text complexity", ""],
        ["BOOK:0000003", "qualitative measures", "owl:Class", "BOOK:0000001", "Measures that provide subjective assessment of text complexity", ""],
        ["BOOK:0000004", "general descriptors", "owl:Class", "BOOK:0000001", "General descriptive categories for books", ""],
        ["BOOK:0000005", "instructional merit descriptors", "owl:Class", "BOOK:0000001", "Descriptors related to educational value", ""]
    ]
    
    df = pd.DataFrame(classes)
    df.to_csv('../robot_classes.csv', index=False, header=False)
    print("Created ../robot_classes.csv with", len(classes) - 2, "classes")

def create_object_properties_template():
    """Create an object properties template file"""
    props = [
        ["ID", "Label", "Type", "Domain", "Range", "Definition", "Characteristic"],
        ["ID", "LABEL", "TYPE", "DOMAIN", "RANGE", "A IAO:0000115", "CHARACTERISTIC"],
        ["BOOK:1000001", "has descriptor", "owl:ObjectProperty", "BOOK:0000001", "", "Property linking a book to its descriptors", ""]
    ]
    
    df = pd.DataFrame(props)
    df.to_csv('../robot_object_properties.csv', index=False, header=False)
    print("Created ../robot_object_properties.csv")

def create_data_properties_template():
    """Create a data properties template file"""
    props = [
        ["ID", "Label", "Type", "Domain", "Range", "Definition"],
        ["ID", "LABEL", "TYPE", "DOMAIN", "RANGE", "A IAO:0000115"],
        ["BOOK:2000001", "title", "owl:DatatypeProperty", "BOOK:0000001", "xsd:string", "The title of the book"],
        ["BOOK:2000002", "author", "owl:DatatypeProperty", "BOOK:0000001", "xsd:string", "The author of the book"]
    ]
    
    df = pd.DataFrame(props)
    df.to_csv('../robot_data_properties.csv', index=False, header=False)
    print("Created ../robot_data_properties.csv")

def create_individuals_template(book_data):
    """Create a proper individuals template that will pass all checks"""
    individuals = []
    
    # IMPORTANT: For individuals, we use TYPE as owl:NamedIndividual and a separate column for class assertions
    header = ["ID", "Label", "Type", "Class Assertion", "Title", "Author"]
    
    # The template row uses proper ROBOT template strings
    template = ["ID", "LABEL", "TYPE", "SC %", "A rdfs:label", "A rdfs:comment"]
    
    individuals.append(header)
    individuals.append(template)
    
    # Add book entries - using proper TYPE and class assertions
    for idx, row in book_data.iterrows():
        book_id = generate_id("BOOK", 3000001 + idx)
        book_title = safe_str(row.get('book', f'Book {idx+1}'))
        author = safe_str(row.get('author', ''))
        
        # Create a properly formatted individual entry
        book_entry = [
            book_id,                   # ID
            book_title,                # Label
            "owl:NamedIndividual",     # Type - this is the correct way to specify an individual
            "BOOK:0000001",            # Class Assertion - this specifies it's an instance of book
            book_title,                # Title annotation
            author                     # Author annotation
        ]
        
        individuals.append(book_entry)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(individuals)
    df.to_csv('../robot_individuals.csv', index=False, header=False)
    print("Created ../robot_individuals.csv with", len(individuals) - 2, "books")

def main():
    # Read book data from the input directory
    input_path = '../input/book_criteria.csv'
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found")
        return
    
    try:
        # Read the CSV file
        book_data = pd.read_csv(input_path)
        print(f"Successfully loaded book data with {len(book_data)} rows")
        
        # Create all templates
        create_class_template()
        create_object_properties_template()
        create_data_properties_template()
        create_individuals_template(book_data)
        
        print("\nAll ROBOT templates created successfully")
        print("Next steps:")
        print("1. Run the robot_to_owl.sh script to create your ontology")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
