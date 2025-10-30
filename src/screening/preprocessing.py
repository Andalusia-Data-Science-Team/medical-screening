import pandas as pd

def preprocessing(filepath: str, sheet_name: str = "KSA") -> pd.DataFrame:
    """
    Preprocess doctor skills data by loading from Excel and cleaning specific columns.

    Args:
        filepath (str): Path to the Excel file.
        sheet_name (str): Sheet name to load (default is 'KSA').

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Load data
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    # Select relevant columns
    df = df[['Title', 'Specialty', 'SubSpecialty', 'Scope of Service', 'Degree']]

    # Clean unwanted patterns
    for col in ["Specialty", "SubSpecialty", "Degree"]:
        df[col] = df[col].astype(str).str.replace(r";#\d+", "", regex=True)

    return df

def format_doctors(df, specialty):
    """
    Format doctor information from a DataFrame into a readable string.

    Iterates through each row of the given DataFrame and concatenates
    the values of 'Title', 'Degree', 'SubSpecialty', and 'Scope of Service'
    into a human-readable string. The output contains one line per doctor.

    Args:
        df (pd.DataFrame): A pandas DataFrame with at least the columns
            ['Title', 'Degree', 'SubSpecialty', 'Scope of Service'].

    Returns:
        str: A single string where each line represents one doctor,
        formatted as:
        "Title - Degree in SubSpecialty - Scope of Service"
    """
    df = df[df['Specialty'] == specialty]
    formatted = []
    for _, row in df.iterrows():
        formatted.append(
            f"{row['Title']} - {row['Degree']} in {row['SubSpecialty']} - {row['Scope of Service']}"
        )
    return "\n".join(formatted)
