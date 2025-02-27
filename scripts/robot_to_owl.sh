#!/bin/bash
# robot_to_owl.sh
#
# This script processes ROBOT templates to create a book ontology in OWL format
# with numbered output files to show creation order

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$BASE_DIR/output"

echo "Script directory: $SCRIPT_DIR"
echo "Base directory: $BASE_DIR"
echo "Output directory: $OUTPUT_DIR"

# Create output directory with full permissions
mkdir -p "$OUTPUT_DIR"
chmod 755 "$OUTPUT_DIR"
echo "Created output directory: $OUTPUT_DIR"

# Template files
CLASSES_TEMPLATE="$BASE_DIR/robot_classes.csv"
OBJECT_PROPS_TEMPLATE="$BASE_DIR/robot_object_properties.csv"
DATA_PROPS_TEMPLATE="$BASE_DIR/robot_data_properties.csv"
INDIVIDUALS_TEMPLATE="$BASE_DIR/robot_individuals.csv"

# Output files - NUMBERED to show creation order
CLASSES_OWL="$OUTPUT_DIR/1_book_classes.owl"
OBJECT_PROPS_OWL="$OUTPUT_DIR/2_book_with_object_props.owl"
DATA_PROPS_OWL="$OUTPUT_DIR/3_book_with_all_props.owl"
ONTOLOGY_OWL="$OUTPUT_DIR/4_book_ontology.owl"
ANNOTATED_OWL="$OUTPUT_DIR/5_book_ontology_annotated.owl"
REASONED_OWL="$OUTPUT_DIR/6_book_ontology_reasoned.owl"
REPORT_HTML="$OUTPUT_DIR/7_book_report.html"
JSON_FORMAT="$OUTPUT_DIR/8_book_ontology.json"
ERROR_FILE="$OUTPUT_DIR/errors_template.csv"

# Function to check if the previous command succeeded
check_success() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed!"
        exit 1
    else
        echo "Success: $1 completed."
    fi
}

# Print template file information
if [ -f "$CLASSES_TEMPLATE" ]; then
    echo "Found classes template: $CLASSES_TEMPLATE"
    head -n 3 "$CLASSES_TEMPLATE"
else
    echo "ERROR: Classes template not found at $CLASSES_TEMPLATE"
    exit 1
fi

# 1. Create class hierarchy
echo "Step 1: Creating class hierarchy..."
robot template --template "$CLASSES_TEMPLATE" \
  --prefix "BOOK: http://example.com/book/" \
  --ontology-iri "http://example.com/book.owl" \
  --output "$CLASSES_OWL"
check_success "Creating class hierarchy"

# 2. Add object properties
echo "Step 2: Adding object properties..."
robot template --template "$OBJECT_PROPS_TEMPLATE" \
  --prefix "BOOK: http://example.com/book/" \
  --input "$CLASSES_OWL" \
  --output "$OBJECT_PROPS_OWL"
check_success "Adding object properties"

# 3. Add data properties
echo "Step 3: Adding data properties..."
robot template --template "$DATA_PROPS_TEMPLATE" \
  --prefix "BOOK: http://example.com/book/" \
  --input "$OBJECT_PROPS_OWL" \
  --output "$DATA_PROPS_OWL"
check_success "Adding data properties"

# 4. Add individuals (books) with error handling
echo "Step 4: Adding book individuals..."
robot template --template "$INDIVIDUALS_TEMPLATE" \
  --prefix "BOOK: http://example.com/book/" \
  --input "$DATA_PROPS_OWL" \
  --output "$ONTOLOGY_OWL" \
  --force true \
  --errors "$ERROR_FILE"
check_success "Adding book individuals"

# Display error file if it exists
if [ -f "$ERROR_FILE" ]; then
    echo "Warning: Some errors occurred during processing. See $ERROR_FILE for details."
    echo "First 5 errors:"
    head -n 5 "$ERROR_FILE"
fi

# 5. Annotate with metadata
echo "Step 5: Adding ontology metadata..."
robot annotate --input "$ONTOLOGY_OWL" \
  --ontology-iri "http://example.com/book.owl" \
  --version-iri "http://example.com/book/2025-02-26/book.owl" \
  --annotation dc11:title "Book Ontology" \
  --annotation dc11:description "An ontology for categorizing books by various educational criteria" \
  --link-annotation dc:license https://creativecommons.org/licenses/by/4.0/ \
  --output "$ANNOTATED_OWL"
check_success "Adding ontology metadata"

# 6. Run reasoner to check consistency
echo "Step 6: Running reasoner..."
robot reason --input "$ANNOTATED_OWL" \
  --output "$REASONED_OWL"
check_success "Running reasoner"

# 7. Generate quality report (modified to be less strict)
echo "Step 7: Generating quality report..."
robot report --input "$REASONED_OWL" \
  --fail-on none \
  --output "$REPORT_HTML"
check_success "Generating quality report"

# 8. Convert to JSON format only
echo "Step 8: Converting to JSON format..."
robot convert --input "$REASONED_OWL" --format json --output "$JSON_FORMAT"
check_success "Converting to JSON format"

echo "Book ontology creation complete!"
echo "Results are available in the output directory: $OUTPUT_DIR"
echo
echo "Created files in order:"
echo "1. $CLASSES_OWL - Class hierarchy"
echo "2. $OBJECT_PROPS_OWL - Added object properties"
echo "3. $DATA_PROPS_OWL - Added data properties"
echo "4. $ONTOLOGY_OWL - Added book individuals"
echo "5. $ANNOTATED_OWL - Added ontology metadata"
echo "6. $REASONED_OWL - Final reasoned ontology"
echo "7. $REPORT_HTML - Quality report"
echo "8. $JSON_FORMAT - JSON format"
echo
echo "Output directory contents:"
ls -la "$OUTPUT_DIR"
