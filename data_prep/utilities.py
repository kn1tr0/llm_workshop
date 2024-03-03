def parse_markdown_sections(file_path):
    """
    Parses a markdown file and collates text between headings and subheadings.
    """
    sections = {}
    current_section_title = "Title"  # Default section title for content before the first heading
    current_section_text = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('#'):
                # Save the previous section if it exists
                if current_section_text:
                    sections[current_section_title] = "\n".join(current_section_text)
                    current_section_text = []

                # Update the current section title, removing '#' characters and leading/trailing spaces
                current_section_title = line.strip().lstrip('#').strip()
            else:
                # Add line to the current section's text, if the line is not just whitespace
                if line.strip():
                    current_section_text.append(line.strip())

        # Don't forget to save the last section
        if current_section_text:
            sections[current_section_title] = "\n".join(current_section_text)

    return sections