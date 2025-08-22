import json
import re

def clean_description(text):
    """Clean and format description text"""
    # Remove character name prefixes and formatting
    text = re.sub(r'^[A-Za-z\s]+Breakdownmotive', '', text)
    text = re.sub(r'BGM[A-Za-z\s]+video', '', text)
    text = re.sub(r'Description original text\[ Expand/Collapse \]', '', text)
    text = re.sub(r'\[ Expand/Collapse \]', '', text)
    text = re.sub(r'\[[0-9]+\]', '', text)
    text = re.sub(r'Motif \([^)]+\)', '', text)
    
    # Clean up extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Take first 200 characters and add ellipsis if longer
    if len(text) > 200:
        text = text[:200] + '...'
    
    return text

def extract_tags(links):
    """Extract tags from links, filtering out footnotes and special characters"""
    tags = []
    exclude = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]', '[10]', 
               '[11]', '[12]', '[13]', '[14]', '[15]', '[16]', '[17]', '[18]', '[19]', '[20]',
               '[21]', '[22]', '[23]', '[24]', '[25]', '[26]', '[27]', '[28]', '[29]', '[30]',
               '[chinese]', '24.1', '24.2', '.', '|', 'Rarely used image ▼']
    
    for link in links:
        if link['text'] not in exclude and len(link['text']) > 1:
            tags.append(link['text'])
    return tags[:5]  # Limit to 5 tags

def process_videos(videos):
    """Process videos and categorize them"""
    processed = []
    for video in videos:
        if 'youtu' in video['url']:
            processed.append({"url": video['url'], "text": "YT"})
        elif 'tiktok' in video['url']:
            processed.append({"url": video['url'], "text": "TT"})
    return processed[:3]  # Limit to 3 videos

def generate_html():
    """Generate the complete HTML file with all characters"""
    
    # Read the JSON file
    with open('namu_wiki_characters_clean_20250822_153713.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = data['characters']
    
    # Process all characters
    processed_characters = []
    for char in characters:
        section_num = char['section'].split('.')[1] if '.' in char['section'] else char['section']
        
        processed_char = {
            "name": char['name'],
            "section": section_num,
            "main_image": char['main_image'],
            "tags": extract_tags(char['links']),
            "description": clean_description(char['full_description']),
            "links": extract_tags(char['links']),
            "videos": process_videos(char['videos'])
        }
        processed_characters.append(processed_char)
    
    # Generate JavaScript array
    js_array = "const charactersData = [\n"
    for char in processed_characters:
        js_array += "    {\n"
        js_array += f'        "name": "{char["name"]}",\n'
        js_array += f'        "section": "{char["section"]}",\n'
        js_array += f'        "main_image": "{char["main_image"]}",\n'
        js_array += f'        "tags": {json.dumps(char["tags"])},\n'
        js_array += f'        "description": "{char["description"]}",\n'
        js_array += f'        "links": {json.dumps(char["links"])},\n'
        js_array += f'        "videos": {json.dumps(char["videos"])}\n'
        js_array += "    },\n"
    js_array += "];"
    
    # Read the HTML template
    with open('FULL_CHARACTERS_ARCHIVE.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace the JavaScript array in the HTML
    start_marker = "// ALL 59 CHARACTERS DATA"
    end_marker = "// Function to create character card"
    
    start_pos = html_content.find(start_marker)
    end_pos = html_content.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        new_html = html_content[:start_pos] + start_marker + "\n        " + js_array + "\n\n        " + html_content[end_pos:]
        
        # Write the complete HTML file
        with open('COMPLETE_59_CHARACTERS.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"✅ Generated complete HTML file with {len(processed_characters)} characters")
        print("📁 File saved as: COMPLETE_59_CHARACTERS.html")
        return True
    else:
        print("❌ Could not find markers in HTML template")
        return False

if __name__ == "__main__":
    generate_html()
