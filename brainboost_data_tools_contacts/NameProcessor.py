class NameProcessor:


    def __init__(self) -> None:
        pass


    def extract_first_last_name(self, full_name):
        # Split the full name into parts based on spaces
        if full_name:
            name_parts = full_name.split(' ')

            if len(name_parts)==2:
                first_name = name_parts[0]
                last_name = name_parts[1]
            else:
                if len(name_parts)==3:
                    first_name = ' '.join(name_parts[0:2])
                    last_name = ' '.join(name_parts[-1])
                else:
                    if len(name_parts)==4:
                        first_name = ' '.join(name_parts[0:2])
                        last_name = ' '.join(name_parts[2:4])
                    else:
                        if len(name_parts)==5:
                            first_name = ' '.join(name_parts[0:2])
                            last_name = ' '.join(name_parts[2:5])

            return first_name, last_name
        else:
            return '',''

