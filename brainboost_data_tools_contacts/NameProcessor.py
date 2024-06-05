class NameProcessor:
    def extract_first_last_name(self, name):
        first_name = ""
        last_name = ""
        try:
            # Assuming names are in the format "First Last"
            parts = name.split()
            if len(parts) > 1:
                first_name = parts[0]
                last_name = parts[-1]
            elif len(parts) == 1:
                first_name = parts[0]
        except Exception as e:
            print(f"Error extracting first and last name: {e}")
        return first_name, last_name
