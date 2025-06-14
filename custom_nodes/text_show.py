import time

class TextShow:
    """
    A node for displaying text in the OneFlow web interface
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "forceInput": True
                }),
            },
            "optional": {
                "title": ("STRING", {
                    "default": "Generated Text",
                    "multiline": False,
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("displayed_text",)
    FUNCTION = "display_text"
    CATEGORY = "Text"
    OUTPUT_NODE = True

    def display_text(self, text, title="Generated Text"):
        """
        Display text in the web interface
        """
        # Create a formatted display text that will be shown in the UI
        display_content = f"=== {title} ===\n\n{text}\n\n=== End {title} ==="
        
        # Also print to console for debugging
        print(f"\n{display_content}")
        
        # Return the formatted text for display
        return {"ui": {"text": [display_content]}, "result": (text,)}

    @classmethod
    def IS_CHANGED(cls, text, title="Generated Text"):
        return f"{text}_{title}_{time.time()}"


class TextShowAdvanced:
    """
    An advanced text display node with more formatting options
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "forceInput": True
                }),
            },
            "optional": {
                "title": ("STRING", {
                    "default": "Advanced Text Output",
                    "multiline": False,
                }),
                "display_mode": (["full", "preview", "summary"], {
                    "default": "full"
                }),
                "preview_length": ("INT", {
                    "default": 200,
                    "min": 50,
                    "max": 1000,
                    "step": 50,
                    "display": "number"
                }),
                "show_stats": (["yes", "no"], {
                    "default": "yes"
                }),
                "highlight_keywords": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "comma,separated,keywords"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("text", "preview", "word_count", "char_count")
    FUNCTION = "show_text_advanced"
    CATEGORY = "Text"
    OUTPUT_NODE = True

    def show_text_advanced(self, text, title="Advanced Text Output", display_mode="full", 
                          preview_length=200, show_stats="yes", highlight_keywords=""):
        """
        Advanced text display with statistics and formatting
        """
        # Calculate statistics
        word_count = len(text.split())
        char_count = len(text)
        line_count = len(text.split('\n'))
        
        # Create preview
        if len(text) > preview_length:
            preview = text[:preview_length] + "..."
        else:
            preview = text
        
        # Build display content for web interface
        display_lines = []
        display_lines.append(f"{'='*50}")
        display_lines.append(f"📄 {title}")
        display_lines.append(f"{'='*50}")
        
        if show_stats == "yes":
            display_lines.append("📊 Statistics:")
            display_lines.append(f"   • Characters: {char_count:,}")
            display_lines.append(f"   • Words: {word_count:,}")
            display_lines.append(f"   • Lines: {line_count:,}")
            display_lines.append(f"   • Average words per line: {word_count/max(line_count, 1):.1f}")
            display_lines.append("")
        
        # Highlight keywords if provided
        if highlight_keywords.strip():
            keywords = [kw.strip() for kw in highlight_keywords.split(',') if kw.strip()]
            if keywords:
                display_lines.append(f"🔍 Highlighted keywords: {', '.join(keywords)}")
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        display_lines.append(f"   ✓ Found '{keyword}'")
                display_lines.append("")
        
        # Display text based on mode
        if display_mode == "preview":
            display_lines.append(f"📝 Preview ({preview_length} chars):")
            display_lines.append(preview)
        elif display_mode == "summary":
            lines = text.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            display_lines.append("📋 Summary:")
            display_lines.append(f"   • First line: {non_empty_lines[0] if non_empty_lines else 'N/A'}")
            if len(non_empty_lines) > 1:
                display_lines.append(f"   • Last line: {non_empty_lines[-1]}")
            display_lines.append(f"   • Total content: {char_count} characters, {word_count} words")
        else:  # full mode
            display_lines.append("📝 Full Text:")
            display_lines.append(text)
        
        display_lines.append(f"{'='*50}")
        
        # Join all lines for display
        display_content = "\n".join(display_lines)
        
        # Print to console for debugging
        print(f"\n{display_content}\n")
        
        # Return with UI display and results
        return {
            "ui": {"text": [display_content]}, 
            "result": (text, preview, word_count, char_count)
        }

    @classmethod
    def IS_CHANGED(cls, text, title="Advanced Text Output", display_mode="full", 
                   preview_length=200, show_stats="yes", highlight_keywords=""):
        return f"{text}_{title}_{display_mode}_{time.time()}"


# Node mappings
NODE_CLASS_MAPPINGS = {
    "TextShow": TextShow,
    "TextShowAdvanced": TextShowAdvanced
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextShow": "Text Show",
    "TextShowAdvanced": "Text Show Advanced"
}