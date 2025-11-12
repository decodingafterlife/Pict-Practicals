import heapq
import collections
import os

class Node:
    """
    A node for the Huffman Tree.
    It stores the character, its frequency, and links to left/right children.
    """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Comparator for the priority queue (heapq).
        We compare nodes based on their frequency.
        This makes heapq a min-heap based on frequency.
        """
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq < other.freq

def build_huffman_tree(text):
    """
    Builds the Huffman tree from a given text.
    
    Returns:
        Node: The root node of the Huffman tree.
              Returns None if the text is empty.
    """
    if not text:
        return None

    # 1. Count frequencies of each character
    frequency = collections.Counter(text)

    # 2. Build a min-priority queue (min-heap)
    #    The queue will store the leaf nodes.
    priority_queue = []
    for char, freq in frequency.items():
        node = Node(char, freq)
        heapq.heappush(priority_queue, node)

    # 3. Build the tree using the greedy strategy
    #    Repeat until only one node (the root) is left in the queue.
    while len(priority_queue) > 1:
        # 3a. Extract the two nodes with the *smallest* frequencies
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)

        # 3b. Create a new internal node
        #     - Its frequency is the sum of its children's frequencies.
        #     - It has no specific character (we can use None or a placeholder).
        merged_freq = left_child.freq + right_child.freq
        merged_node = Node(None, merged_freq)
        merged_node.left = left_child
        merged_node.right = right_child

        # 3c. Add the new merged node back into the priority queue
        heapq.heappush(priority_queue, merged_node)

    # 4. The last remaining node is the root of the Huffman tree
    #    Handle the edge case of an empty queue (empty text)
    return priority_queue[0] if priority_queue else None

def generate_codes(root):
    """
    Generates the Huffman codes for each character by traversing the tree.
    
    Args:
        root (Node): The root of the Huffman tree.
        
    Returns:
        dict: A dictionary mapping characters to their binary code strings.
    """
    codes = {}
    
    def _build_codes_recursive(node, current_code):
        """Helper function to recursively traverse the tree."""
        if node is None:
            return

        # If this is a leaf node, we've found a character.
        # Store the code we've built so far.
        if node.char is not None:
            # Handle edge case of single-character text (e.g., "aaaaa")
            # The root itself is a leaf. We'll assign '0'.
            if not current_code:
                codes[node.char] = '0'
            else:
                codes[node.char] = current_code
            return

        # If it's an internal node, traverse left and right.
        # Append '0' for left and '1' for right.
        _build_codes_recursive(node.left, current_code + '0')
        _build_codes_recursive(node.right, current_code + '1')

    _build_codes_recursive(root, "")
    return codes

def encode(text, huffman_codes):
    """
    Encodes the original text using the generated Huffman codes.
    
    Args:
        text (str): The original text string.
        huffman_codes (dict): The map of char -> code.
        
    Returns:
        str: The binary encoded string.
    """
    encoded_text = ""
    for char in text:
        encoded_text += huffman_codes[char]
    return encoded_text

def decode(encoded_text, root):
    """
    Decodes a Huffman-encoded string using the Huffman tree.
    
    Args:
        encoded_text (str): The binary encoded string.
        root (Node): The root of the Huffman tree.
        
    Returns:
        str: The original, decoded text.
    """
    if root is None:
        return ""
        
    # Handle single-character text edge case
    if root.left is None and root.right is None:
        return root.char * len(encoded_text)

    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        # Traverse the tree based on the bit
        if bit == '0':
            current_node = current_node.left
        else: # bit == '1'
            current_node = current_node.right

        # If we've reached a leaf node, we've found a character
        if current_node.char is not None:
            decoded_text += current_node.char
            # Return to the root to start searching for the next character
            current_node = root
            
    return decoded_text

# --- Main execution example ---
if __name__ == "__main__":
    
    # 1. Define the input text
    sample_text = "this is an example for huffman encoding"
    
    if not sample_text:
        print("Input text is empty. Exiting.")
    else:
        print(f"Original Text: {sample_text}")
        print("-" * 30)

        # 2. Build the Huffman tree
        huffman_tree_root = build_huffman_tree(sample_text)

        # 3. Generate the codes
        huffman_codes = generate_codes(huffman_tree_root)

        print("Huffman Codes (Character -> Code):")
        # Sort by character for consistent output
        sorted_codes = sorted(huffman_codes.items())
        for char, code in sorted_codes:
            # Use repr(char) to make spaces and newlines visible
            print(f"  {repr(char):<5}: {code}")

        print("-" * 30)
        
        # 4. Encode the text
        encoded_data = encode(sample_text, huffman_codes)
        print(f"Encoded Data (length {len(encoded_data)} bits):")
        print(encoded_data)
        
        print("-" * 30)

        # 5. Decode the text
        decoded_data = decode(encoded_data, huffman_tree_root)
        print(f"Decoded Text:")
        print(decoded_data)
        
        print("-" * 30)

        # 6. Show compression results
        original_size_bits = len(sample_text) * 8 # Assuming 8 bits (ASCII) per char
        compressed_size_bits = len(encoded_data)
        
        print(f"Original Size:     {len(sample_text)} chars * 8 bits/char = {original_size_bits} bits")
        print(f"Compressed Size: {compressed_size_bits} bits")
        if original_size_bits > 0:
            compression_ratio = (1 - (compressed_size_bits / original_size_bits)) * 100
            print(f"Compression:       Saved {original_size_bits - compressed_size_bits} bits ({compression_ratio:.2f}% reduction)")
        
        # 7. Verification
        if sample_text == decoded_data:
            print("\nVerification successful: Original and decoded text match.")
        else:
            print("\nVerification FAILED: Original and decoded text do not match.")