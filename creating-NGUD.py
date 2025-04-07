import sys
import re

def transform_text(text):
    # Post-processing substitutions for tab-delimited patterns
    def apply_post_processing(text):
        # Apply the specified substitutions in the given order
        text = re.sub(r'(\t)ου(\t)ου(\t)DET(\t)', r'\1η\2η\3DET\4', text)
        text = re.sub(r'(\t)Ου(\t)ου(\t)DET(\t)', r'\1Η\2η\3DET\4', text)
        text = re.sub(r'(\t)ου(\t)DET(\t)', r'\1η\2DET\3', text)
        text = re.sub(r'(\t)Κι(\t)κι(\t)CCONJ(\t)', r'\1Τσι\2τσι\3CCONJ\4', text)
        text = re.sub(r'(\t)κι(\t)κι(\t)CCONJ(\t)', r'\1τσι\2τσι\3CCONJ\4', text)
        return text
    
    # Split text into words while preserving whitespace and punctuation
    def split_with_separators(text):
        pattern = r'(\s+|[.,!?;:"\'\(\)\[\]\{\}])'
        parts = re.split(pattern, text)
        result = []
        i = 0
        while i < len(parts):
            if i+1 < len(parts) and re.match(pattern, parts[i+1]):
                # Combine word with its following separator
                result.append(parts[i] + parts[i+1])
                i += 2
            else:
                result.append(parts[i])
                i += 1
        return result
    
    # Process each part (word or separator)
    def process_parts(parts):
        result = []
        for part in parts:
            if part.strip() == "":
                # Keep whitespace and separators unchanged
                result.append(part)
            else:
                # Transform content part
                transformed = transform_word(part)
                
                # Check if the word would be completely deleted
                if transformed.strip() == "" and part.strip() != "":
                    # Keep original if transformation would delete entire word
                    result.append(part)
                else:
                    result.append(transformed)
        return ''.join(result)
    
    # Function to count consonants in a cluster
    def count_consonant_weight(text):
        # Greek vowels
        vowels = 'αεηιουωάέήίόύώΑΕΗΙΟΥΩΆΈΉΊΌΎΏ'
        # Count Ξ/ξ and Ψ/ψ as 2 consonants each
        double_consonants = 'ΞξΨψ'
        
        count = 0
        for char in text:
            if char in vowels:
                count = 0  # Reset count for vowels
            elif char in double_consonants:
                count += 2  # Double consonants count as 2
            elif char not in vowels and char.isalpha():
                count += 1  # Regular consonants count as 1
            # Non-alphabetic characters don't affect the count
        return count
    
    # Check if deletion would create a consonant cluster > 3 or identical adjacent consonants
    def would_create_problematic_consonants(word, pos):
        # Greek vowels for reference
        vowels = 'αεηιουωάέήίόύώΑΕΗΙΟΥΩΆΈΉΊΌΎΏ'
        
        # Create a simulated version of the word with the character at pos deleted
        simulated = word[:pos] + word[pos+1:]
        
        # Check for identical adjacent consonants
        if pos > 0 and pos < len(word) - 1:
            left_char = simulated[pos-1] if pos-1 >= 0 else ''
            right_char = simulated[pos] if pos < len(simulated) else ''
            
            # Check if both are consonants and identical
            if (left_char not in vowels and right_char not in vowels and 
                left_char.isalpha() and right_char.isalpha() and 
                left_char.lower() == right_char.lower()):
                return True
        
        # Find all consonant clusters
        clusters = re.finditer(r'[^αεηιουωάέήίόύώΑΕΗΙΟΥΩΆΈΉΊΌΎΏ]+', simulated)
        
        for cluster in clusters:
            # Check if this cluster is at or near the deletion point
            if (pos >= cluster.start() - 1 and pos <= cluster.end()):
                # Count the consonant weight of this cluster
                weight = count_consonant_weight(cluster.group())
                if weight > 3:
                    return True
        
        return False
    
    # Check if the current word matches the excluded patterns
    def is_excluded_pattern(word):
        # Check if the word matches any of the excluded patterns
        excluded_patterns = [
            r'^\tη\tο\tDET\t',
            r'^\tΗ\tο\tDET\t',
            r'^\tΟι\tο\tDET\t',
            r'^\tοι\tο\tDET\t'
        ]
        
        for pattern in excluded_patterns:
            if re.match(pattern, word):
                return True
        return False
    
    # Check if the word is one of the excluded whole words
    def is_excluded_whole_word(word):
        excluded_whole_words = ['οι', 'Οι', 'η', 'Η']
        return word.strip() in excluded_whole_words
    
    # Check if a word contains any of the exception sequences that should be preserved
    def contains_exception_sequence(word):
        # Fixed exception sequences
        exception_sequences = [
            'εύ', 'Εύ', 'άι', 'Άι', 'αει', 'Αει', 'άει', 'Άει', 
            'αη', 'Αη', 'άη', 'Άη', 'άυ', 'Άυ', 'όι', 'Όι', 
            'οη', 'Οη', 'όη', 'Όη', 'όυ', 'Όυ', 'έει'
        ]
        
        # Check for fixed sequences
        for seq in exception_sequences:
            if seq in word:
                return True
                
        return False
        
    # Apply post-processing for whole words after "text ="
    def post_process_whole_word(word):
        word_map = {
            'Ου': 'Η',
            'ου': 'η',
            'κι': 'τσι',
            'Κι': 'Τσι'
        }
        if word.strip() in word_map:
            return word.replace(word.strip(), word_map[word.strip()])
        return word
    
    # Apply transformations to a single word
    def transform_word(word):
        # Skip transformation if word matches excluded patterns or is an excluded whole word
        if is_excluded_pattern(word) or is_excluded_whole_word(word):
            return word
        
        # Preserve "ίου" before other transformations
        word = re.sub(r'ίου', '<<preserve_iou>>', word)
        
        # Preserve all exception sequences before transformations
        exception_sequences = [
            ('εύ', '<<preserve_eu>>'), 
            ('Εύ', '<<preserve_Eu>>'), 
            ('άι', '<<preserve_ai>>'), 
            ('Άι', '<<preserve_Ai>>'),
            ('αει', '<<preserve_aei>>'),
            ('Αει', '<<preserve_Aei>>'),
            ('άει', '<<preserve_aei_a>>'),
            ('Άει', '<<preserve_Aei_A>>'),
            ('έει', '<<preserve_eei>>'),
            ('αη', '<<preserve_ah>>'),
            ('Αη', '<<preserve_Ah>>'),
            ('άη', '<<preserve_ah_a>>'),
            ('Άη', '<<preserve_Ah_A>>'),
            ('άυ', '<<preserve_au>>'),
            ('Άυ', '<<preserve_Au>>'),
            ('όι', '<<preserve_oi>>'),
            ('Όι', '<<preserve_Oi>>'),
            ('οη', '<<preserve_oh>>'),
            ('Οη', '<<preserve_Oh>>'),
            ('όη', '<<preserve_oh_o>>'),
            ('Όη', '<<preserve_Oh_O>>'),
            ('όυ', '<<preserve_ou>>'),
            ('Όυ', '<<preserve_Ou>>')
        ]
        
        for seq, placeholder in exception_sequences:
            word = word.replace(seq, placeholder)
        
        for seq, placeholder in exception_sequences:
            word = word.replace(seq, placeholder)
        
        # Apply transformations 1-16
        word = re.sub(r'οι', 'ι', word)
        word = re.sub(r'ει', 'ι', word)
        word = re.sub(r'Οι', 'Ι', word)
        word = re.sub(r'Ει', 'Ι', word)
        word = re.sub(r'ου', '#%', word)
        word = re.sub(r'Ου', '%#', word)
        word = re.sub(r'αι', 'ε', word)
        word = re.sub(r'Αι', 'Ε', word)
        
        # Rule-based deletion of "ι" with conditions
        def delete_i(match):
            pos = match.start()
            preceding = word[pos - 1] if pos > 0 else ''
            following = word[pos + 1] if pos + 1 < len(word) else ''
            
            # Check existing conditions
            if preceding in 'αεηιουωάέήίόύώ' or following in 'αεηιουωάέήίόύώ':
                return match.group(0)
                
            # Check if deletion would create a large consonant cluster or identical adjacent consonants
            if would_create_problematic_consonants(word, pos):
                return match.group(0)
                
            return ''
        
        word = re.sub(r'ι', delete_i, word)
        
        # For uppercase I, check consonant cluster before deletion
        def delete_uppercase_i(match):
            pos = match.start()
            if would_create_problematic_consonants(word, pos):
                return match.group(0)
            return ''
            
        word = re.sub(r'Ι', delete_uppercase_i, word)
        word = re.sub(r'#%', '', word)
        word = re.sub(r'%#', '', word)
        
        # For η deletion, check consonant cluster
        def delete_eta(match):
            pos = match.start()
            if would_create_problematic_consonants(word, pos):
                return match.group(0)
            return ''
            
        word = re.sub(r'η', delete_eta, word)
        word = re.sub(r'Η', delete_eta, word)
        
        # Rule-based deletion of "υ" with conditions
        def delete_u(match):
            pos = match.start()
            preceding = word[pos - 1] if pos > 0 else ''
            following = word[pos + 1] if pos + 1 < len(word) else ''
            
            # Check existing conditions
            if preceding in 'αεηιουΑΕΗΙΟ' or following in 'αεηιουωάέήίόύώ':
                return match.group(0)
                
            # Check if deletion would create a large consonant cluster or identical adjacent consonants
            if would_create_problematic_consonants(word, pos):
                return match.group(0)
                
            return ''
        
        word = re.sub(r'υ', delete_u, word)
        
        # For uppercase Y, check consonant cluster before deletion
        def delete_uppercase_y(match):
            pos = match.start()
            if would_create_problematic_consonants(word, pos):
                return match.group(0)
            return ''
            
        word = re.sub(r'Υ', delete_uppercase_y, word)
        
        # Apply transformations 17-22
        word = re.sub(r'ε(?!ί)', 'ι', word)
        word = re.sub(r'Ε(?!ί)', 'Ι', word)
        word = re.sub(r'ο(?!ύ|ί)', 'ου', word)
        word = re.sub(r'Ο(?!ύ|ί)', 'Ου', word)
        word = re.sub(r'ω', 'ου', word)
        word = re.sub(r'Ω', 'Ου', word)
        
        # Restore "ίου" after all transformations
        word = re.sub(r'<<preserve_iou>>', 'ίου', word)
        
        # Restore all exception sequences
        for seq, placeholder in exception_sequences:
            word = word.replace(placeholder, seq)
        
        return word
    
    # Split text, transform each part, and join back
    parts = split_with_separators(text)
    
    # Process the text and apply post-processing
    processed_text = process_parts(parts)
    processed_text = apply_post_processing(processed_text)
    
    # Process sentences after "# text = " in CoNLL-U format
    lines = processed_text.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('# text = '):
            # Extract the sentence text
            text_part = line[line.index('=')+1:].strip()
            
            # Apply word substitutions for the sentence
            for old_word, new_word in [('Ου', 'Η'), ('ου', 'η'), ('κι', 'τσι'), ('Κι', 'Τσι')]:
                # Use word boundaries to match whole words only
                text_part = re.sub(r'\b' + old_word + r'\b', new_word, text_part)
            
            # Update the line with the modified sentence
            lines[i] = '# text = ' + text_part
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python transform_text.py path_to_input_file.txt path_to_output_file.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        transformed_text = transform_text(text)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(transformed_text)
        
        print(f"Transformation complete. Output written to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()