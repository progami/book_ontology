import pandas as pd
import os

# Read book data from the input directory
book_data = pd.read_csv('../input/book_criteria.csv')

# Clean column names (remove spaces and special characters)
book_data.columns = [c.strip().replace(' ', '_').replace('/', '_') for c in book_data.columns]

# Function to generate new ID
def generate_id(prefix, index):
    return f"{prefix}:{str(index).zfill(7)}"

# Create individuals template
def create_individuals_template(book_data):
    individuals = []
    
    # Create header rows - first row is human-readable, second has ROBOT keywords
    # Use CURIEs (BOOK:2000001) instead of labels (title) for property references
    header = ["ID", "Label", "Type", "Instance Of", "Title", "Author", "Year", "Pages", "Summary"]
    template_row = ["ID", "LABEL", "TYPE", "TI %", "I BOOK:2000001", "I BOOK:2000004", 
                   "I BOOK:2000002", "I BOOK:2000003", "I BOOK:2000005"]
    
    individuals.append(header)
    individuals.append(template_row)
    
    # Add book entries
    for idx, row in book_data.iterrows():
        book_id = generate_id("BOOK", 3000001 + idx)
        
        # Create a book entry
        book_entry = [
            book_id,
            str(row.get('book', '')),
            "owl:NamedIndividual", 
            "BOOK:0000001",  # Reference to the "book" class
            str(row.get('book', '')),
            str(row.get('author', '')),
            str(int(row.get('year_of_publication', 0))) if not pd.isna(row.get('year_of_publication', 0)) else '',
            str(int(row.get('pages', 0))) if not pd.isna(row.get('pages', 0)) else '',
            str(row.get('summary', ''))
        ]
        
        individuals.append(book_entry)
    
    # Create DataFrame and save to CSV - using parent directory
    df = pd.DataFrame(individuals)
    df.to_csv('../robot_individuals.csv', index=False, header=False)
    print("Created ../robot_individuals.csv with", len(individuals) - 2, "books")

# Create separate templates
def create_class_template():
    classes = [
        ["ID", "Label", "Type", "Subclass Of", "Definition", "Comment"],
        ["ID", "LABEL", "TYPE", "SC %", "A IAO:0000115", "A rdfs:comment"],
        ["BOOK:0000001", "book", "owl:Class", "", "A published work consisting of pages", "The root class for all books"],
        ["BOOK:0000002", "Quantitative measures", "owl:Class", "BOOK:0000001", "Measures that provide numerical assessment of text complexity", ""],
        ["BOOK:0000003", "Qualitative measures", "owl:Class", "BOOK:0000001", "Measures that provide subjective assessment of text complexity", ""],
        ["BOOK:0000004", "General descriptors", "owl:Class", "BOOK:0000001", "General descriptive categories for books", ""],
        ["BOOK:0000005", "Instructional merit descriptors", "owl:Class", "BOOK:0000001", "Descriptors related to educational value", ""],
        ["BOOK:0000006", "ATOS reading level", "owl:Class", "BOOK:0000002", "A readability formula for books and other materials", ""],
        ["BOOK:0000007", "Lexile level", "owl:Class", "BOOK:0000002", "A scale for measuring reader ability and text difficulty", ""],
        ["BOOK:0000008", "Flesch kincaid", "owl:Class", "BOOK:0000002", "A readability test designed to indicate comprehension difficulty", ""],
        ["BOOK:0000009", "levels of meaning", "owl:Class", "BOOK:0000003", "The depth and complexity of meanings within a text", ""],
        ["BOOK:0000010", "knowledge demands", "owl:Class", "BOOK:0000003", "Prior knowledge required to understand the text", ""],
        ["BOOK:0000011", "text structure", "owl:Class", "BOOK:0000003", "The organizational pattern of the text", ""],
        ["BOOK:0000012", "language conventionality and clarity", "owl:Class", "BOOK:0000003", "The clarity and accessibility of the language used", ""],
        ["BOOK:0000013", "genre", "owl:Class", "BOOK:0000004", "A category of literary composition", ""],
        ["BOOK:0000014", "topic", "owl:Class", "BOOK:0000004", "The subject matter of a text", ""],
        ["BOOK:0000015", "subgenre", "owl:Class", "BOOK:0000004", "A subcategory within a genre", ""]
    ]
    
    df = pd.DataFrame(classes)
    df.to_csv('../robot_classes.csv', index=False, header=False)
    print("Created ../robot_classes.csv")

def create_object_properties_template():
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
    print("Created ../robot_object_properties.csv")

def create_data_properties_template():
    props = [
        ["ID", "Label", "Type", "Domain", "Range", "Definition"],
        ["ID", "LABEL", "TYPE", "DOMAIN", "RANGE", "A IAO:0000115"],
        ["BOOK:2000001", "title", "owl:DatatypeProperty", "BOOK:0000001", "xsd:string", "The title of the book"],
        ["BOOK:2000002", "yearOfPublication", "owl:DatatypeProperty", "BOOK:0000001", "xsd:integer", "The year the book was published"],
        ["BOOK:2000003", "pages", "owl:DatatypeProperty", "BOOK:0000001", "xsd:integer", "The number of pages in the book"],
        ["BOOK:2000004", "author", "owl:DatatypeProperty", "BOOK:0000001", "xsd:string", "The author of the book"],
        ["BOOK:2000005", "summary", "owl:DatatypeProperty", "BOOK:0000001", "xsd:string", "A brief summary of the book's content"],
        ["BOOK:2000006", "lexile score", "owl:DatatypeProperty", "BOOK:0000007", "xsd:integer", "The numerical Lexile measure of text complexity"],
        ["BOOK:2000007", "flesch score", "owl:DatatypeProperty", "BOOK:0000008", "xsd:decimal", "The numerical Flesch-Kincaid readability score"],
        ["BOOK:2000008", "atos score", "owl:DatatypeProperty", "BOOK:0000006", "xsd:decimal", "The numerical ATOS readability score"]
    ]
    
    df = pd.DataFrame(props)
    df.to_csv('../robot_data_properties.csv', index=False, header=False)
    print("Created ../robot_data_properties.csv")

# Create all templates
create_class_template()
create_object_properties_template()
create_data_properties_template()
create_individuals_template(book_data)

print("All ROBOT templates created successfully.")
print("Next steps:")
print("1. Review the generated templates")
print("2. Run the ROBOT workflow to create your ontology")
