class EmailProcessor:

    def __init__(self) -> None:
        pass


    def generate_email_variations(self, name, company):
        """
        Generates a more comprehensive list of possible email addresses for a person

        Args:
            name (str): A string containing the person's name (first, middle, or last)
            company (str): The company domain name

        Returns:
            list: A list of strings containing possible email address variations
        """
        name_parts = name.lower().split()
        variations = []

        # Separator variations (dot, underscore, hyphen, no separator)
        separators = [".", "_", "-", ""]

        # Domain variations (common extensions)
        domains = [".com", ".net", ".org", ".co"]

        # Generate variations with initials, middle name, and combinations
        for sep in separators:
            for domain in domains:
                # First name variations (full name, initials)
                variations.append(f"{name_parts[0]}{sep}{name_parts[-1]}{domain}@{company}")
                variations.append(f"{name_parts[0][0]}{sep}{name_parts[-1]}{domain}@{company}")

                # Variations with middle name (if provided)
                if len(name_parts) > 1:
                    variations.append(f"{name_parts[0]}{sep}{name_parts[1]}{sep}{name_parts[-1]}{domain}@{company}")
                    variations.append(f"{name_parts[0][0]}{sep}{name_parts[1]}{sep}{name_parts[-1]}{domain}@{company}")

        return variations

# Example usage inside the EmailProcessor class
name1 = "Liz Adeniji"
company = "segment"

# Create an instance of EmailProcessor
email_processor = EmailProcessor()

# Call the method on the instance
possible_emails1 = email_processor.generate_email_variations(name1, company)

print(possible_emails1)
